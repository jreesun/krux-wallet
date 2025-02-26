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
    NUM_SPECIAL_1,
    NUM_SPECIAL_2,
)
from ..krux_settings import t, TC_CODE_PATH, TC_CODE_PBKDF2_ITERATIONS


class TCCodeVerification(Page):
    """Tamper Check Code Verification Page"""

    def __init__(self, ctx):
        super().__init__(ctx, None)
        self.ctx = ctx

    def capture(self, changing_tc_code=False, return_hash=False):
        """Capture Tamper Check Code from user"""
        import hashlib
        from machine import unique_id

        label = (
            t("Current Tamper Check Code")
            if changing_tc_code
            else t("Tamper Check Code")
        )
        tc_code = self.capture_from_keypad(
            label, [NUM_SPECIAL_1, LETTERS, UPPERCASE_LETTERS, NUM_SPECIAL_2]
        )
        if tc_code == ESC_KEY:
            return False
        # Hashes the tamper check code
        tc_code_bytes = tc_code.encode()
        # Tamper Check Code hash will be used in "TC Flash Hash"
        tc_code_hash = hashlib.sha256(tc_code_bytes).digest()

        # Read the contents of tamper check code file
        with open(TC_CODE_PATH, "rb") as f:
            file_secret = f.read()

        self.ctx.display.clear()
        self.ctx.display.draw_centered_text(t("Processing.."))

        # Generate PBKDF2 stretched secret
        secret = hashlib.pbkdf2_hmac(
            "sha256", tc_code_hash, unique_id(), TC_CODE_PBKDF2_ITERATIONS
        )
        if secret == file_secret:
            if return_hash:
                return tc_code_hash
            return True

        self.flash_error(t("Invalid Tamper Check Code"))
        return False
