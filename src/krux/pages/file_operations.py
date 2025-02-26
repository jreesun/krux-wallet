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

from . import (
    Page,
    ESC_KEY,
    LETTERS,
    UPPERCASE_LETTERS,
)
from ..krux_settings import t
from ..sd_card import SDHandler

FILE_SPECIAL = "1234567890[]-._()~"


class SaveFile(Page):
    """File saver user interface"""

    def __init__(self, ctx):
        super().__init__(ctx, None)

    def save_file(
        self,
        data,
        empty_name,
        filename="",
        file_description="",
        file_extension="",
        file_suffix="",
        save_as_binary=True,
        prompt=True,
    ):
        """File saver handler page"""
        persisted = False
        try:
            with SDHandler() as sd:
                # Wait until user defines a filename or select NO on the prompt
                while True:
                    self.ctx.display.clear()
                    if not prompt or self.prompt(
                        file_description + "\n" + t("Save to SD card?") + "\n\n",
                        self.ctx.display.height() // 2,
                    ):
                        new_filename = self.set_filename(
                            filename,
                            empty_name,
                            file_suffix,
                            file_extension,
                        )

                        if new_filename == ESC_KEY:
                            break

                        # if user defined a filename and it is ok, save!
                        if new_filename:
                            if save_as_binary:
                                sd.write_binary(new_filename, data)
                            else:
                                sd.write(new_filename, data)
                            self.flash_text(
                                t("Saved to SD card") + ":\n%s" % new_filename
                            )
                            persisted = True
                            break
                    else:
                        break
        except:
            self.flash_text(t("SD card not detected."))
        return persisted

    def set_filename(
        self, curr_filename="", empty_filename="some_file", suffix="", file_extension=""
    ):
        """
        Helper to set the filename based on a suggestion and the user input.
        Returns ESC_KEY if the user cancels the operation.
        Returns None if filename was not properly defined.
        """

        def remove_suffix(filename, suffix):
            return (
                filename[: -len(suffix)]
                if suffix and filename.endswith(suffix)
                else filename
            )

        # Remove file extension and suffix if they exist
        curr_filename = remove_suffix(
            remove_suffix(curr_filename, file_extension), suffix
        )

        while True:
            # Loop until user types a valid name or presses ESC
            # Capture filename from keypad
            new_filename = self.capture_from_keypad(
                t("Filename"),
                [LETTERS, UPPERCASE_LETTERS, FILE_SPECIAL],
                starting_buffer=(
                    (curr_filename + suffix)
                    if curr_filename
                    else (empty_filename + suffix)
                ),
            )

            if new_filename == ESC_KEY:
                return new_filename

            if new_filename == "" or all(c == "." for c in new_filename):
                continue

            final_filename = new_filename
            # Add file extension if not present
            if not final_filename.endswith(file_extension):
                final_filename += file_extension

            # Check for existing file and prompt for overwrite if necessary
            if SDHandler.file_exists("/sd/" + final_filename):
                self.ctx.display.clear()
                if not self.prompt(
                    t("Filename %s exists on SD card, overwrite?") % final_filename
                    + "\n\n",
                    self.ctx.display.height() // 2,
                ):
                    continue

            return final_filename
