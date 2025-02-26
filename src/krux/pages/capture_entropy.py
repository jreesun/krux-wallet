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
import math
from . import Page
from ..display import FONT_HEIGHT, BOTTOM_LINE, BOTTOM_PROMPT_LINE
from ..krux_settings import t
from ..themes import theme

POOR_VARIANCE_TH = 10  # RMS value of L, A, B channels considered poor
INSUFFICIENT_VARIANCE_TH = 5  # RMS value of L, A, B channels considered insufficient
INSUFFICIENT_SHANNONS_ENTROPY_TH = 3  # bits per pixel
NOT_PRESSED = 0
PROCEED_PRESSED = 1
CANCEL_PRESSED = 2

INSUFFICIENT_ENTROPY = 0
POOR_ENTROPY = 1
GOOD_ENTROPY = 2
UNKNOWN_ENTROPY = 3


class CameraEntropy(Page):
    """Class for capturing entropy from a snapshot"""

    def __init__(self, ctx):
        super().__init__(ctx, None)
        self.ctx = ctx

        # State machine to measure the entropy every 4 frames and reduce processing load
        self.image_stats = None
        self.image_stats_vector = [0] * 3
        self.measurement_machine_state = 0
        self.previous_measurement = UNKNOWN_ENTROPY
        self.stdev_index = 0
        self.y_label_offset = BOTTOM_LINE
        if board.config["type"] == "amigo":
            self.y_label_offset = BOTTOM_PROMPT_LINE

    def _callback(self):
        """
        Returns PROCEED if user pressed ENTER or touched the screen,
        CANCEL if user pressed PAGE or PAGE_PREV, 0 otherwise
        """
        if self.ctx.input.enter_event() or self.ctx.input.touch_event(
            validate_position=False
        ):
            return PROCEED_PRESSED
        if self.ctx.input.page_event() or self.ctx.input.page_prev_event():
            return CANCEL_PRESSED
        return NOT_PRESSED

    def rms_value(self, data):
        """Calculates the RMS value of a list of numbers"""
        if not data:
            return 0
        square_sum = sum(x**2 for x in data)
        mean_square = square_sum / len(data)
        rms = math.sqrt(mean_square)
        return int(rms)

    def entropy_measurement_update(self, img, all_at_once=False, show_measurement=True):
        """
        Entropy measurement state machine calculates and prints entropy estimation every 4 frames
        """

        if all_at_once:
            self.measurement_machine_state = 0

        if self.measurement_machine_state == 0:
            self.image_stats = img.get_statistics()
            if all_at_once:
                # Calculate all channels at once for final entropy estimation
                self.image_stats_vector[0] = self.image_stats.l_stdev()
                self.image_stats_vector[1] = self.image_stats.a_stdev()
                self.image_stats_vector[2] = self.image_stats.b_stdev()
            self.stdev_index = self.rms_value(self.image_stats_vector)
            entropy_level = INSUFFICIENT_ENTROPY
            if self.stdev_index > POOR_VARIANCE_TH:
                entropy_level = GOOD_ENTROPY
            elif self.stdev_index > INSUFFICIENT_VARIANCE_TH:
                entropy_level = POOR_ENTROPY
            if self.previous_measurement != entropy_level and show_measurement:
                self.ctx.display.to_portrait()
                self.previous_measurement = entropy_level
                self.ctx.display.fill_rectangle(
                    0,
                    self.y_label_offset,
                    self.ctx.display.width(),
                    FONT_HEIGHT,
                    theme.bg_color,
                )
                if entropy_level == GOOD_ENTROPY:
                    self.ctx.display.draw_hcentered_text(
                        t("Good entropy"), self.y_label_offset, theme.go_color
                    )
                elif entropy_level == POOR_ENTROPY:
                    self.ctx.display.draw_hcentered_text(
                        t("Poor entropy!"), self.y_label_offset, theme.del_color
                    )
                else:
                    self.ctx.display.draw_hcentered_text(
                        t("Insufficient entropy!"),
                        self.y_label_offset,
                        theme.error_color,
                    )
                self.ctx.display.to_landscape()

        elif self.measurement_machine_state == 1:
            self.image_stats_vector[0] = self.image_stats.l_stdev()
        elif self.measurement_machine_state == 2:
            self.image_stats_vector[1] = self.image_stats.a_stdev()
        elif self.measurement_machine_state == 3:
            self.image_stats_vector[2] = self.image_stats.b_stdev()
        self.measurement_machine_state += 1
        self.measurement_machine_state %= 4

    def capture(self, show_entropy_details=True):
        """Captures camera's entropy as the hash of image buffer"""
        import hashlib
        import gc
        import sensor
        import shannon
        from ..wdt import wdt
        from ..camera import ENTROPY_MODE

        self.ctx.display.clear()
        self.ctx.display.draw_centered_text(t("TOUCH or ENTER to capture"))
        self.ctx.display.to_landscape()
        self.ctx.camera.initialize_run(mode=ENTROPY_MODE)
        self.ctx.display.clear()

        command = 0

        # Flush events ocurred while loading camera
        self.ctx.input.reset_ios_state()
        while True:
            wdt.feed()

            img = sensor.snapshot()

            command = self._callback()
            if command != NOT_PRESSED:
                break

            self.entropy_measurement_update(img)
            self.ctx.display.render_image(img)

        self.ctx.display.to_portrait()
        gc.collect()
        sensor.run(0)

        # User cancelled
        if command == CANCEL_PRESSED:
            self.flash_text(t("Capture cancelled"))
            return None

        self.ctx.display.draw_centered_text(t("Processing.."))

        self.entropy_measurement_update(img, all_at_once=True, show_measurement=False)

        img_bytes = img.to_bytes()
        img_pixels = img.width() * img.height()
        del img

        # Calculate Shannon's entropy:
        shannon_16b = shannon.entropy_img16b(img_bytes)
        shannon_16b_total = shannon_16b * img_pixels

        entropy_msg = t("Shannon's entropy:") + "\n"
        entropy_msg += str(round(shannon_16b, 2)) + " " + "bits/px" + "\n"
        entropy_msg += t("(%d total)") % int(shannon_16b_total) + "\n\n"
        entropy_msg += t("Pixels deviation index:") + " "
        entropy_msg += str(self.stdev_index)
        self.ctx.display.clear()
        self.ctx.input.reset_ios_state()
        if (
            shannon_16b < INSUFFICIENT_SHANNONS_ENTROPY_TH
            or self.stdev_index < INSUFFICIENT_VARIANCE_TH
        ):
            error_msg = t("Insufficient entropy!")
            error_msg += "\n\n"
            error_msg += entropy_msg
            self.ctx.display.draw_centered_text(error_msg, theme.error_color)
            self.ctx.input.wait_for_button()
            return None
        if show_entropy_details:
            self.ctx.display.draw_centered_text(entropy_msg)
            self.ctx.input.wait_for_button()
        hasher = hashlib.sha256()
        image_len = len(img_bytes)
        hasher_index = 0
        while hasher_index < image_len:
            hasher.update(img_bytes[hasher_index : hasher_index + 128])
            hasher_index += 128
        return hasher.digest()
