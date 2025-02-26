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
from embit import bip85
from embit.bip32 import HARDENED_INDEX
from ...qr import FORMAT_NONE
from ...sd_card import B64_FILE_EXTENSION
from ...baseconv import base_encode
from ...display import BOTTOM_PROMPT_LINE, FONT_HEIGHT, DEFAULT_PADDING
from ...krux_settings import t
from ...krux_settings import Settings
from .. import (
    Menu,
    Page,
    DIGITS,
    ESC_KEY,
    choose_len_mnemonic,
)

BIP_PWD_APP_INDEX = 707764
DEFAULT_PWD_LEN = "21"
PWD_MIN_LEN = 20
PWD_MAX_LEN = 86


class Bip85(Page):
    """UI to export and load BIP85 entropy"""

    def _capture_index(self):
        """Capture the index from the user"""
        while True:
            child = self.capture_from_keypad(t("Index"), [DIGITS])
            if child == ESC_KEY:
                return None
            try:
                child_index = int(child)
            except:  # Empty input
                continue
            if child_index >= HARDENED_INDEX:
                self.flash_error(
                    t("Value %s out of range: [%s, %s]")
                    % (child_index, 0, HARDENED_INDEX - 1)
                )
                continue
            return child_index

    def _derive_mnemonic(self):
        """Derive a BIP85 mnemonic"""
        num_words = choose_len_mnemonic(self.ctx)
        if not num_words:
            return

        child_index = self._capture_index()
        if child_index is None:
            return

        bip85_words = bip85.derive_mnemonic(
            self.ctx.wallet.key.root,
            num_words,
            child_index,
        )
        self.ctx.display.clear()

        from ...key import Key

        key = Key(
            bip85_words,
            self.ctx.wallet.key.policy_type,
            self.ctx.wallet.key.network,
            script_type=self.ctx.wallet.key.script_type,
        )
        if not Settings().security.hide_mnemonic:
            self.display_mnemonic(
                bip85_words,
                suffix=t("Words"),
                fingerprint=key.fingerprint_hex_str(True),
            )
        else:
            self.ctx.display.draw_centered_text(key.fingerprint_hex_str(True))
        if self.prompt(t("Load?"), BOTTOM_PROMPT_LINE):
            from ...wallet import Wallet

            self.ctx.wallet = Wallet(key)
        return

    def _base64_password_qr(self, code, title):
        """Export BIP85 base64 password as QR"""
        self.display_qr_codes(code, FORMAT_NONE, title=title)

    def _save_b64_pwd_to_sd(self, info):
        from ..file_operations import SaveFile

        save_page = SaveFile(self.ctx)
        title = "BIP85 Password"
        file_name = "BIP85_password"
        save_page.save_file(
            info,
            file_name,
            file_name,
            title + ":",
            B64_FILE_EXTENSION,
            save_as_binary=False,
        )

    def _derive_base64_password(self):
        """Derive a BIP85 base64 password"""
        child_index = self._capture_index()
        if child_index is None:
            return

        # Capture the password length
        while True:
            pwd_len_txt = self.capture_from_keypad(
                t("Password Length"), [DIGITS], starting_buffer=DEFAULT_PWD_LEN
            )
            if pwd_len_txt == ESC_KEY:
                return
            try:
                pwd_len = int(pwd_len_txt)
            except:  # Empty input
                continue

            # Check if the password length is within the range
            if pwd_len < PWD_MIN_LEN or pwd_len > PWD_MAX_LEN:
                self.flash_error(
                    t("Value %s out of range: [%s, %s]")
                    % (pwd_len, PWD_MIN_LEN, PWD_MAX_LEN)
                )
                continue
            break

        entropy = bip85.derive_entropy(
            self.ctx.wallet.key.root,
            BIP_PWD_APP_INDEX,
            [pwd_len, child_index],
        )
        password = base_encode(entropy, 64).decode().strip()
        password = password[:pwd_len]
        info = password
        info += "\n\n" + t("Index: %s") % child_index
        info += "\n" + t("Length: %s") % pwd_len
        while True:
            menu_items = [
                (
                    t("QR Code"),
                    lambda: self._base64_password_qr(password, t("Base64 Password")),
                ),
                (
                    t("Save to SD card"),
                    (
                        None
                        if not self.has_sd_card()
                        else lambda: self._save_b64_pwd_to_sd(info)
                    ),
                ),
            ]
            self.ctx.display.clear()
            info_len = self.ctx.display.draw_hcentered_text(info, info_box=True)
            info_len *= FONT_HEIGHT
            info_len += DEFAULT_PADDING
            submenu = Menu(
                self.ctx,
                menu_items,
                offset=info_len,
            )
            index, _ = submenu.run_loop()
            if index == len(menu_items) - 1:
                break

    def export(self):
        """Exports BIP85 child mnemonics"""
        submenu = Menu(
            self.ctx,
            [
                (t("BIP39 Mnemonic"), self._derive_mnemonic),
                (t("Base64 Password"), self._derive_base64_password),
            ],
        )
        submenu.run_loop()
