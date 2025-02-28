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

import qrcode
from embit.wordlists.bip39 import WORDLIST
from . import Page, Menu, MENU_CONTINUE, MENU_EXIT, ESC_KEY
from ..themes import theme, WHITE, BLACK, DARKGREY
from ..krux_settings import t
from ..settings import THIN_SPACE
from ..qr import get_size
from ..display import DEFAULT_PADDING, FONT_HEIGHT, NARROW_SCREEN_WITH
from ..input import (
    BUTTON_ENTER,
    BUTTON_PAGE,
    BUTTON_PAGE_PREV,
    BUTTON_TOUCH,
    SWIPE_DOWN,
    SWIPE_RIGHT,
    SWIPE_LEFT,
    SWIPE_UP,
)

STANDARD_MODE = 0
LINE_MODE = 1
ZOOMED_R_MODE = 2
REGION_MODE = 3
TRANSCRIBE_MODE = 4


class SeedQRView(Page):
    """Tools to visualize and transcript Seed QRs"""

    def __init__(self, ctx, binary=False, data=None, title=None):
        super().__init__(ctx, None)
        self.ctx = ctx
        self.binary = binary
        if data:
            self.code = qrcode.encode(data)  # pylint: disable=E1101
            self.title = title
        else:
            if self.binary:
                self.title = "Compact SeedQR"
                self.code = self._binary_seed_qr()
            else:
                self.title = "SeedQR"
                self.code = self._seed_qr()
        self.qr_size = get_size(self.code)
        self.region_size = 7 if self.qr_size == 21 else 5
        self.columns = (self.qr_size + self.region_size - 1) // self.region_size
        self.lr_index = 0
        if theme.bg_color == WHITE:
            self.qr_foreground = WHITE
        else:
            self.qr_foreground = None

    def _seed_qr(self):
        words = self.ctx.wallet.key.mnemonic.split(" ")
        numbers = ""
        for word in words:
            numbers += str("%04d" % WORDLIST.index(word))
        return qrcode.encode(numbers)  # pylint: disable=E1101

    def _binary_seed_qr(self):
        binary_seed = self._to_compact_seed_qr(self.ctx.wallet.key.mnemonic)
        return qrcode.encode(binary_seed)  # pylint: disable=E1101

    def _to_compact_seed_qr(self, mnemonic):
        mnemonic = mnemonic.split(" ")
        checksum_bits = 8 if len(mnemonic) == 24 else 4
        indexes = [WORDLIST.index(word) for word in mnemonic]
        bitstring = "".join(["{:0>11}".format(bin(index)[2:]) for index in indexes])[
            :-checksum_bits
        ]
        return int(bitstring, 2).to_bytes((len(bitstring) + 7) // 8, "big")

    def highlight_qr_region(self, code, region=(0, 0, 0, 0), zoom=False):
        """Draws in white a highlighted region of the QR code"""
        reg_x, reg_y, reg_width, reg_height = region
        max_width = self.ctx.display.width()
        if zoom:
            max_width -= DEFAULT_PADDING
            if self.qr_size == 21:
                qr_size = 7
            else:
                qr_size = 5
            offset_x = 0
            offset_y = 0
            scale = max_width // qr_size
        else:
            qr_size = self.qr_size
            offset_x = reg_x
            offset_y = reg_y
            scale = max_width // (qr_size + 2)
        qr_width = qr_size * scale
        offset = (self.ctx.display.width() - qr_width) // 2
        for y in range(reg_height):  # vertical blocks loop
            for x in range(reg_width):  # horizontal blocks loop
                y_index = reg_y + y
                x_index = reg_x + x
                xy_index = y_index * self.qr_size
                xy_index += x_index
                if y_index < self.qr_size and x_index < self.qr_size:
                    bit_value = code[xy_index >> 3] & (1 << (xy_index % 8))
                    if bit_value:
                        self.ctx.display.fill_rectangle(
                            offset + (offset_x + x) * scale,
                            offset + (offset_y + y) * scale,
                            scale,
                            scale,
                            BLACK,
                        )
                    else:
                        self.ctx.display.fill_rectangle(
                            offset + (offset_x + x) * scale,
                            offset + (offset_y + y) * scale,
                            scale,
                            scale,
                            WHITE,
                        )

    def _region_legend(self, row, column):
        region_char = chr(65 + row)
        self.ctx.display.draw_hcentered_text(
            t("Region:") + " " + region_char + str(column + 1),
            self.ctx.display.qr_offset(),
            color=theme.highlight_color,
        )

    def draw_grided_qr(self, mode):
        """Draws grided QR"""
        self.ctx.display.clear()
        if self.ctx.display.width() > NARROW_SCREEN_WITH:
            grid_size = self.ctx.display.width() // NARROW_SCREEN_WITH
        else:
            grid_size = 1
        grid_offset = self.ctx.display.width() % (self.qr_size + 2)
        grid_offset //= 2
        grid_pad = self.ctx.display.width() // (self.qr_size + 2)
        grid_offset += grid_pad
        if mode == STANDARD_MODE:
            if self.qr_foreground:
                self.ctx.display.draw_qr_code(
                    0, self.code, light_color=self.qr_foreground
                )
            else:
                self.ctx.display.draw_qr_code(0, self.code)
        elif mode == LINE_MODE:
            self.ctx.display.draw_qr_code(
                0, self.code, light_color=theme.disabled_color
            )
            self.highlight_qr_region(
                self.code, region=(0, self.lr_index, self.qr_size, 1)
            )
            line_offset = grid_pad * self.lr_index
            for i in range(2):
                self.ctx.display.fill_rectangle(
                    grid_offset,
                    grid_offset + i * grid_pad + line_offset,
                    self.qr_size * grid_pad + 1,
                    grid_size,
                    theme.highlight_color,
                )
            for i in range(self.qr_size + 1):
                self.ctx.display.fill_rectangle(
                    grid_offset + i * grid_pad,
                    grid_offset + line_offset,
                    grid_size,
                    grid_pad + 1,
                    theme.highlight_color,
                )
            self.ctx.display.draw_hcentered_text(
                t("Line:") + " " + str(self.lr_index + 1),
                self.ctx.display.qr_offset(),
                color=theme.highlight_color,
            )
        elif mode == ZOOMED_R_MODE:
            max_width = self.ctx.display.width() - DEFAULT_PADDING
            zoomed_grid_pad = max_width // self.region_size
            zoomed_grid_offset = (
                self.ctx.display.width() - self.region_size * zoomed_grid_pad
            )
            zoomed_grid_offset //= 2
            row = self.lr_index // self.columns
            column = self.lr_index % self.columns
            self.highlight_qr_region(
                self.code,
                region=(
                    column * self.region_size,
                    (row) * self.region_size,
                    self.region_size,
                    self.region_size,
                ),
                zoom=True,
            )
            for i in range(self.region_size + 1):
                self.ctx.display.fill_rectangle(
                    zoomed_grid_offset,
                    zoomed_grid_offset + i * zoomed_grid_pad,
                    self.region_size * zoomed_grid_pad + 1,
                    grid_size,
                    theme.highlight_color,
                )
            for i in range(self.region_size + 1):
                self.ctx.display.fill_rectangle(
                    zoomed_grid_offset + i * zoomed_grid_pad,
                    zoomed_grid_offset,
                    grid_size,
                    self.region_size * zoomed_grid_pad + 1,
                    theme.highlight_color,
                )
            self._region_legend(row, column)
        elif mode == REGION_MODE:
            row = self.lr_index // self.columns
            column = self.lr_index % self.columns
            self.ctx.display.draw_qr_code(
                0, self.code, light_color=theme.disabled_color
            )
            self.highlight_qr_region(
                self.code,
                region=(
                    column * self.region_size,
                    (row) * self.region_size,
                    self.region_size,
                    self.region_size,
                ),
            )
            line_offset = grid_pad * row * self.region_size
            column_offset = grid_pad * column * self.region_size
            draw_limit = grid_offset + self.qr_size * grid_pad
            for i in range(self.region_size + 1):
                x_position = grid_offset + column_offset
                x_length = self.region_size * grid_pad + 1
                transposed = x_position + x_length - draw_limit
                if transposed > 0:
                    x_length -= transposed
                y_position = grid_offset + i * grid_pad + line_offset
                if y_position > draw_limit:
                    break
                self.ctx.display.fill_rectangle(
                    x_position,
                    y_position,
                    x_length,
                    grid_size,
                    theme.highlight_color,
                )
            for i in range(self.region_size + 1):
                x_position = grid_offset + i * grid_pad + column_offset
                if x_position > draw_limit:
                    break
                y_position = grid_offset + line_offset
                y_length = self.region_size * grid_pad + 1
                transposed = y_position + y_length - draw_limit
                if transposed > 0:
                    y_length -= transposed
                self.ctx.display.fill_rectangle(
                    x_position,
                    y_position,
                    grid_size,
                    y_length,
                    theme.highlight_color,
                )
            self._region_legend(row, column)
        else:  #  TRANSCRIBE_MODE
            self.ctx.display.draw_qr_code(0, self.code, light_color=WHITE)
            for i in range(self.qr_size + 1):
                self.ctx.display.fill_rectangle(
                    grid_offset,
                    grid_offset + i * grid_pad,
                    self.qr_size * grid_pad + 1,
                    grid_size,
                    theme.highlight_color,
                )
                self.ctx.display.fill_rectangle(
                    grid_offset + i * grid_pad,
                    grid_offset,
                    grid_size,
                    self.qr_size * grid_pad + 1,
                    theme.highlight_color,
                )

    def add_frame(self, binary_image, size):
        """Adds a 1 block frame to QR codes"""
        new_size = size + 2
        # Create a new bytearray to store the framed image
        framed_image = bytearray(b"\x00" * ((new_size * new_size + 7) >> 3))
        # Copy the original image into the center of the framed image
        for y in range(0, size):
            for x in range(0, size):
                original_index = y * size + x
                original_bit = (
                    binary_image[original_index >> 3] >> (original_index % 8)
                ) & 1
                if original_bit:
                    framed_index = (y + 1) * new_size + x + 1
                    framed_image[framed_index >> 3] |= 1 << (framed_index % 8)

        return framed_image, new_size

    def save_pbm_image(self, file_name):
        """Saves QR code image as compact B&W bitmap format file"""
        from ..sd_card import PBM_IMAGE_EXTENSION
        from .file_operations import SaveFile

        code, size = self.add_frame(self.code, self.qr_size)
        pbm_data = bytearray()
        pbm_data.extend(("P4\n{0} {0}\n".format(size)).encode())
        for row in range(size):
            byte = 0
            for col in range(size):
                bit_index = row * size + col
                if code[bit_index >> 3] & (1 << (bit_index % 8)):
                    byte |= 1 << (7 - (col % 8))

                # If we filled a byte or reached the end of the row, append it
                if col % 8 == 7 or col == size - 1:
                    pbm_data.append(byte)
                    byte = 0

        save_page = SaveFile(self.ctx)
        save_page.save_file(
            pbm_data,
            file_name,
            file_extension=PBM_IMAGE_EXTENSION,
            save_as_binary=True,
            prompt=False,
        )

    def save_bmp_image(self, file_name, resolution):
        """Save QR code image as .bmp file"""
        from ..sd_card import BMP_IMAGE_EXTENSION
        from .file_operations import SaveFile

        import image
        import lcd

        code, size = self.add_frame(self.code, self.qr_size)
        raw_image = image.Image(size=(size, size))
        for y_index in range(0, size):
            for x_index in range(0, size):
                index = y_index * size + x_index
                bit_value = (code[index >> 3] >> (index % 8)) & 1
                if bit_value:
                    raw_image.set_pixel((x_index, y_index), lcd.BLACK)
                else:
                    raw_image.set_pixel((x_index, y_index), lcd.WHITE)
        bmp_img = image.Image(size=(resolution, resolution), copy_to_fb=True)
        scale = resolution // size
        bmp_img.draw_image(
            raw_image,
            0,
            0,
            x_scale=scale,
            y_scale=scale,
        )
        save_page = SaveFile(self.ctx)
        file_name = save_page.set_filename(
            file_name, file_extension=BMP_IMAGE_EXTENSION
        )
        if file_name == ESC_KEY:
            return

        self.ctx.display.clear()
        self.ctx.display.draw_centered_text(t("Processing.."))

        bmp_img.save("/sd/" + file_name)
        self.flash_text(t("Saved to SD card") + ":\n%s" % file_name)

    def save_qr_image_menu(self):
        """Options to save QR codes as images on SD card"""

        # Replaces spaces and thin spaces
        suggested_file_name = self.title.replace(" ", "_").replace(THIN_SPACE, "_")
        if len(suggested_file_name) > 10:  # Crop file name
            suggested_file_name = suggested_file_name[:10]

        size = self.qr_size + 2
        bmp_resolutions = []
        resolution = size
        for _ in range(4):
            resolution *= 2
            if resolution <= 480:
                bmp_resolutions.append(resolution)
        self.ctx.display.clear()
        self.ctx.display.draw_hcentered_text(
            t("Res. - Format"), FONT_HEIGHT, info_box=True
        )
        qr_menu = []
        qr_menu.append(
            (
                "%dx%d - PBM" % (size, size),
                lambda: self.save_pbm_image(suggested_file_name),
            )
        )
        for bmp_resolution in bmp_resolutions:
            qr_menu.append(
                (
                    "%dx%d - BMP" % (bmp_resolution, bmp_resolution),
                    lambda res=bmp_resolution: self.save_bmp_image(
                        suggested_file_name, res
                    ),
                )
            )
        submenu = Menu(self.ctx, qr_menu, offset=2 * FONT_HEIGHT, back_label=None)
        submenu.run_loop()
        return MENU_CONTINUE
        # return MENU_EXIT  # Use this to exit QR Viewer after saving

    def print_qr(self):
        "Printer handler"
        from .utils import Utils

        utils = Utils(self.ctx)
        title = self.title.replace(THIN_SPACE, " ")  # Replaces thin spaces
        utils.print_standard_qr(self.code, title=title, is_qr=True)
        # return MENU_EXIT  # Uncomment to exit QR Viewer after printing

    def display_qr(self, allow_export=False, transcript_tools=True, quick_exit=False):
        """Displays QR codes in multiple modes"""

        if self.title:
            label = self.title
        else:
            label = ""
        if transcript_tools and self.ctx.input.touch is not None:
            label += "\n" + t("Swipe to change mode")
        mode = 0
        while True:
            button = None
            while button not in (SWIPE_DOWN, SWIPE_UP):

                def toggle_brightness():
                    if self.qr_foreground == WHITE:
                        self.qr_foreground = DARKGREY
                    elif self.qr_foreground is None:
                        self.qr_foreground = WHITE
                    else:
                        self.qr_foreground = None

                self.draw_grided_qr(mode)
                if self.ctx.display.height() > self.ctx.display.width():
                    self.ctx.display.draw_hcentered_text(
                        label,
                        self.ctx.display.qr_offset() + FONT_HEIGHT,
                    )
                button = self.ctx.input.wait_for_button()
                if transcript_tools:
                    if button in (BUTTON_PAGE, SWIPE_LEFT):  # page, swipe
                        mode += 1
                        mode %= 5
                        self.lr_index = 0
                    elif button in (BUTTON_PAGE_PREV, SWIPE_RIGHT):  # page, swipe
                        mode -= 1
                        mode %= 5
                        self.lr_index = 0
                elif button == BUTTON_PAGE:
                    toggle_brightness()
                if button in (BUTTON_ENTER, BUTTON_TOUCH):
                    if mode in (LINE_MODE, REGION_MODE, ZOOMED_R_MODE):
                        self.lr_index += 1
                    else:
                        if not (button == BUTTON_TOUCH and mode == TRANSCRIBE_MODE):
                            button = SWIPE_DOWN  # leave
                if mode == LINE_MODE:
                    self.lr_index %= self.qr_size
                elif mode in (REGION_MODE, ZOOMED_R_MODE):
                    self.lr_index %= self.columns * self.columns
            if quick_exit:
                return MENU_CONTINUE
            printer_func = self.print_qr if self.has_printer() else None
            qr_menu = [
                (t("Return to QR Viewer"), lambda: None),
                (t("Toggle Brightness"), toggle_brightness),
                (
                    t("Save QR Image to SD Card"),
                    (
                        self.save_qr_image_menu
                        if allow_export and self.has_sd_card()
                        else None
                    ),
                ),
                (t("Print to QR"), printer_func),
            ]
            submenu = Menu(self.ctx, qr_menu, back_label=t("Back to Menu"))
            _, status = submenu.run_loop()
            if status == MENU_EXIT:
                return MENU_CONTINUE
