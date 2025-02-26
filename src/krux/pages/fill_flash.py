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
import flash
import sensor
from . import Page, MENU_CONTINUE
from .capture_entropy import CameraEntropy, POOR_VARIANCE_TH
from ..themes import theme
from ..krux_settings import t
from ..display import BOTTOM_LINE, MINIMAL_PADDING
from ..wdt import wdt
from ..firmware import FLASH_SIZE
from ..camera import ENTROPY_MODE
import time

FLASH_ROWS = 64
BLOCK_SIZE = 0x1000
TOTAL_BLOCKS = FLASH_SIZE // BLOCK_SIZE
IMAGE_BYTES_SIZE = 0x25800
MAX_CHUNK_INDEX = IMAGE_BYTES_SIZE // BLOCK_SIZE
MAX_CAPTURE_PERIOD = 25  # Max. frame capture period in seconds


class FillFlash(Page):
    """Fill the flash memory with entropy data from the camera."""

    def __init__(self, ctx):
        super().__init__(ctx, None)
        self.ctx = ctx

    def capture_image_with_sufficient_entropy(self, entropy_measurement):
        """Capture an image with sufficient entropy."""
        start_time = time.time()  # Record the start time
        self.ctx.display.to_landscape()
        while time.time() - start_time < MAX_CAPTURE_PERIOD:
            wdt.feed()
            img = sensor.snapshot()
            entropy_measurement.entropy_measurement_update(img, all_at_once=True)
            self.ctx.display.render_image(img, title_lines=1, double_subtitle=True)
            if entropy_measurement.stdev_index > POOR_VARIANCE_TH:
                self.ctx.display.to_portrait()
                return img.to_bytes()
        raise ValueError(t("Insufficient entropy!"))

    def fill_flash_with_camera_entropy(self):
        """Fill the flash memory with entropy data from the camera."""
        if not self.prompt(
            t("Fill the flash with entropy from camera?"),
            self.ctx.display.height() // 2,
        ):
            return MENU_CONTINUE

        display_width = self.ctx.display.width()
        blocks_per_line = (
            TOTAL_BLOCKS + display_width - 1
        ) // display_width  # Ceiling division

        empty_buf = b"\xff" * BLOCK_SIZE
        img_bytes = b""
        block_count = 0
        offset_x = (display_width - (TOTAL_BLOCKS // blocks_per_line)) // 2

        offset_y = BOTTOM_LINE if board.config["type"] == "amigo" else BOTTOM_LINE - 12

        self.ctx.display.clear()
        self.ctx.display.draw_hcentered_text(t("Filling Flash"), MINIMAL_PADDING)

        self.ctx.camera.initialize_run(mode=ENTROPY_MODE)
        entropy_measurement = CameraEntropy(self.ctx)

        chunk_index = MAX_CHUNK_INDEX  # Force initial image capture
        line_color = theme.fg_color

        for address in range(0, FLASH_SIZE, BLOCK_SIZE):
            wdt.feed()

            if chunk_index == MAX_CHUNK_INDEX:
                chunk_index = 0
                img_bytes = self.capture_image_with_sufficient_entropy(
                    entropy_measurement
                )

            start = chunk_index * BLOCK_SIZE
            end = start + BLOCK_SIZE
            chunk = img_bytes[start:end]

            try:
                if flash.read(address, BLOCK_SIZE) == empty_buf:
                    flash.write(address, chunk)
                    chunk_index += 1
                    line_color = theme.highlight_color
            except Exception:
                self.ctx.camera.stop_sensor()
                self.flash_text("Flash error")
                return MENU_CONTINUE

            # Draw progress indicator
            if block_count % blocks_per_line == 0:
                self.ctx.display.draw_vline(offset_x, offset_y, 8, line_color)
                line_color = theme.fg_color
                offset_x += 1
            block_count += 1

        self.ctx.camera.stop_sensor()
        self.flash_text(t("Flash filled with camera entropy"))
        return MENU_CONTINUE
