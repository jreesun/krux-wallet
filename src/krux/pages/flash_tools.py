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
from . import Page, Menu, MENU_CONTINUE, DEFAULT_PADDING
from ..themes import theme
from ..krux_settings import t
from ..display import FONT_HEIGHT, FONT_WIDTH, NARROW_SCREEN_WITH
from ..wdt import wdt
from ..firmware import (
    FLASH_SIZE,
    SPIFFS_ADDR,
    ERASE_BLOCK_SIZE,
)

BLOCK_SIZE = 0x1000
FLASH_ROWS = 64


class FlashTools(Page):
    """Menu for flash tools"""

    def flash_tools_menu(self):
        """Load the flash tools menu"""
        flash_menu = Menu(
            self.ctx,
            [
                (t("Flash Map"), self.flash_map),
                (t("TC Flash Hash"), self.tc_flash_hash),
                (t("Erase User's Data"), self.erase_users_data),
            ],
        )
        flash_menu.run_loop()
        return MENU_CONTINUE

    def flash_map(self):
        """Load the flash map page"""
        import flash
        import image

        image_block_size = self.ctx.display.width() // FLASH_ROWS
        if self.ctx.display.width() >= self.ctx.display.height():
            image_block_size -= 1
        empty_buf = b"\xff" * BLOCK_SIZE
        column, row = 0, 0
        offset_x = (self.ctx.display.width() - (image_block_size * FLASH_ROWS)) // 2
        offset_y = DEFAULT_PADDING + 2 * FONT_HEIGHT
        self.ctx.display.clear()
        self.ctx.display.draw_hcentered_text(t("Flash Map"))

        # Draw the legend
        l_y_text_offset = offset_y + image_block_size * FLASH_ROWS + FONT_HEIGHT
        l_y_block_offset = l_y_text_offset + (FONT_HEIGHT - FONT_WIDTH) // 2
        l_x_offset = DEFAULT_PADDING
        self.ctx.display.fill_rectangle(
            l_x_offset, l_y_block_offset, FONT_WIDTH, FONT_WIDTH, theme.highlight_color
        )
        l_x_offset += (3 * FONT_WIDTH) // 2
        self.ctx.display.draw_string(
            l_x_offset,
            l_y_text_offset,
            "Firmware",
            theme.fg_color,
        )
        if self.ctx.display.width() <= NARROW_SCREEN_WITH:
            l_y_text_offset += FONT_HEIGHT
            l_y_block_offset += FONT_HEIGHT
            l_x_offset = DEFAULT_PADDING
        else:
            l_x_offset = self.ctx.display.width() - DEFAULT_PADDING
            l_x_offset -= (3 * FONT_WIDTH) // 2
            l_x_offset -= lcd.string_width_px(t("User's Data"))
        self.ctx.display.fill_rectangle(
            l_x_offset, l_y_block_offset, FONT_WIDTH, FONT_WIDTH, theme.fg_color
        )
        l_x_offset += (3 * FONT_WIDTH) // 2
        self.ctx.display.draw_string(
            l_x_offset,
            l_y_text_offset,
            t("User's Data"),
            theme.fg_color,
        )
        l_y_text_offset += FONT_HEIGHT
        l_y_block_offset += FONT_HEIGHT
        l_x_offset = DEFAULT_PADDING
        self.ctx.display.fill_rectangle(
            l_x_offset, l_y_block_offset, FONT_WIDTH, FONT_WIDTH, theme.disabled_color
        )
        l_x_offset += (3 * FONT_WIDTH) // 2
        self.ctx.display.draw_string(
            l_x_offset,
            l_y_text_offset,
            t("Empty"),
            theme.fg_color,
        )

        # Draw a map of the flash memory
        mem_bar = image.Image(size=(FLASH_ROWS * image_block_size, image_block_size))
        for address in range(0, FLASH_SIZE, BLOCK_SIZE):
            wdt.feed()
            color = theme.highlight_color if address < SPIFFS_ADDR else theme.fg_color
            if flash.read(address, BLOCK_SIZE) == empty_buf:
                color = theme.disabled_color
            # Draw the block
            mem_bar.draw_rectangle(
                column * image_block_size,
                0,
                image_block_size,
                image_block_size,
                color,
                fill=True,
            )
            # Uncomment this lines to see flash_map on simulator
            # y_pos = offset_y + row * image_block_size
            # self.ctx.display.fill_rectangle(
            #     column * image_block_size,
            #     y_pos,
            #     image_block_size,
            #     image_block_size,
            #     color,
            # )
            column += 1
            if column >= FLASH_ROWS:
                y_pos = offset_y + row * image_block_size
                lcd.display(mem_bar, oft=(offset_x, y_pos))
                column = 0
                row += 1
        self.ctx.input.reset_ios_state()
        self.ctx.input.wait_for_button()

        return MENU_CONTINUE

    def tc_flash_hash(self):
        """Load the flash hash page"""

        if self.ctx.tc_code_enabled:
            from .tc_code_verification import TCCodeVerification

            tc_code_verification = TCCodeVerification(self.ctx)
            tc_code_hash = tc_code_verification.capture(return_hash=True)
            if not tc_code_hash:
                return MENU_CONTINUE
        else:
            self.flash_error(t("Set a tamper check code first"))
            return MENU_CONTINUE

        flash_hash = FlashHash(self.ctx, tc_code_hash)
        flash_hash.generate()

        return MENU_CONTINUE

    def erase_spiffs(self):
        """Erase all SPIFFS, removing all saved configs and mnemonics"""

        import flash

        empty_buf = b"\xff" * ERASE_BLOCK_SIZE
        for address in range(SPIFFS_ADDR, FLASH_SIZE, ERASE_BLOCK_SIZE):
            wdt.feed()
            if flash.read(address, ERASE_BLOCK_SIZE) == empty_buf:
                continue
            flash.erase(address, ERASE_BLOCK_SIZE)

    def erase_users_data(self):
        """Fully formats SPIFFS memory"""
        self.ctx.display.clear()
        if self.prompt(
            t(
                "Permanently remove all stored encrypted mnemonics and settings from flash?"
            ),
            self.ctx.display.height() // 2,
        ):
            self.ctx.display.clear()
            self.ctx.display.draw_centered_text(
                t("Erasing user's data..")
                + "\n\n"
                + t("Do not power off, it may take a while to complete.")
            )
            self.erase_spiffs()
            # Reboot so default settings take place and SPIFFS is formatted.
            self.ctx.power_manager.reboot()
        return MENU_CONTINUE


class FlashHash(Page):
    """Generate a human recognizable snapshot of the flash memory tied to a tamper check code"""

    def __init__(self, ctx, tc_code_hash):
        super().__init__(ctx, None)
        self.ctx = ctx
        self.tc_code_hash = tc_code_hash
        self.image_block_size = self.ctx.display.width() // 7

    def hash_pin_with_flash(self, spiffs_region=False):
        """Hashes the tamper check code, unique ID, and flash memory together."""
        import hashlib
        import flash
        from machine import unique_id

        counter = SPIFFS_ADDR // BLOCK_SIZE if spiffs_region else 0
        range_begin = SPIFFS_ADDR if spiffs_region else 0
        range_end = FLASH_SIZE if spiffs_region else SPIFFS_ADDR
        percentage_offset = (
            DEFAULT_PADDING + 3 * FONT_HEIGHT + self.image_block_size * 5
        )
        if self.ctx.display.width() < self.ctx.display.height():
            percentage_offset += FONT_HEIGHT
        sha256 = hashlib.sha256()
        sha256.update(self.tc_code_hash)
        sha256.update(unique_id())
        for address in range(range_begin, range_end, BLOCK_SIZE):
            counter += 1
            data = flash.read(address, BLOCK_SIZE)
            sha256.update(data)
            if counter % 100 == 0:
                # Update progress
                self.ctx.display.draw_hcentered_text(
                    "%d%%" % (counter // 41), percentage_offset
                )
                wdt.feed()
        return sha256.digest()

    def hash_to_random_color(self, hash_bytes):
        """Generates a random color from part of the hash."""
        # Extract the last 3 bytes of the hash
        red = hash_bytes[-3] % 2  # 0 or 1
        green = hash_bytes[-2] % 2
        blue = hash_bytes[-1] % 2

        # If all components are False, pick the highest value component and make it True
        if not red and not green and not blue:
            if hash_bytes[-3] >= hash_bytes[-2] and hash_bytes[-3] >= hash_bytes[-1]:
                red = 1
            elif hash_bytes[-2] >= hash_bytes[-3] and hash_bytes[-2] >= hash_bytes[-1]:
                green = 1
            else:
                blue = 1
        red = (0xFF >> 3) << 11 if red else 0
        green = (0xFF >> 2) << 5 if green else 0
        blue = 0xFF >> 3 if blue else 0

        return red + green + blue

    def hash_to_fingerprint(self, hash_bytes, y_offset=DEFAULT_PADDING):
        """Generates a 5x5 pixelated fingerprint based on a 256-bit hash."""

        fg_color = self.hash_to_random_color(hash_bytes)
        block_size = self.image_block_size

        # Create a 5x5 grid, only compute first 3 columns and mirror them
        for row in range(5):
            for col in range(3):  # Left half and center
                byte_index = row * 3 + col
                bit_value = hash_bytes[byte_index] % 2  # 0 or 1

                # Set the color based on the bit value
                color = fg_color if bit_value == 0 else 0  # 0 is background color

                # Calculate positions
                x = (col + 1) * block_size
                y = y_offset + row * block_size
                self.ctx.display.fill_rectangle(x, y, block_size, block_size, color)

                # Mirror the column for symmetry
                if col < 2:
                    mirrored_col = 5 - col
                    x_mirror = mirrored_col * block_size
                    self.ctx.display.fill_rectangle(
                        x_mirror, y, block_size, block_size, color
                    )

    def hash_to_words(self, hash_bytes):
        """Converts a hash to a list of mnemonic words."""
        from embit.bip39 import mnemonic_from_bytes

        words = mnemonic_from_bytes(hash_bytes).split()
        return " ".join(words[:2])

    def generate(self):
        """Generates the Tamper Check Flash Hash snapshot."""
        self.ctx.display.clear()
        self.ctx.display.draw_hcentered_text(t("Processing.."))
        firmware_hash = self.hash_pin_with_flash()
        self.ctx.display.clear()
        self.ctx.display.draw_hcentered_text("TC Flash Hash")
        y_offset = DEFAULT_PADDING + 2 * FONT_HEIGHT
        self.hash_to_fingerprint(firmware_hash, y_offset)
        anti_tamper_words = self.hash_to_words(firmware_hash)
        y_offset += self.image_block_size * 5
        if self.ctx.display.width() < self.ctx.display.height():
            y_offset += FONT_HEIGHT
        y_offset += (
            self.ctx.display.draw_hcentered_text(
                anti_tamper_words, y_offset, color=theme.highlight_color
            )
            * FONT_HEIGHT
        )
        spiffs_hash = self.hash_pin_with_flash(spiffs_region=True)
        anti_tamper_words = self.hash_to_words(spiffs_hash)
        self.ctx.display.draw_hcentered_text(anti_tamper_words, y_offset)
        self.ctx.input.reset_ios_state()
        self.ctx.input.wait_for_button()
        return MENU_CONTINUE
