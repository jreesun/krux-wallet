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
# pylint: disable=R0902

import time

from .touchscreens.ft6x36 import touch_control
from .krux_settings import Settings

IDLE = 0
PRESSED = 1
RELEASED = 2

SWIPE_THRESHOLD = 50
SWIPE_RIGHT = 1
SWIPE_LEFT = 2
SWIPE_UP = 3
SWIPE_DOWN = 4

TOUCH_S_PERIOD = 20  # Touch sample period - Min = 10


class Touch:
    """Touch is a singleton API to interact with touchscreen driver"""

    def __init__(self, width, height, irq_pin=None):
        """Touch API init - width and height are in Landscape mode
        For Krux width = max_y, height = max_x
        """
        self.sample_time = 0
        self.y_regions = []
        self.x_regions = []
        self.index = 0
        self.press_point = []
        self.release_point = (0, 0)
        self.gesture = None
        self.state = IDLE
        self.width, self.height = width, height
        self.touch_driver = touch_control
        self.touch_driver.activate_irq(irq_pin)
        self.touch_driver.threshold(Settings().hardware.touch.threshold)

    def clear_regions(self):
        """Remove previously stored buttons map"""
        self.y_regions = []
        self.x_regions = []

    def add_y_delimiter(self, region):
        """Adds a y button delimiter to be mapped as a array by touchscreen"""
        if region > self.width:
            raise ValueError("Touch region added outside display area")
        self.y_regions.append(region)

    def add_x_delimiter(self, region):
        """Adds a x button delimiter to be mapped as a array by touchscreen"""
        if region > self.height:
            raise ValueError("Touch region added outside display area")
        self.x_regions.append(region)

    def valid_position(self, data):
        """Checks if touch position is within buttons area"""

        if (
            hasattr(Settings().hardware.display, "flipped_orientation")
            and Settings().hardware.display.flipped_orientation
        ):
            data = (self.height - data[0], self.width - data[1])

        if self.x_regions and data[0] < self.x_regions[0]:
            return False
        if self.x_regions and data[0] > self.x_regions[-1]:
            return False
        if self.y_regions and data[1] < self.y_regions[0]:
            return False
        if self.y_regions and data[1] > self.y_regions[-1]:
            return False
        return True

    # def highlight_region(self, x_index, y_index):
    #     """Outlines the region of the current index"""
    #     import lcd
    #     from .themes import theme

    #     # Draw outline delimiting the region
    #     if y_index >= 0 and x_index >= 0:
    #         y_start = self.y_regions[y_index] if y_index < len(self.y_regions) else 0
    #         y_start += 1
    #         y_end = (
    #             self.y_regions[y_index + 1]
    #             if y_index + 1 < len(self.y_regions)
    #             else self.height
    #         )
    #         y_end -= 1
    #         x_start = self.x_regions[x_index] if x_index < len(self.x_regions) else 0
    #         x_start += 1
    #         x_end = (
    #             self.x_regions[x_index + 1]
    #             if x_index + 1 < len(self.x_regions)
    #             else self.height
    #         )
    #         x_end -= 1

    #         lcd.draw_outline(
    #             x_start,
    #             y_start,
    #             x_end - x_start,
    #             y_end - y_start,
    #             theme.fg_color,
    #         )

    def _extract_index(self, data):
        """
        Gets an index from touched points, x and y delimiters.
        The index is calculated based on the position of the touch within the defined regions.
        """
        y_index = 0
        x_index = 0

        # Calculate y index
        for region in self.y_regions:
            if data[1] > region:
                y_index += 1
        y_index -= 1 if y_index > 0 else 0

        # Calculate x index if x regions are defined (2D array)
        if self.x_regions:
            for x_region in self.x_regions:
                if data[0] > x_region:
                    x_index += 1
            x_index -= 1  # Adjust index to be zero-based
            # Combine y and x indices to get the final index
            index = y_index * (len(self.x_regions) - 1) + x_index
        else:
            index = y_index

        # self.highlight_region(x_index, y_index)

        return index

    def set_regions(self, x_list=None, y_list=None):
        """Set buttons map regions x and y"""
        if x_list:
            if isinstance(x_list, list):
                self.x_regions = x_list
            else:
                raise ValueError("x_list must be a list")
        else:
            self.x_regions = []

        if y_list:
            if isinstance(y_list, list):
                self.y_regions = y_list
            else:
                raise ValueError("y_list must be a list")
        else:
            self.y_regions = []

    def _store_points(self, data):
        """Store pressed points and calculare an average pressed point"""

        if (
            hasattr(Settings().hardware.display, "flipped_orientation")
            and Settings().hardware.display.flipped_orientation
        ):
            data = (self.height - data[0], self.width - data[1])

        if self.state == IDLE:
            self.state = PRESSED
            self.press_point = [data]
            self.index = self._extract_index(self.press_point[0])
        # Calculare an average (max. 10 samples) pressed point to increase precision
        elif self.state == PRESSED and len(self.press_point) < 10:
            self.press_point.append(data)
            len_press = len(self.press_point)
            x = 0
            y = 0
            for n in range(len_press):
                x += self.press_point[n][0]
                y += self.press_point[n][1]
            x //= len_press
            y //= len_press
            self.index = self._extract_index((x, y))
        self.release_point = data

    def current_state(self):
        """Returns the touchscreen state"""
        self.sample_time = time.ticks_ms()
        data = self.touch_driver.current_point()
        if isinstance(data, tuple):
            self._store_points(data)
        elif data is None:  # gets release then return to idle.
            if self.state == RELEASED:  # On touch release
                self.state = IDLE
            elif self.state == PRESSED:
                if self.release_point is not None:
                    lateral_lenght = self.release_point[0] - self.press_point[0][0]
                    if lateral_lenght > SWIPE_THRESHOLD:
                        self.gesture = SWIPE_RIGHT
                    elif -lateral_lenght > SWIPE_THRESHOLD:
                        self.gesture = SWIPE_LEFT
                        lateral_lenght *= -1  # make it positive value
                    vertical_lenght = self.release_point[1] - self.press_point[0][1]
                    if (
                        vertical_lenght > SWIPE_THRESHOLD
                        and vertical_lenght > lateral_lenght
                    ):
                        self.gesture = SWIPE_DOWN
                    elif (
                        -vertical_lenght > SWIPE_THRESHOLD
                        and -vertical_lenght > lateral_lenght
                    ):
                        self.gesture = SWIPE_UP
                self.state = RELEASED
        else:
            print("Touch error")
        return self.state

    def event(self, validate_position=True):
        """Checks if a touch happened and stores the point"""
        current_time = time.ticks_ms()
        if current_time > self.sample_time + TOUCH_S_PERIOD:
            if self.touch_driver.event():
                # Resets touch and gets irq point
                self.state = IDLE
                if not validate_position:
                    return True
                if isinstance(self.touch_driver.irq_point, tuple):
                    if self.valid_position(self.touch_driver.irq_point):
                        self._store_points(self.touch_driver.irq_point)
                        return True
        return False

    def value(self):
        """Wraps touch states to behave like a regular button"""
        return 1 if self.current_state() == IDLE else 0

    def swipe_right_value(self):
        """Returns detected gestures and clean respective variable"""
        if self.gesture == SWIPE_RIGHT:
            self.gesture = None
            return 0
        return 1

    def swipe_left_value(self):
        """Returns detected gestures and clean respective variable"""
        if self.gesture == SWIPE_LEFT:
            self.gesture = None
            return 0
        return 1

    def swipe_up_value(self):
        """Returns detected gestures and clean respective variable"""
        if self.gesture == SWIPE_UP:
            self.gesture = None
            return 0
        return 1

    def swipe_down_value(self):
        """Returns detected gestures and clean respective variable"""
        if self.gesture == SWIPE_DOWN:
            self.gesture = None
            return 0
        return 1

    def current_index(self):
        """Returns current intex of last touched point"""
        return self.index
