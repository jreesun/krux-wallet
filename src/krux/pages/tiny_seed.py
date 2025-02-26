# The MIT License (MIT)

# Copyright (c) 2021-2024 Krux contributors

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import board
import lcd
import image
import sensor
import time
from embit.wordlists.bip39 import WORDLIST
from . import Page, FLASH_MSG_TIME, proceed_menu
from ..themes import theme
from ..wdt import wdt
from ..krux_settings import t
from ..display import (
    DEFAULT_PADDING,
    MINIMAL_PADDING,
    MINIMAL_DISPLAY,
    FONT_HEIGHT,
    FONT_WIDTH,
    NARROW_SCREEN_WITH,
    SMALLEST_HEIGHT,
)
from ..camera import BINARY_GRID_MODE
from ..input import BUTTON_ENTER, BUTTON_PAGE, BUTTON_PAGE_PREV, BUTTON_TOUCH
from ..bip39 import entropy_checksum

# Tiny Seed last bit index positions according to checksums
TS_LAST_BIT_NO_CS = 143
TS_LAST_BIT_12W_CS = 139
TS_LAST_BIT_24W_CS = 135

TS_ESC_START_POSITION = TS_LAST_BIT_NO_CS + 1
TS_ESC_END_POSITION = TS_ESC_START_POSITION + 5
TS_GO_POSITION = TS_ESC_START_POSITION + 11


class TinySeed(Page):
    """Class for handling Tinyseed format"""

    def __init__(self, ctx, label="Tiny Seed"):
        super().__init__(ctx, None)
        self.ctx = ctx
        self.label = label
        self.x_offset = MINIMAL_PADDING + 2 * FONT_WIDTH
        self.printer = None
        if self.ctx.display.width() > NARROW_SCREEN_WITH:
            self.x_pad = self.ctx.display.width() * 2 // 27
            self.y_pad = self.ctx.display.height() // 17
        else:
            self.x_pad = FONT_WIDTH + 1
            self.y_pad = FONT_HEIGHT
        if self.ctx.display.height() > SMALLEST_HEIGHT:
            self.y_offset = DEFAULT_PADDING + 3 * FONT_HEIGHT
        else:
            self.y_offset = 2 * FONT_HEIGHT

    def _draw_grid(self):
        """Draws grid for import and export Tinyseed UI"""
        y = self.y_offset
        x = self.x_offset
        for _ in range(13):
            self.ctx.display.draw_vline(
                x, self.y_offset, 12 * self.y_pad, theme.frame_color
            )
            x += self.x_pad
            self.ctx.display.draw_hline(
                self.x_offset, y, 12 * self.x_pad, theme.frame_color
            )
            y += self.y_pad

    def _draw_labels(self, page):
        """Draws labels for import and export Tinyseed UI"""
        self.ctx.display.draw_hcentered_text(self.label)
        # For non‑minimal displays, show extra bit numbers (rotate to landscape temporarily)
        if not MINIMAL_DISPLAY:
            self.ctx.display.to_landscape()
            bit_number = 2048
            bit_offset = MINIMAL_PADDING + 2 * FONT_HEIGHT
            for _ in range(12):
                lcd.draw_string(
                    (7 - len(str(bit_number))) * FONT_WIDTH - MINIMAL_PADDING,
                    self.ctx.display.width() - bit_offset,
                    str(bit_number),
                    theme.fg_color,
                    theme.bg_color,
                )
                bit_number //= 2
                bit_offset += self.x_pad
            self.ctx.display.to_portrait()
        # Draw row numbers on the left side
        y = self.y_offset + (self.y_pad - FONT_HEIGHT) // 2
        for i in range(12):
            line = "{:2}".format(page * 12 + i + 1)
            self.ctx.display.draw_string(MINIMAL_PADDING, y, line)
            y += self.y_pad

    def _draw_punched(self, words, page):
        """Draws punched bits for import and export Tinyseed UI"""
        y = self.y_offset
        # Compute radius for rounded corners if possible.
        radius = (
            ((self.x_pad - 5) // 3)
            if self.x_pad < self.y_pad
            else ((self.y_pad - 5) // 3)
        )
        if radius < 4:
            radius = 0
        # Determine whether we are working with words or numbers.
        is_word_list = isinstance(words[0], str)
        for row in range(12):
            if is_word_list:
                word_list_index = WORDLIST.index(words[page * 12 + row]) + 1
            else:
                word_list_index = words[page * 12 + row]
            for bit in range(12):
                if (word_list_index >> (11 - bit)) & 1:
                    x = self.x_offset + 3 + bit * self.x_pad
                    self.ctx.display.fill_rectangle(
                        x,
                        y + 3,
                        self.x_pad - 5,
                        self.y_pad - 5,
                        theme.highlight_color,
                        radius,
                    )
            y += self.y_pad

    def export(self):
        """Shows seed as a punch pattern for Tiny Seed layout"""
        words = self.ctx.wallet.key.mnemonic.split(" ")
        num_pages = len(words) // 12
        for page in range(num_pages):
            self._draw_labels(page)
            self._draw_grid()
            self._draw_punched(words, page)
            self.ctx.input.wait_for_button()
            self.ctx.display.clear()

    def print_tiny_seed(self):
        """Creates a bitmap image of a punched Tiny Seed and sends it to a thermal printer"""
        from ..printers import create_printer

        self.printer = create_printer()
        words = self.ctx.wallet.key.mnemonic.split(" ")
        image_size = 156
        border_y = 8
        border_x = 16
        grid_x_offset = border_x + 17  # border + offset
        grid_y_offset = border_y + 26  # border + offset
        pad_x = 7  # grid cell width in px
        pad_y = 8  # grid cell height in px
        self.ctx.display.clear()
        self.ctx.display.draw_hcentered_text(
            t("Printing.."), self.ctx.display.height() // 2
        )
        self.printer.print_string("Tiny Seed\n\n")
        num_pages = len(words) // 12
        for page in range(num_pages):
            ts_image = image.Image(size=(image_size, image_size), copy_to_fb=True)
            ts_image.clear()
            # Draw the frame (borders)
            ts_image.draw_rectangle(
                0, 0, 109 + 2 * border_x, border_y, lcd.WHITE, fill=True
            )
            ts_image.draw_rectangle(
                0, 138 + border_y, 109 + 2 * border_x, border_y, lcd.WHITE, fill=True
            )
            ts_image.draw_rectangle(0, border_y, border_x, 138, lcd.WHITE, fill=True)
            ts_image.draw_rectangle(
                109 + border_x, border_y, border_x, 138, lcd.WHITE, fill=True
            )

            # Draw grid lines
            x = grid_x_offset
            y = grid_y_offset
            for _ in range(13):
                ts_image.draw_line(x, y, x, y + 12 * pad_y, lcd.WHITE)
                x += pad_x
            y = grid_y_offset
            for _ in range(13):
                ts_image.draw_line(
                    grid_x_offset, y, grid_x_offset + 12 * pad_x, y, lcd.WHITE
                )
                y += pad_y

            # Draw punched bits into the grid.
            y = grid_y_offset
            for row in range(12):
                if isinstance(words[0], str):
                    word_list_index = WORDLIST.index(words[page * 12 + row]) + 1
                else:
                    word_list_index = words[page * 12 + row]
                for col in range(12):
                    if (word_list_index >> (11 - col)) & 1:
                        x = grid_x_offset + col * pad_x
                        ts_image.draw_rectangle(
                            x, y, pad_x, pad_y, lcd.WHITE, fill=True
                        )
                y += pad_y

            ts_image.to_grayscale()
            ts_image.binary([(125, 255)])
            # Print image line by line
            self.printer.set_bitmap_mode(image_size // 8, image_size, 3)
            for y in range(image_size):
                line_bytes = bytearray()
                x = 0
                for _ in range(image_size // 8):
                    im_byte = 0
                    for _ in range(8):
                        im_byte = (im_byte << 1) | (
                            1 if ts_image.get_pixel(x, y) else 0
                        )
                        x += 1
                    line_bytes.append(im_byte)
                self.printer.print_bitmap_line(bytes(line_bytes))
                wdt.feed()
            # Adjust grid offsets for subsequent pages if needed.
            grid_x_offset = border_x + 16
            grid_y_offset = border_y + 25
        self.printer.feed(4)
        self.ctx.display.clear()

    def _draw_index(self, index):
        """Outline index position"""
        height = self.y_pad - 2
        y_pos = (index // 12) * self.y_pad + self.y_offset + 1
        if index < TS_LAST_BIT_NO_CS:
            x_pos = (index % 12) * self.x_pad + self.x_offset + 1
            width = self.x_pad - 2
            self.ctx.display.outline(x_pos, y_pos, width, height, theme.fg_color)

    def _map_keys_array(self):
        """Maps an array of regions for keys to be placed in"""
        if self.ctx.input.touch is not None:
            self.ctx.input.touch.x_regions = [
                self.x_offset + i * self.x_pad for i in range(13)
            ]
            self.ctx.input.touch.y_regions = [
                self.y_offset + i * self.y_pad for i in range(13)
            ]
            self.ctx.input.touch.y_regions.append(self.ctx.display.height())

    def _draw_disabled(self, w24=False):
        """Draws disabled section where checksum is automatically filled"""
        if not w24:
            self.ctx.display.fill_rectangle(
                self.x_offset + 8 * self.x_pad,
                self.y_offset + 11 * self.y_pad,
                4 * self.x_pad,
                self.y_pad,
                theme.frame_color,
            )
            self.ctx.display.fill_rectangle(
                self.x_offset + 7 * self.x_pad,
                self.y_offset + 11 * self.y_pad,
                self.x_pad,
                self.y_pad,
                theme.disabled_color,
            )
        else:
            self.ctx.display.fill_rectangle(
                self.x_offset + 4 * self.x_pad,
                self.y_offset + 11 * self.y_pad,
                8 * self.x_pad,
                self.y_pad,
                theme.frame_color,
            )
            self.ctx.display.fill_rectangle(
                self.x_offset + 3 * self.x_pad,
                self.y_offset + 11 * self.y_pad,
                self.x_pad,
                self.y_pad,
                theme.disabled_color,
            )

    def _auto_checksum(self, word_numbers):
        """Automatically modify last word to add checksum"""
        checksum = check_sum_bg(word_numbers)
        if len(word_numbers) == 12:
            last_index = 11
            mask = 0b11111110000
        else:
            last_index = 23
            mask = 0b11100000000
        word_numbers[last_index] = (
            ((word_numbers[last_index] - 1) & mask) + checksum + 1
        )
        return word_numbers

    def _new_index(self, index, btn, w24, page):
        def _last_editable_bit():
            if w24:
                return TS_LAST_BIT_NO_CS if page == 0 else TS_LAST_BIT_24W_CS
            return TS_LAST_BIT_12W_CS

        if btn == BUTTON_PAGE:
            if index >= TS_GO_POSITION:
                index = 0
            elif index >= TS_ESC_END_POSITION:
                index = TS_GO_POSITION
            elif index >= _last_editable_bit():
                index = TS_ESC_END_POSITION
            else:
                index += 1
        elif btn == BUTTON_PAGE_PREV:
            if index <= 0:
                index = TS_GO_POSITION
            elif index <= _last_editable_bit():
                index -= 1
            elif index <= TS_ESC_END_POSITION:
                index = (
                    TS_LAST_BIT_NO_CS
                    if w24 and not page
                    else (TS_LAST_BIT_24W_CS if w24 else TS_LAST_BIT_12W_CS)
                )
            elif index <= TS_GO_POSITION:
                index = TS_ESC_END_POSITION
        return index

    def enter_tiny_seed(self, w24=False, seed_numbers=None, scanning_24=False):
        """UI to manually enter a Tiny Seed"""

        def _editable_bit():
            if w24:
                return index <= (TS_LAST_BIT_NO_CS if page == 0 else TS_LAST_BIT_24W_CS)
            return index <= TS_LAST_BIT_12W_CS

        index = TS_GO_POSITION if seed_numbers else 0
        if seed_numbers:
            tiny_seed_numbers = seed_numbers
        elif w24:
            tiny_seed_numbers = [2048] * 23 + [1]
        else:
            tiny_seed_numbers = [2048] * 11 + [433]
        self._map_keys_array()
        page = 0
        menu_offset = self.y_offset + 12 * self.y_pad
        while True:
            self._draw_labels(page)
            self._draw_grid()
            if not w24 or page:
                self._draw_disabled(w24)
                tiny_seed_numbers = self._auto_checksum(tiny_seed_numbers)
            self._draw_punched(tiny_seed_numbers, page)
            menu_index = (
                1
                if index >= TS_GO_POSITION
                else (0 if index >= TS_ESC_START_POSITION else None)
            )
            proceed_menu(self.ctx, menu_offset, menu_index, t("Go"), t("Esc"))
            if self.ctx.input.buttons_active:
                self._draw_index(index)
            btn = self.ctx.input.wait_for_button()
            if btn == BUTTON_TOUCH:
                btn = BUTTON_ENTER
                index = self.ctx.input.touch.current_index()
            if btn == BUTTON_ENTER:
                if index > TS_ESC_END_POSITION:  # "Go"
                    if not w24 or (w24 and (page or scanning_24)):
                        if scanning_24:
                            return tiny_seed_numbers
                        return to_words(tiny_seed_numbers)
                    page += 1
                elif index >= TS_ESC_START_POSITION:  # "Esc"
                    self.ctx.display.clear()
                    if self.prompt(t("Are you sure?"), self.ctx.display.height() // 2):
                        break
                    self._map_keys_array()
                elif _editable_bit():
                    word_index = (index // 12) + page * 12
                    bit = 11 - (index % 12)
                    if bit == 11:
                        tiny_seed_numbers[word_index] = 2048
                    else:
                        tiny_seed_numbers[word_index] = (
                            toggle_bit(tiny_seed_numbers[word_index], bit) % 2048
                        )
                    if tiny_seed_numbers[word_index] == 0:
                        tiny_seed_numbers[word_index] = 2048
            index = self._new_index(index, btn, w24, page)
            self.ctx.display.clear()


class TinyScanner(Page):
    """Uses camera sensor to detect punch pattern on a Tiny Seed, in metal or paper"""

    # Settings for different binary grid types
    binary_grid_settings = {
        "Tiny Seed": {
            "xpad_factor": (240 / (12 * 345)),
            "ypad_factor": (210 / (12 * 272)),
            "x_offset_factor_amigo_p0": 39 / 345,
            "y_offset_factor_amigo_p0": 44 / 272,
            "x_offset_factor_amigo_p1": 42 / 345,
            "y_offset_factor_amigo_p1": 41 / 272,
            "x_offset_factor_p0": 65 / 345,
            "y_offset_factor_p0": 17 / 272,
            "x_offset_factor_p1": 62 / 345,
            "y_offset_factor_p1": 22 / 272,
            "aspect_high": 1.3,
            "aspect_low": 1.1,
        },
        "OneKey KeyTag": {
            "xpad_factor": 240 / (12 * 360),
            "ypad_factor": 240 / (12 * 335),
            "x_offset_factor_amigo_p0": 50 / 360,
            "y_offset_factor_amigo_p0": 67 / 335,
            "x_offset_factor_amigo_p1": 50 / 360,
            "y_offset_factor_amigo_p1": 67 / 335,
            "x_offset_factor_p0": 68 / 360,
            "y_offset_factor_p0": 30 / 335,
            "x_offset_factor_p1": 68 / 360,
            "y_offset_factor_p1": 30 / 335,
            "aspect_high": 1.1,
            "aspect_low": 0.9,
        },
        "Binary Grid": {
            "xpad_factor": 1 / 14,
            "ypad_factor": 1 / 14,
            "x_offset_factor_amigo_p0": 1 / 14,
            "y_offset_factor_amigo_p0": 1 / 14,
            "x_offset_factor_amigo_p1": 1 / 14,
            "y_offset_factor_amigo_p1": 1 / 14,
            "x_offset_factor_p0": 1 / 14,
            "y_offset_factor_p0": 1 / 14,
            "x_offset_factor_p1": 1 / 14,
            "y_offset_factor_p1": 1 / 14,
            "aspect_high": 1.3,
            "aspect_low": 0.7,
        },
    }

    grid_settings = None

    def __init__(self, ctx, grid_type="Tiny Seed"):
        super().__init__(ctx, None)
        self.ctx = ctx
        self.capturing = False  # Flag used for first page of 24-word seed
        self.x_regions = []
        self.y_regions = []
        self.time_frame = time.ticks_ms()
        self.previous_seed_numbers = [1] * 12
        self.grid_settings = self.binary_grid_settings[grid_type]
        self.label = t("Binary Grid") if grid_type == "Binary Grid" else grid_type
        self.g_corners = (0x80, 0x80, 0x80, 0x80)
        self.blob_otsu = 0x80
        # Cache board type to avoid repeated lookups.
        self.board_type = board.config.get("type", "")

    def _map_punches_region(self, rect_size, page=0):
        """Calculate x and y coordinates for punched grid regions."""
        self.x_regions = []
        self.y_regions = []
        if self.board_type == "amigo":
            offset_key_x = "x_offset_factor_amigo_p{}".format(page)
            offset_key_y = "y_offset_factor_amigo_p{}".format(page)
        else:
            offset_key_x = "x_offset_factor_p{}".format(page)
            offset_key_y = "y_offset_factor_p{}".format(page)
        x_offset = rect_size[0] + rect_size[2] * self.grid_settings[offset_key_x]
        y_offset = rect_size[1] + rect_size[3] * self.grid_settings[offset_key_y]
        self.x_regions.append(int(x_offset))
        self.y_regions.append(int(y_offset))
        x_pad = rect_size[2] * self.grid_settings["xpad_factor"]
        y_pad = rect_size[3] * self.grid_settings["ypad_factor"]
        for _ in range(12):
            x_offset += x_pad
            y_offset += y_pad
            self.x_regions.append(int(round(x_offset)))
            self.y_regions.append(int(round(y_offset)))

    def _valid_numbers(self, data):
        for n in data:
            if not n or n > 2048:
                return False
        return True

    def _gradient_corners(self, rect, img):
        """Compute histogram thresholds from four corners of the Tiny Seed region."""
        if self.board_type != "amigo":
            region_ul = (
                rect[0] + rect[2] // 8,
                rect[1] + rect[3] // 30,
                rect[2] // 4,
                rect[3] // 4,
            )
            region_ur = (
                rect[0] + 8 * rect[2] // 11,
                rect[1] + rect[3] // 30,
                rect[2] // 4,
                rect[3] // 4,
            )
            region_ll = (
                rect[0] + rect[2] // 8,
                rect[1] + (rect[3] * 5) // 7,
                rect[2] // 4,
                rect[3] // 4,
            )
            region_lr = (
                rect[0] + 8 * rect[2] // 11,
                rect[1] + (rect[3] * 5) // 7,
                rect[2] // 4,
                rect[3] // 4,
            )
        else:  # Amigo has mirrored coordinates
            region_ul = (
                rect[0] + 7 * rect[2] // 11,
                rect[1] + (rect[3] * 5) // 7,
                rect[2] // 4,
                rect[3] // 4,
            )
            region_ur = (
                rect[0] + rect[2] // 30,
                rect[1] + (rect[3] * 5) // 7,
                rect[2] // 4,
                rect[3] // 4,
            )
            region_ll = (
                rect[0] + 7 * rect[2] // 11,
                rect[1] + rect[3] // 8,
                rect[2] // 4,
                rect[3] // 4,
            )
            region_lr = (
                rect[0] + rect[2] // 30,
                rect[1] + rect[3] // 8,
                rect[2] // 4,
                rect[3] // 4,
            )

        # # Debug gradient corners
        # # Warning: These rectangles affect detection
        # img.draw_rectangle(region_ul, color=lcd.YELLOW, thickness=2)
        # img.draw_rectangle(region_ur, color=lcd.ORANGE, thickness=2)
        # img.draw_rectangle(region_ll, color=lcd.RED, thickness=2)
        # img.draw_rectangle(region_lr, color=lcd.MAGENTA, thickness=2)

        # # Debug corners luminosity
        # gradient_bg_ul = img.get_statistics(roi=region_ul).median()
        # gradient_bg_ur = img.get_statistics(roi=region_ur).median()
        # gradient_bg_ll = img.get_statistics(roi=region_ll).median()
        # gradient_bg_lr = img.get_statistics(roi=region_lr).median()
        # img.draw_string(10,40,str(gradient_bg_ul))
        # img.draw_string(70,40,str(gradient_bg_ur))
        # img.draw_string(10,55,str(gradient_bg_ll))
        # img.draw_string(70,55,str(gradient_bg_lr))
        # Compute Otsu threshold for each corner
        try:
            grad_ul = img.get_histogram(roi=region_ul).get_threshold().value()
            grad_ur = img.get_histogram(roi=region_ur).get_threshold().value()
            grad_ll = img.get_histogram(roi=region_ll).get_threshold().value()
            grad_lr = img.get_histogram(roi=region_lr).get_threshold().value()
            self.g_corners = (grad_ul, grad_ur, grad_ll, grad_lr)
        except Exception:
            pass

    def _gradient_value(self, index):
        """Calculate an interpolated threshold from the four corner gradients."""
        grad_ul, grad_ur, grad_ll, grad_lr = self.g_corners
        y_pos = index % 12
        x_pos = index // 12
        gradient_upper = (grad_ul * (11 - x_pos) + grad_ur * x_pos) // 11
        gradient_lower = (grad_ll * (11 - x_pos) + grad_lr * x_pos) // 11
        gradient = (gradient_upper * (11 - y_pos) + gradient_lower * y_pos) // 11
        # Weighted average with the overall corner average:
        filtered = (grad_ul + grad_ur + grad_ll + grad_lr + 6 * gradient) // 10
        return filtered

    def _detect_tiny_seed(self, img):
        """Detect the Tiny Seed region as a bright blob."""
        aspect_low = self.grid_settings["aspect_low"]
        aspect_high = self.grid_settings["aspect_high"]

        def choose_rect(rects):
            best_rect = None
            best_diff = float("inf")
            medium_aspect = (aspect_low + aspect_high) / 2
            for rect in rects:
                if rect[3] == 0:
                    continue
                aspect = rect[2] / rect[3]
                if (
                    rect[0] >= 0
                    and rect[1] >= 0
                    and (rect[0] + rect[2]) < img.width()
                    and (rect[1] + rect[3]) < img.height()
                    and aspect_low < aspect < aspect_high
                ):
                    diff = abs(aspect - medium_aspect)
                    if diff < best_diff:
                        best_diff = diff
                        best_rect = rect
            return best_rect

        try:
            self.blob_otsu = img.get_histogram().get_threshold().value()
        except:
            pass
        blob_threshold = [(self.blob_otsu, 255)]
        blobs = img.find_blobs(
            blob_threshold, x_stride=30, y_stride=30, area_threshold=5000
        )
        # Debug: Optionally draw the blobs to see them during development
        # for blob in blobs:
        #     img.draw_rectangle(blob.rect(), color=(255, 125 * attempts, 0), thickness=3)
        rect = choose_rect([blob.rect() for blob in blobs])
        if rect:
            outline = (rect[0] - 1, rect[1] - 1, rect[2] + 1, rect[3] + 1)
            thickness = 4 if self.capturing else 2
            img.draw_rectangle(outline, lcd.WHITE, thickness=thickness)
        return rect

    def _draw_grid(self, img):
        if self.ctx.display.height() > SMALLEST_HEIGHT:
            for i in range(13):
                img.draw_line(
                    self.x_regions[i],
                    self.y_regions[0],
                    self.x_regions[i],
                    self.y_regions[-1],
                    lcd.WHITE,
                )
                img.draw_line(
                    self.x_regions[0],
                    self.y_regions[i],
                    self.x_regions[-1],
                    self.y_regions[i],
                    lcd.WHITE,
                )

    def _detect_and_draw_punches(self, img):
        """Detect punched bits on the grid and update the seed numbers accordingly."""
        page_seed_numbers = [0] * 12
        index = 0
        pad_x = self.x_regions[1] - self.x_regions[0]
        pad_y = self.y_regions[1] - self.y_regions[0]
        if pad_x < 4 or pad_y < 4:
            return page_seed_numbers

        # Prepare mapping (reverse one axis based on board type)
        y_map = self.y_regions[:-1][:]
        x_map = self.x_regions[:-1][:]
        if self.board_type == "amigo":
            x_map.reverse()
        else:
            y_map.reverse()
        # Think in portrait mode, with Tiny Seed tilted 90 degrees
        # Loop ahead will sweep TinySeed bits/dots and evaluate its luminosity
        for x in x_map:
            for y in y_map:
                eval_rect = (x + 2, y + 2, pad_x - 3, pad_y - 3)
                dot_l = img.get_statistics(roi=eval_rect).median()

                # # Debug gradient
                # if index == 0:
                #     img.draw_string(10,10,"0:"+str(gradient_ref))
                # if index == 11:
                #     img.draw_string(10,25,"11:"+str(gradient_ref))
                # if index == 132:
                #     img.draw_string(70,10,"132:"+str(gradient_ref))
                # if index == 143:
                #     img.draw_string(70,25,"143:"+str(gradient_ref))

                # Defines a threshold to evaluate if the dot is considered punched
                punch_threshold = self._gradient_value(index)
                punch_thickness = (
                    1 if self.ctx.display.height() > SMALLEST_HEIGHT else 2
                )
                if dot_l < punch_threshold:
                    img.draw_rectangle(
                        eval_rect, thickness=punch_thickness, color=lcd.WHITE
                    )
                    word_index = index // 12
                    bit = 11 - (index % 12)
                    page_seed_numbers[word_index] = toggle_bit(
                        page_seed_numbers[word_index], bit
                    )
                index += 1
        return page_seed_numbers

    def _run_camera(self):
        """Turns camera on and rotates screen to landscape"""
        sensor.run(1)
        self.ctx.display.clear()
        self.ctx.display.to_landscape()

    def _exit_camera(self):
        sensor.run(0)
        self.ctx.display.to_portrait()
        self.ctx.display.clear()

    def _check_buttons(self, w24, page):
        if self.ctx.input.enter_event() or self.ctx.input.touch_event(
            validate_position=False
        ):
            if w24 and page == 0:
                self.capturing = True
            else:
                return True
        if self.ctx.input.page_event() or self.ctx.input.page_prev_event():
            return True
        return False

    def _process_12w_scan(self, page_seed_numbers):
        if not self._valid_numbers(page_seed_numbers):
            return None
        if check_sum_bg(page_seed_numbers) == (
            (page_seed_numbers[11] - 1) & 0b00000001111
        ):
            if page_seed_numbers == self.previous_seed_numbers:
                self._exit_camera()
                self.ctx.display.draw_centered_text(
                    t("Review scanned data, edit if necessary")
                )
                self.ctx.input.wait_for_button()
                self.ctx.display.clear()
                words = TinySeed(self.ctx, label=self.label).enter_tiny_seed(
                    seed_numbers=page_seed_numbers
                )
                if words:
                    return words
                self.flash_text(
                    t("Scanning words 1-12 again") + "\n\n" + t("Wait for the capture")
                )
                self._run_camera()
                self.previous_seed_numbers = [1] * 12
            else:
                self.previous_seed_numbers = page_seed_numbers
        return None

    def _process_24w_pg0_scan(self, page_seed_numbers):
        if page_seed_numbers == self.previous_seed_numbers and self.capturing:
            self.ctx.input.reset_ios_state()
            self._exit_camera()
            self.ctx.display.draw_centered_text(
                t("Review scanned data, edit if necessary")
            )
            self.ctx.input.wait_for_button()
            self.ctx.display.clear()
            words = TinySeed(self.ctx, label=self.label).enter_tiny_seed(
                True, page_seed_numbers, True
            )
            self.capturing = False
            if words is not None:
                self.flash_text(
                    t("Scanning words 13-24") + "\n\n" + t("Wait for the capture")
                )
                self._run_camera()
                return words
            # Esc command was given
            self.flash_text(
                t("Scanning words 1-12 again") + "\n\n" + t("TOUCH or ENTER to capture")
            )
            self._run_camera()
        elif self._valid_numbers(page_seed_numbers):
            self.previous_seed_numbers = page_seed_numbers
        return None

    def scanner(self, w24=False):
        """Scans the Tiny Seed using the camera sensor."""
        page = 0
        if w24:
            w24_seed_numbers = [0] * 24
        self.previous_seed_numbers = [1] * 12

        self.ctx.display.clear()
        message = (
            t("TOUCH or ENTER to capture")
            if (w24 and page == 0)
            else t("Wait for the capture")
        )
        self.ctx.display.draw_centered_text(message)
        precamera_ticks = time.ticks_ms()
        self.ctx.camera.initialize_run(mode=BINARY_GRID_MODE)
        self.ctx.camera.zoom_mode()
        self.ctx.display.to_landscape()
        postcamera_ticks = time.ticks_ms()
        delay = precamera_ticks + FLASH_MSG_TIME - postcamera_ticks
        if delay > 0:
            time.sleep_ms(delay)
        self.ctx.input.reset_ios_state()
        self.ctx.display.clear()

        while True:
            wdt.feed()
            page_seed_numbers = None
            img = self.ctx.camera.snapshot()
            rect = self._detect_tiny_seed(img)
            if rect:
                self._gradient_corners(rect, img)
                self._map_punches_region(rect, page)
                page_seed_numbers = self._detect_and_draw_punches(img)
                self._draw_grid(img)
            if self.board_type == "m5stickv":
                img.lens_corr(strength=1.0, zoom=0.56)
            if self.board_type == "amigo":
                lcd.display(img, oft=(80, 40))
            else:
                lcd.display(img)
            if page_seed_numbers:
                if w24:
                    if page == 0:
                        first_page = self._process_24w_pg0_scan(page_seed_numbers)
                        if first_page:
                            w24_seed_numbers[0:12] = first_page
                            page = 1
                    else:
                        w24_seed_numbers[12:24] = page_seed_numbers
                        if check_sum_bg(w24_seed_numbers) == (
                            (w24_seed_numbers[23] - 1) & 0b00011111111
                        ):
                            if page_seed_numbers == self.previous_seed_numbers:
                                self._exit_camera()
                                return to_words(w24_seed_numbers)
                            self.previous_seed_numbers = page_seed_numbers
                else:
                    words = self._process_12w_scan(page_seed_numbers)
                    if words:
                        return words
            if self._check_buttons(w24, page):
                break

        self._exit_camera()
        return None


def toggle_bit(word, bit):
    """Toggle bit state according to pressed index"""
    return word ^ (1 << bit)


def to_words(tiny_seed_numbers):
    """Converts a list of numbers 1-2048 to a list of respective BIP39 words"""
    return [WORDLIST[num - 1] for num in tiny_seed_numbers]


def check_sum_bg(tiny_seed_numbers):
    """Dinamically calculates checksum of binary grid"""
    total_bits = len(tiny_seed_numbers) * 11
    # Calculate the number of checksum bits.
    checksum_length = total_bits // 33

    # Accumulate the bits from the Binary Grid words.
    acc = 0
    for n in tiny_seed_numbers:
        if not n:
            raise ValueError("Invalid Binary Grid number")
        # Subtract 1 because Binary Grid values are 1-indexed.
        acc = (acc << 11) | (n - 1)

    # The bitstream is: [entropy bits][checksum bits]
    # Remove the checksum bits by right-shifting.
    entropy_int = acc >> checksum_length
    entropy_bytes_count = 16 if checksum_length == 4 else 32
    data = entropy_int.to_bytes(entropy_bytes_count, "big")

    return entropy_checksum(data, checksum_length)
