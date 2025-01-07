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

# from . import Page
from ..display import SPLASH, FONT_HEIGHT, TOTAL_LINES
from ..themes import theme


class ScreenSaver:
    """Screensaver animation method"""

    def __init__(self, ctx):
        self.ctx = ctx

    def start(self):
        """Displays a screensaver until user presses a button or touch"""
        anim_frame = 0
        initial_offset = (TOTAL_LINES - len(SPLASH)) // 2
        fg_color = theme.fg_color
        bg_color = theme.bg_color
        self.ctx.display.clear()
        button_press = None
        while button_press is None:
            # show animation on the screeen
            offset_y = anim_frame * FONT_HEIGHT
            self.ctx.display.fill_rectangle(
                0,
                offset_y,
                self.ctx.display.width(),
                FONT_HEIGHT,
                bg_color,
            )
            if initial_offset <= anim_frame < len(SPLASH) + initial_offset:
                self.ctx.display.draw_hcentered_text(
                    SPLASH[anim_frame - initial_offset], offset_y, fg_color, bg_color
                )
            anim_frame += 1
            if anim_frame > len(SPLASH) + (2 * initial_offset) + 1:
                anim_frame = 0
                bg_color, fg_color = fg_color, bg_color
            # wait_duration(animation period) can be modified here
            button_press = self.ctx.input.wait_for_button(block=False)
