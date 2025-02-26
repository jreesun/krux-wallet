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

from .. import (
    Page,
    Menu,
    MENU_EXIT,
    ESC_KEY,
    choose_len_mnemonic,
)
from ...themes import theme
from ...krux_settings import t
from ...display import (
    DEFAULT_PADDING,
    FONT_HEIGHT,
    TOTAL_LINES,
    BOTTOM_PROMPT_LINE,
    MINIMAL_DISPLAY,
)

D6_STATES = [str(i + 1) for i in range(6)]
D20_STATES = [str(i + 1) for i in range(20)]

D6_12W_MIN_ROLLS = 50
D6_24W_MIN_ROLLS = 99
D20_12W_MIN_ROLLS = 30
D20_24W_MIN_ROLLS = 60
MIN_ENTROPY_12W = 128
MIN_ENTROPY_24W = 256

# Min. rolls hardly will reach min. entropy according to Shannon's index
# With a small tolerance, excessive low entropy warnings won't pop up when min. rolls are used.
ENTROPY_TOLERANCE = 2  # bits

PATTERN_DETECT_TOLERANCE = 30  # %
BAR_GRAPH_POSITION = 20  # % of screen (top of the graph)
BAR_GRAPH_SIZE = 60  # % of screen


class DiceEntropy(Page):
    """Capture and analise entropy from dice rolls"""

    def __init__(self, ctx, is_d20=False):
        super().__init__(ctx, None)
        self.ctx = ctx
        self.is_d20 = is_d20
        self.roll_states = D20_STATES if is_d20 else D6_STATES
        self.num_sides = len(self.roll_states)
        self.min_rolls = 0
        self.min_entropy = 0
        self.rolls = []
        self.roll_counts = [0] * self.num_sides

    def shannon_sum(self, distribution, sample_size):
        """Calculates Shannon's entropy of a given list"""
        import math

        # Calculate entropy
        unit_entropy = 0
        for count in distribution:
            probability = count / sample_size
            unit_entropy -= probability * (probability and math.log2(probability))
        return unit_entropy

    def calculate_entropy(self):
        """Calculates Shannon's entropy of a given list"""

        total_rolls = len(self.rolls)
        if not total_rolls:
            return 0
        self.roll_counts = [0] * self.num_sides
        for roll in self.rolls:
            self.roll_counts[int(roll) - 1] += 1

        return int(self.shannon_sum(self.roll_counts, total_rolls) * total_rolls)

    def pattern_detection(self):
        """
        Calculate Shannon's entropy of roll derivatives
        to detect arithmetic progression patterns.
        """
        import math

        if len(self.rolls) < self.min_rolls // 2:
            return 0  # Not enough data to analyze

        # Calculate derivatives
        derivatives = [
            int(self.rolls[i]) - int(self.rolls[i - 1])
            for i in range(1, len(self.rolls))
        ]
        min_derivative, max_derivative = -self.num_sides + 1, self.num_sides - 1
        derivative_range = max_derivative - min_derivative + 1
        derivative_counts = [0] * derivative_range

        # Count each derivative
        for derivative in derivatives:
            index = derivative - min_derivative
            derivative_counts[index] += 1

        derivative_entropy = self.shannon_sum(derivative_counts, len(derivatives))

        # Normalize entropy
        max_entropy = math.log2(derivative_range)
        normalized_entropy = (max_entropy - derivative_entropy) / max_entropy * 100

        return int(normalized_entropy) > PATTERN_DETECT_TOLERANCE

    def stats_for_nerds(self):
        """
        Displays statistical information and a graphical representation of dice roll outcomes.
        This method provides a deeper insight into the entropy collection process by showing:
        1. Distribution of dice rolls as a bar graph.
        2. The calculated Shannon's entropy in bits.
        It's intended for users interested in the quality and distribution of their entropy source.
        """
        self.ctx.display.clear()
        self.ctx.display.draw_hcentered_text(t("Rolls distribution:"), FONT_HEIGHT)
        shannon_entropy = self.calculate_entropy()
        max_count = max(self.roll_counts) or 1  # Prevent division by zero

        # Calculate scale factor based on display height and BAR_GRAPH_SIZE percentage
        display_height = self.ctx.display.height()
        scale = (display_height * BAR_GRAPH_SIZE) / (100 * max_count)

        # Generate bar heights using list comprehension
        bar_graph = [int(count * scale) for count in self.roll_counts]

        # Calculate horizontal padding and vertical offset for the bar graph
        display_width = self.ctx.display.width()
        bar_pad = display_width // (self.num_sides + 2)
        offset_x = bar_pad
        offset_y = (BAR_GRAPH_POSITION + BAR_GRAPH_SIZE) * display_height // 100

        # Draw each bar in the graph
        for height in bar_graph:
            self.ctx.display.fill_rectangle(
                offset_x + 1,
                offset_y - height,
                bar_pad - 2,
                height,
                theme.highlight_color,
            )
            offset_x += bar_pad

        # Draw Shannon's entropy below the graph
        suffix = " bits" if not MINIMAL_DISPLAY else "b"
        self.ctx.display.draw_hcentered_text(
            t("Shannon's entropy:") + " " + str(shannon_entropy) + suffix,
            offset_y + FONT_HEIGHT,
        )

        self.ctx.input.wait_for_button()

    def draw_progress_bar(self):
        """
        Draws a progress bar on the display to show the current progress of dice rolls.
        The progress bar consists of two sections: one indicating the number of rolls
        made relative to the minimum required, and the other indicating the Shannon's
        entropy of the rolls relative to the minimum required entropy. It changes color
        to indicate when the minimum criteria have been met.
        """
        offset_y = DEFAULT_PADDING + 2 * FONT_HEIGHT
        pb_height = FONT_HEIGHT - 4
        if len(self.rolls) > 0:  # Only draws if rolls > 0
            progress = min(self.min_rolls, len(self.rolls))
            progress *= self.ctx.display.usable_width() - 3
            progress //= self.min_rolls
            self.ctx.display.fill_rectangle(
                DEFAULT_PADDING + 2,
                offset_y + 2,
                progress,
                (pb_height // 2) - 2,
                theme.fg_color,
            )

        shannon_entropy = self.calculate_entropy()
        entropy_color = (
            theme.error_color if self.pattern_detection() else theme.highlight_color
        )
        if shannon_entropy:  # Only draws if Shannon's > 0
            shannon_progress = min(self.min_entropy, shannon_entropy)
            shannon_progress *= self.ctx.display.usable_width() - 3
            shannon_progress //= self.min_entropy
            self.ctx.display.fill_rectangle(
                DEFAULT_PADDING + 2,
                offset_y + (pb_height // 2) + 1,
                shannon_progress,
                (pb_height // 2) - 2,
                entropy_color,
            )
        if (
            shannon_entropy >= (self.min_entropy - ENTROPY_TOLERANCE)
            and len(self.rolls) >= self.min_rolls
        ):
            outline_color = theme.go_color
        else:
            outline_color = theme.no_esc_color
        self.ctx.display.outline(
            DEFAULT_PADDING,
            offset_y,
            self.ctx.display.usable_width(),
            pb_height,
            outline_color,
        )

    def new_key(self):
        """Create a new key from dice rolls"""
        len_mnemonic = choose_len_mnemonic(self.ctx)
        if not len_mnemonic:
            return None

        if len_mnemonic == 24:
            self.min_entropy = MIN_ENTROPY_24W
            self.min_rolls = D20_24W_MIN_ROLLS if self.is_d20 else D6_24W_MIN_ROLLS
        else:  # 12 words
            self.min_entropy = MIN_ENTROPY_12W
            self.min_rolls = D20_12W_MIN_ROLLS if self.is_d20 else D6_12W_MIN_ROLLS

        delete_flag = False
        self.ctx.display.draw_hcentered_text(
            t("Roll dice at least %d times to generate a mnemonic.") % (self.min_rolls)
        )
        if self.prompt(t("Proceed?"), BOTTOM_PROMPT_LINE):

            def delete_roll(buffer):
                # buffer not used here
                nonlocal delete_flag
                delete_flag = True
                return buffer

            while True:
                roll = ""
                while True:
                    dice_title = t("Rolls:") + " %d\n" % len(self.rolls)
                    entropy = (
                        "".join(self.rolls)
                        if self.num_sides < 10
                        else "-".join(self.rolls)
                    )
                    if len(entropy) <= 10:
                        dice_title += entropy
                    else:
                        dice_title += "..." + entropy[-10:]
                    roll = self.capture_from_keypad(
                        dice_title,
                        [self.roll_states],
                        delete_key_fn=delete_roll,
                        progress_bar_fn=self.draw_progress_bar,
                        go_on_change=True,
                    )
                    if roll == ESC_KEY:
                        return None
                    break

                if roll != "":
                    self.rolls.append(roll)
                else:
                    # If its not a roll it is Del or Go
                    if delete_flag:  # Del
                        delete_flag = False
                        if len(self.rolls) > 0:
                            self.rolls.pop()
                    elif len(self.rolls) < self.min_rolls:  # Not enough to Go
                        self.flash_text(t("Not enough rolls!"))
                    else:
                        warning_txt = ""
                        if self.calculate_entropy() < (
                            self.min_entropy - ENTROPY_TOLERANCE
                        ):
                            warning_txt += t("Poor entropy!")
                        if self.pattern_detection():
                            if warning_txt:
                                warning_txt += "\n"
                            warning_txt += t("Pattern detected!")
                        if warning_txt:
                            self.ctx.display.clear()
                            self.ctx.display.draw_centered_text(warning_txt)
                            if self.prompt(t("Proceed anyway?"), BOTTOM_PROMPT_LINE):
                                break
                        else:
                            break

            entropy = (
                "".join(self.rolls) if self.num_sides < 10 else "-".join(self.rolls)
            )
            self.ctx.display.clear()
            rolls_str = t("Rolls:") + "\n\n%s" % entropy
            max_lines = TOTAL_LINES - 6  # room for menu
            menu_offset = self.ctx.display.draw_hcentered_text(
                rolls_str, info_box=True, max_lines=max_lines
            )
            menu_offset *= FONT_HEIGHT
            menu_offset += DEFAULT_PADDING
            submenu = Menu(
                self.ctx,
                [
                    (t("Stats for Nerds"), lambda: MENU_EXIT),
                    (t("Generate Mnemonic"), lambda: MENU_EXIT),
                ],
                offset=menu_offset,
                back_label=None,
            )
            index, _ = submenu.run_loop()
            if index == 0:
                self.stats_for_nerds()

            import hashlib
            import binascii

            entropy_bytes = entropy.encode()
            entropy_hash = binascii.hexlify(
                hashlib.sha256(entropy_bytes).digest()
            ).decode()
            self.ctx.display.clear()
            self.ctx.display.draw_centered_text(
                t("SHA256 of rolls:") + "\n\n%s" % entropy_hash
            )
            self.ctx.input.wait_for_button()
            num_bytes = 32 if len_mnemonic == 24 else 16
            return hashlib.sha256(entropy_bytes).digest()[:num_bytes]

        return None
