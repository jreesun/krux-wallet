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
import lcd
import board
import time
from .themes import theme
from .krux_settings import Settings
from .settings import THIN_SPACE

DEFAULT_PADDING = 10
MINIMAL_PADDING = 5
FONT_WIDTH, FONT_HEIGHT = board.config["krux"]["display"]["font"]
FONT_WIDTH_WIDE, FONT_HEIGHT_WIDE = board.config["krux"]["display"]["font_wide"]
PORTRAIT, LANDSCAPE = [2, 3] if board.config["type"] == "cube" else [1, 2]
QR_DARK_COLOR, QR_LIGHT_COLOR = (
    [16904, 61307] if board.config["type"] == "m5stickv" else [0, 6342]
)
TOTAL_LINES = board.config["lcd"]["width"] // FONT_HEIGHT
BOTTOM_LINE = (TOTAL_LINES - 1) * FONT_HEIGHT
MINIMAL_DISPLAY = board.config["type"] in ("m5stickv", "cube")
if MINIMAL_DISPLAY:
    BOTTOM_PROMPT_LINE = BOTTOM_LINE - DEFAULT_PADDING
else:
    # room left for no/yes buttons
    BOTTOM_PROMPT_LINE = BOTTOM_LINE - 3 * FONT_HEIGHT

# Status bar dimensions
STATUS_BAR_HEIGHT = (
    FONT_HEIGHT + 1 if MINIMAL_DISPLAY else FONT_HEIGHT + MINIMAL_PADDING
)

FLASH_MSG_TIME = 2000

NARROW_SCREEN_WITH = 135
SMALLEST_HEIGHT = 240

# Splash will use horizontally-centered text plots. Uses Thin spaces to help with alignment
SPLASH = [
    "██" + THIN_SPACE * 3,
    "██" + THIN_SPACE * 3,
    "██" + THIN_SPACE * 3,
    "██████" + THIN_SPACE * 3,
    "██" + THIN_SPACE * 3,
    THIN_SPACE + "██" + THIN_SPACE * 2 + "██",
    "██" + THIN_SPACE + "██",
    "████" + THIN_SPACE,
    "██" + THIN_SPACE + "██",
    THIN_SPACE + "██" + THIN_SPACE * 2 + "██",
    THIN_SPACE * 2 + "██" + THIN_SPACE * 3 + "██",
]


class Display:
    """Display is a singleton interface for interacting with the device's display"""

    def __init__(self):
        self.portrait = False
        if board.config["type"] == "amigo":
            self.flipped_x_coordinates = (
                Settings().hardware.display.flipped_x_coordinates
            )
        else:
            self.flipped_x_coordinates = False
        self.blk_ctrl = None
        if "BACKLIGHT" in board.config["krux"]["pins"]:
            self.gpio_backlight_ctrl(Settings().hardware.display.brightness)

    def initialize_lcd(self):
        """Initializes the LCD"""
        if board.config["lcd"]["lcd_type"] == 3:
            lcd.init(type=board.config["lcd"]["lcd_type"])
            lcd.register(0x3A, 0x05)
            lcd.register(0xB2, [0x05, 0x05, 0x00, 0x33, 0x33])
            lcd.register(0xB7, 0x23)
            lcd.register(0xBB, 0x22)
            lcd.register(0xC0, 0x2C)
            lcd.register(0xC2, 0x01)
            lcd.register(0xC3, 0x13)
            lcd.register(0xC4, 0x20)
            lcd.register(0xC6, 0x0F)
            lcd.register(0xD0, [0xA4, 0xA1])
            lcd.register(0xD6, 0xA1)
            lcd.register(
                0xE0,
                [
                    0x23,
                    0x70,
                    0x06,
                    0x0C,
                    0x08,
                    0x09,
                    0x27,
                    0x2E,
                    0x34,
                    0x46,
                    0x37,
                    0x13,
                    0x13,
                    0x25,
                    0x2A,
                ],
            )
            lcd.register(
                0xE1,
                [
                    0x70,
                    0x04,
                    0x08,
                    0x09,
                    0x07,
                    0x03,
                    0x2C,
                    0x42,
                    0x42,
                    0x38,
                    0x14,
                    0x14,
                    0x27,
                    0x2C,
                ],
            )
            self.set_pmu_backlight(Settings().hardware.display.brightness)
        elif board.config["type"] in ["yahboom", "wonder_mv"]:
            lcd.init(
                invert=True,
                rst=board.config["lcd"]["rst"],
                dcx=board.config["lcd"]["dcx"],
                ss=board.config["lcd"]["ss"],
                clk=board.config["lcd"]["clk"],
            )
        elif board.config["type"] == "cube":
            lcd.init(
                invert=True,
                offset_h0=80,
            )
        elif board.config["type"] == "amigo":
            lcd_type = Settings().hardware.display.lcd_type
            invert = Settings().hardware.display.inverted_colors
            bgr_to_rgb = Settings().hardware.display.bgr_colors
            lcd.init(invert=invert, lcd_type=lcd_type)
            lcd.mirror(True)
            lcd.bgr_to_rgb(bgr_to_rgb)
        else:
            lcd.init(invert=False)
            lcd.mirror(False)
            lcd.bgr_to_rgb(False)
        self.to_portrait()

    def gpio_backlight_ctrl(self, brightness):
        """Control backlight using GPIO PWM"""

        if self.blk_ctrl is None:
            from machine import Timer, PWM

            pwm_timer = Timer(Timer.TIMER0, Timer.CHANNEL0, mode=Timer.MODE_PWM)
            self.blk_ctrl = PWM(
                pwm_timer,
                freq=1000,
                duty=100,
                pin=board.config["krux"]["pins"]["BACKLIGHT"],
                enable=True,
            )
        # Calculate duty cycle
        if board.config["type"] == "cube":
            # Ranges from 80% to 0% duty cycle
            # 100 is 0% duty cycle (off, not used here)
            pwm_value = 5 - int(brightness)
        else:
            # Ranges from 20% to 100% duty cycle
            pwm_value = int(brightness)
        pwm_value *= 20
        self.blk_ctrl.duty(pwm_value)

    def qr_offset(self):
        """Retuns y offset to subtitle QR codes"""
        if board.config["type"] == "cube":
            return BOTTOM_LINE
        return self.width() + MINIMAL_PADDING

    def width(self):
        """Returns the width of the display, taking into account rotation"""
        if self.portrait:
            return lcd.width()
        return lcd.height()

    def usable_width(self):
        """Returns available width considering side padding"""
        return self.width() - 2 * DEFAULT_PADDING

    def height(self):
        """Returns the height of the display, taking into account rotation"""
        if self.portrait:
            return lcd.height()
        return lcd.width()

    def qr_data_width(self):
        """Returns a smaller width for the QR to be generated
        within, which will then be scaled up to fit the display's width.
        We do this because the QR would be too dense to be readable
        by most devices otherwise.
        """
        if self.width() > 300:
            return self.width() // 6  # reduce density even more on larger screens
        if self.width() > 200:
            return self.width() // 5
        return self.width() // 4

    def to_landscape(self):
        """Changes the rotation of the display to landscape"""
        if self.portrait:
            lcd.rotation(
                (LANDSCAPE + 2) % 4
                if hasattr(Settings().hardware, "display")
                and getattr(Settings().hardware.display, "flipped_orientation", False)
                else LANDSCAPE
            )
            self.portrait = False

    def to_portrait(self):
        """Changes the rotation of the display to portrait"""
        if not self.portrait:
            lcd.rotation(
                (PORTRAIT + 2) % 4
                if hasattr(Settings().hardware, "display")
                and getattr(Settings().hardware.display, "flipped_orientation", False)
                else PORTRAIT
            )
            self.portrait = True

    def to_lines(self, text, max_lines=None):
        """Takes a string of text and converts it to lines to display on
        the screen
        """
        lines = []
        start = 0
        line_count = 0
        columns = (
            self.usable_width() if self.width() > NARROW_SCREEN_WITH else self.width()
        )
        if Settings().i18n.locale in [
            "ko-KR",
            "zh-CN",
            "ja-JP",
        ] and lcd.string_has_wide_glyph(text):
            columns //= FONT_WIDTH_WIDE
        else:
            columns //= FONT_WIDTH

        # Quick return if content fits in one line
        if len(text) <= columns and "\n" not in text:
            return [text]

        if not max_lines:
            max_lines = TOTAL_LINES

        while start < len(text) and line_count < max_lines:
            # Find the next line break, if any
            line_break = text.find("\n", start)
            if line_break == -1:
                next_break = len(text)
            else:
                next_break = min(line_break, len(text))

            end = start + columns
            # If next segment fits on one line, add it and continue
            if end >= next_break:
                lines.append(text[start:next_break].rstrip())
                start = next_break + 1
                line_count += 1
                continue

            # If the end of the line is in the middle of a word,
            # move the end back to the end of the previous word
            if text[end] != " " and text[end] != "\n":
                end = text.rfind(" ", start, end)

            # If there is no space, force break the word
            if end == -1 or end < start:
                end = start + columns

            lines.append(text[start:end].rstrip())
            # don't jump space if we're breaking a word
            jump_space = 1 if text[end] == " " else 0
            start = end + jump_space
            line_count += 1

        # Replace last line with ellipsis if we didn't finish the text
        if line_count == max_lines and start < len(text):
            lines[-1] = lines[-1][: columns - 3] + "..."

        return lines

    def clear(self):
        """Clears the display"""
        lcd.clear(theme.bg_color)

    def outline(self, x, y, width, height, color=theme.fg_color):
        """Draws an outline rectangle from given coordinates"""
        if self.flipped_x_coordinates:
            x = self.width() - x - 1
            x -= width
        lcd.draw_outline(x, y, width, height, color)

    def fill_rectangle(self, x, y, width, height, color, radius=0):
        """Draws a rectangle to the screen with optional rounded corners"""
        if self.flipped_x_coordinates:
            x = self.width() - x
            x -= width
        lcd.fill_rectangle(x, y, width, height, color, radius)

    def draw_line(self, x_0, y_0, x_1, y_1, color=theme.fg_color):
        """Draws a line to the screen"""
        if self.flipped_x_coordinates:
            if x_0 < self.width():
                x_0 += 1
            if x_1 < self.width():
                x_1 += 1
            x_start = self.width() - x_1
            x_end = self.width() - x_0
        else:
            x_start = x_0
            x_end = x_1
        lcd.draw_line(x_start, y_0, x_end, y_1, color)

    def draw_hline(self, x, y, width, color=theme.fg_color):
        """Draws a horizontal line to the screen"""
        self.draw_line(x, y, x + width, y, color)

    def draw_vline(self, x, y, height, color=theme.fg_color):
        """Draws a vertical line to the screen"""
        self.draw_line(x, y, x, y + height, color)

    def fill_circle(self, x, y, radius, quadrant=0, color=theme.fg_color):
        """
        Fills a circle to the screen.
        quadrant=0 will draw all 4 quadrants.
        1 is top right, 2 is top left, 3 is bottom left, 4 is bottom right.
        """
        if self.flipped_x_coordinates:
            x = self.width() - x
        lcd.draw_circle(x, y, radius, quadrant, color)

    def draw_string(self, x, y, text, color=theme.fg_color, bg_color=theme.bg_color):
        """Draws a string to the screen"""
        if self.flipped_x_coordinates:
            x = self.width() - x
            x -= lcd.string_width_px(text)
            x = max(0, x)
        lcd.draw_string(x, y, text, color, bg_color)

    def draw_hcentered_text(
        self,
        text,
        offset_y=DEFAULT_PADDING,
        color=theme.fg_color,
        bg_color=theme.bg_color,
        info_box=False,
        max_lines=None,
    ) -> int:
        """Draws text horizontally-centered on the display, at the given offset_y"""
        lines = (
            text if isinstance(text, list) else self.to_lines(text, max_lines=max_lines)
        )
        if info_box:
            bg_color = theme.info_bg_color
            padding = (
                DEFAULT_PADDING
                if self.width() > NARROW_SCREEN_WITH
                else MINIMAL_PADDING
            )
            self.fill_rectangle(
                padding - 3,
                offset_y - 1,
                self.width() - (2 * padding) + 6,
                (len(lines)) * FONT_HEIGHT + 2,
                bg_color,
                FONT_WIDTH,  # radius
            )

        for i, line in enumerate(lines):
            if len(line) > 0:
                offset_x = max(0, (self.width() - lcd.string_width_px(line)) // 2)
                self.draw_string(
                    offset_x,
                    offset_y + (i * (FONT_HEIGHT)),
                    line,
                    color,
                    bg_color,
                )
        return len(lines)  # return number of lines drawn

    def draw_centered_text(self, text, color=theme.fg_color, bg_color=theme.bg_color):
        """Draws text horizontally and vertically centered on the display"""
        lines = text if isinstance(text, list) else self.to_lines(text)
        lines_height = len(lines) * FONT_HEIGHT
        offset_y = max(0, (self.height() - lines_height) // 2)
        self.draw_hcentered_text(text, offset_y, color, bg_color)

    def flash_text(self, text, color=theme.fg_color, duration=FLASH_MSG_TIME):
        """Flashes text centered on the display for duration ms"""
        self.clear()
        self.draw_centered_text(text, color)
        time.sleep_ms(duration)
        self.clear()

    def draw_qr_code(
        self, offset_y, qr_code, dark_color=QR_DARK_COLOR, light_color=QR_LIGHT_COLOR
    ):
        """Draws a QR code on the screen"""
        lcd.draw_qr_code_binary(
            offset_y, qr_code, self.width(), dark_color, light_color, light_color
        )

    def set_pmu_backlight(self, level):
        """Sets the backlight of the display to the given power level, from 0 to 8"""

        from .power import power_manager

        # Translate 5 levels to 1-8 range = 1,2,3,5,8
        translated_level = int(level)
        if translated_level == 4:
            translated_level = 5
        elif translated_level == 5:
            translated_level = 8
        power_manager.set_screen_brightness(translated_level)

    def max_menu_lines(self, line_offset=STATUS_BAR_HEIGHT):
        """Maximum menu items the display can fit"""
        return (self.height() - line_offset) // (2 * FONT_HEIGHT)

    def render_image(self, img, title_lines=0, double_subtitle=False):
        """Renders the image based on the board type."""
        board_type = board.config["type"]

        # Initialize offset and region components
        offset_x, offset_y = 0, 0
        region_x, region_y, region_w, region_h = 8, 0, 304, 240

        if board_type == "amigo":
            offset_x = 40 if self.flipped_x_coordinates else 120
            offset_y = 40
            region_x, region_y, region_w, region_h = 0, 0, 320, 240
        elif board_type == "m5stickv":
            # Apply lens correction and update img reference
            img = img.lens_corr(strength=1.0, zoom=0.56)
            region_x, region_y, region_w, region_h = 68, 52, 185, 135
        elif board_type == "cube":
            region_x, region_y, region_w, region_h = 48, 0, 224, 240

        # Adjust for title if needed for boards with height < 320px
        if title_lines and board_type != "amigo":
            message_height = DEFAULT_PADDING + FONT_HEIGHT * title_lines
            offset_x += message_height
            region_x += message_height
            region_w -= message_height
            # Adjust bottom padding for double subtitle
            if double_subtitle and board_type != "m5stickv":
                # Extra cut on Cube to fit progress bar
                # and entropy measurement on flash filling
                region_w -= FONT_HEIGHT

        # Pass precomputed values as tuples
        lcd.display(
            img, oft=(offset_x, offset_y), roi=(region_x, region_y, region_w, region_h)
        )


display = Display()
