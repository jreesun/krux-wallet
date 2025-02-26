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
import time
from . import Page
from ..display import FONT_HEIGHT, MINIMAL_PADDING
from ..input import PRESSED
from ..themes import theme
from ..qr import QRPartParser, FORMAT_UR
from ..wdt import wdt
from ..krux_settings import t
from ..camera import QR_SCAN_MODE, ANTI_GLARE_MODE, ZOOMED_MODE

ANTI_GLARE_WAIT_TIME = 500
MESSAGE_DISPLAY_PERIOD = 5000
PROGRESS_BAR_HEIGHT = 15


class QRCodeCapture(Page):
    """UI to capture an encryption key"""

    def __init__(self, ctx):
        super().__init__(ctx, None)
        self.ctx = ctx
        self.progress_bar_offset_y = {"cube": 225, "m5stickv": 210, "amigo": 380}.get(
            board.config["type"], 305
        )

    def light_control(self):
        """Controls the light based on the user input"""
        if self.ctx.input.enter_value() == PRESSED:
            self.ctx.light.turn_on()
        else:
            self.ctx.light.turn_off()

    def anti_glare_control(self):
        """Controls the anti-glare based on the user input"""
        self.ctx.display.to_portrait()
        mode = self.ctx.camera.toggle_camera_mode()
        if mode == QR_SCAN_MODE:
            self.ctx.display.draw_centered_text(t("Standard mode"))
        elif mode == ANTI_GLARE_MODE:
            self.ctx.display.draw_centered_text(t("Anti-glare mode"))
        elif mode == ZOOMED_MODE:
            self.ctx.display.clear()
            self.ctx.display.draw_centered_text(t("Zoomed mode"))
        time.sleep_ms(ANTI_GLARE_WAIT_TIME)
        # Erase the message from the screen
        self.ctx.display.fill_rectangle(
            0,
            (self.ctx.display.height() - FONT_HEIGHT) // 2,
            self.ctx.display.width(),
            FONT_HEIGHT,
            theme.bg_color,
        )
        self.ctx.display.to_landscape()
        self.ctx.input.reset_ios_state()

    def update_progress_ur(self, parser, color):
        """Fill the progress bar according to FORMAT_UR"""
        self.ctx.display.to_portrait()

        filled = (
            self.ctx.display.width() * parser.parsed_count()
        ) // parser.total_count()
        self.ctx.display.fill_rectangle(
            0, self.progress_bar_offset_y, filled, PROGRESS_BAR_HEIGHT, color
        )

        self.ctx.display.to_landscape()

    def update_progress_other(self, parser, index, previous_index):
        """Updates the progress bar for pMofN and BBQR"""
        self.ctx.display.to_portrait()

        block_size = self.ctx.display.width() / parser.total_count()
        fill_size = int(block_size * (index + 1)) - int(block_size * index)
        self.ctx.display.fill_rectangle(
            int(block_size * index),
            self.progress_bar_offset_y,
            fill_size,
            PROGRESS_BAR_HEIGHT,
            theme.highlight_color,
        )
        if previous_index is not None:
            fill_size = int(block_size * (previous_index + 1)) - int(
                block_size * previous_index
            )
            self.ctx.display.fill_rectangle(
                int(block_size * previous_index),
                self.progress_bar_offset_y,
                fill_size,
                PROGRESS_BAR_HEIGHT,
                theme.fg_color,
            )

        self.ctx.display.to_landscape()

    def qr_capture_loop(self):
        """Captures either singular or animated QRs and parses their contents"""

        self.ctx.display.clear()
        self.ctx.display.draw_centered_text(t("Loading Camera.."))
        self.ctx.camera.initialize_run()

        parser = QRPartParser()
        prev_parsed_count = 0
        new_part = None
        previous_part = None
        ur_highlighted = False

        # Flush events ocurred while loading camera
        self.ctx.input.reset_ios_state()
        start_time = time.ticks_ms()
        title_lines = self.ctx.display.draw_hcentered_text(
            t("Press PAGE to toggle mode"), MINIMAL_PADDING
        )
        self.ctx.display.to_landscape()
        while True:
            wdt.feed()

            if self.ctx.light:
                self.light_control()
            elif self.ctx.input.enter_event():
                break

            # Anti-glare mode
            if self.ctx.input.page_event():
                if self.ctx.camera.has_antiglare():
                    self.anti_glare_control()
                else:
                    break

            # Exit the capture loop with PAGE_PREV or TOUCH
            if self.ctx.input.page_prev_event() or self.ctx.input.touch_event():
                break

            if new_part is not None and new_part != previous_part:
                if parser.format == FORMAT_UR:
                    self.update_progress_ur(parser, theme.highlight_color)
                    ur_highlighted = True
                    previous_part = None
                else:
                    self.update_progress_other(parser, new_part, previous_part)
                    previous_part = new_part
                new_part = None
            elif ur_highlighted:
                self.update_progress_ur(parser, theme.fg_color)
                ur_highlighted = False

            img = self.ctx.camera.snapshot()
            if time.ticks_ms() < start_time + MESSAGE_DISPLAY_PERIOD:
                self.ctx.display.render_image(img, title_lines=title_lines)
            else:
                self.ctx.display.render_image(img)

            res = img.find_qrcodes()
            if res:
                data = res[0].payload()
                new_part = parser.parse(data)

                if (
                    parser.format == FORMAT_UR
                    and parser.processed_parts_count() > prev_parsed_count
                ):
                    prev_parsed_count = parser.processed_parts_count()
                    new_part = True

            if parser.is_complete():
                break

        self.ctx.camera.stop_sensor()
        if self.ctx.light:
            self.ctx.light.turn_off()
        self.ctx.display.to_portrait()

        if parser.is_complete():
            return parser.result(), parser.format
        return None, None
