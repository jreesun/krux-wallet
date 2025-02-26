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

from ..display import BOTTOM_PROMPT_LINE
from ..krux_settings import t, Settings
from ..encryption import AES_BLOCK_SIZE
from ..themes import theme
from . import (
    Page,
    Menu,
    MENU_CONTINUE,
    ESC_KEY,
    LETTERS,
    UPPERCASE_LETTERS,
    NUM_SPECIAL_1,
    NUM_SPECIAL_2,
)

ENCRYPTION_KEY_MAX_LEN = 200


class EncryptionKey(Page):
    """UI to capture an encryption key"""

    def __init__(self, ctx):
        super().__init__(ctx, None)
        self.ctx = ctx

    def encryption_key(self):
        """Loads and returns an ecnryption key from keypad or QR code"""
        submenu = Menu(
            self.ctx,
            [
                (t("Type Key"), self.load_key),
                (t("Scan Key QR Code"), self.load_qr_encryption_key),
            ],
            back_label=None,
        )
        _, key = submenu.run_loop()
        if key in (ESC_KEY, MENU_CONTINUE):
            return None

        if key:
            self.ctx.display.clear()
            self.ctx.display.draw_hcentered_text(t("Key") + ": " + key)
            if self.prompt(
                t("Proceed?"),
                BOTTOM_PROMPT_LINE,
            ):
                return key
        return None

    def load_key(self):
        """Loads and returns a key from keypad"""
        data = self.capture_from_keypad(
            t("Key"), [LETTERS, UPPERCASE_LETTERS, NUM_SPECIAL_1, NUM_SPECIAL_2]
        )
        if len(str(data)) > ENCRYPTION_KEY_MAX_LEN:
            raise ValueError("Maximum length exceeded (%s)" % ENCRYPTION_KEY_MAX_LEN)
        return data

    def load_qr_encryption_key(self):
        """Loads and returns a key from a QR code"""

        from .qr_capture import QRCodeCapture

        qr_capture = QRCodeCapture(self.ctx)
        data, _ = qr_capture.qr_capture_loop()
        if data is None:
            self.flash_error(t("Failed to load"))
            return None
        if len(data) > ENCRYPTION_KEY_MAX_LEN:
            raise ValueError("Maximum length exceeded (%s)" % ENCRYPTION_KEY_MAX_LEN)
        return data


class EncryptMnemonic(Page):
    """UI with mnemonic encryption output options"""

    def __init__(self, ctx):
        super().__init__(ctx, None)
        self.ctx = ctx

    def encrypt_menu(self):
        """Menu with mnemonic encryption output options"""

        encrypt_outputs_menu = [
            (t("Store on Flash"), self.store_mnemonic_on_memory),
            (
                t("Store on SD Card"),
                (
                    None
                    if not self.has_sd_card()
                    else lambda: self.store_mnemonic_on_memory(True)
                ),
            ),
            (t("Encrypted QR Code"), self.encrypted_qr_code),
        ]
        submenu = Menu(self.ctx, encrypt_outputs_menu)
        _, _ = submenu.run_loop()
        return MENU_CONTINUE

    def _get_user_inputs(self):
        """Ask user for the key, mnemonic_id and i_vector"""

        error_txt = t("Mnemonic was not encrypted")

        key_capture = EncryptionKey(self.ctx)
        key = key_capture.encryption_key()
        if key is None:
            self.flash_error(t("Key was not provided"))
            return None

        version = Settings().encryption.version
        i_vector = None
        if version == "AES-CBC":
            self.ctx.display.clear()
            self.ctx.display.draw_centered_text(
                t("Additional entropy from camera required for AES-CBC mode")
            )
            if not self.prompt(t("Proceed?"), BOTTOM_PROMPT_LINE):
                self.flash_error(error_txt)
                return None
            from .capture_entropy import CameraEntropy

            camera_entropy = CameraEntropy(self.ctx)
            entropy = camera_entropy.capture(show_entropy_details=False)
            if entropy is None:
                self.flash_error(error_txt)
                return None
            i_vector = entropy[:AES_BLOCK_SIZE]

        mnemonic_id = None
        self.ctx.display.clear()
        if self.prompt(
            t(
                "Give this mnemonic a custom ID? Otherwise current fingerprint will be used"
            ),
            self.ctx.display.height() // 2,
        ):
            mnemonic_id = self.capture_from_keypad(
                t("Mnemonic ID"),
                [LETTERS, UPPERCASE_LETTERS, NUM_SPECIAL_1],
            )
        if mnemonic_id in (None, ESC_KEY):
            mnemonic_id = self.ctx.wallet.key.fingerprint_hex_str()

        return (key, mnemonic_id, i_vector)

    def store_mnemonic_on_memory(self, sd_card=False):
        """Save encrypted mnemonic on flash or sd_card"""

        user_inputs = self._get_user_inputs()
        if user_inputs is None:
            return
        key, mnemonic_id, i_vector = user_inputs

        from ..encryption import MnemonicStorage

        mnemonic_storage = MnemonicStorage()
        if mnemonic_id in mnemonic_storage.list_mnemonics(sd_card):
            self.flash_error(
                t("ID already exists") + "\n" + t("Encrypted mnemonic was not stored")
            )
            del mnemonic_storage
            return

        self.ctx.display.clear()
        self.ctx.display.draw_centered_text(t("Processing.."))
        words = self.ctx.wallet.key.mnemonic
        if mnemonic_storage.store_encrypted(key, mnemonic_id, words, sd_card, i_vector):
            self.ctx.display.clear()
            self.ctx.display.draw_centered_text(
                t("Encrypted mnemonic was stored with ID:") + " " + mnemonic_id
            )
        else:
            self.ctx.display.clear()
            self.ctx.display.draw_centered_text(
                t("Failed to store mnemonic"), theme.error_color
            )
        self.ctx.input.wait_for_button()
        del mnemonic_storage

    def encrypted_qr_code(self):
        """Exports an encryprted mnemonic QR code"""

        user_inputs = self._get_user_inputs()
        if user_inputs is None:
            return
        key, mnemonic_id, i_vector = user_inputs

        self.ctx.display.clear()
        self.ctx.display.draw_centered_text(t("Processing.."))

        from ..encryption import EncryptedQRCode

        encrypted_qr = EncryptedQRCode()
        words = self.ctx.wallet.key.mnemonic
        qr_data = encrypted_qr.create(key, mnemonic_id, words, i_vector)
        del encrypted_qr

        from .qr_view import SeedQRView

        seed_qr_view = SeedQRView(self.ctx, data=qr_data, title=mnemonic_id)
        seed_qr_view.display_qr(allow_export=True)


class LoadEncryptedMnemonic(Page):
    """UI to load encrypted mnemonics stored on flash and Sd card"""

    def __init__(self, ctx):
        super().__init__(ctx, None)
        self.ctx = ctx

    def load_from_storage(self, remove_opt=False):
        """Lists all encrypted mnemonics stored is flash and SD card"""
        from ..encryption import MnemonicStorage

        mnemonic_ids_menu = []
        mnemonic_storage = MnemonicStorage()
        mnemonics = mnemonic_storage.list_mnemonics()
        sd_mnemonics = mnemonic_storage.list_mnemonics(sd_card=True)
        del mnemonic_storage

        for mnemonic_id in sorted(mnemonics):
            mnemonic_ids_menu.append(
                (
                    mnemonic_id + "(flash)",
                    lambda m_id=mnemonic_id: (
                        self._remove_encrypted_mnemonic(m_id)
                        if remove_opt
                        else self._load_encrypted_mnemonic(m_id)
                    ),
                )
            )
        for mnemonic_id in sorted(sd_mnemonics):
            mnemonic_ids_menu.append(
                (
                    mnemonic_id + "(SD card)",
                    lambda m_id=mnemonic_id: (
                        self._remove_encrypted_mnemonic(m_id, sd_card=True)
                        if remove_opt
                        else self._load_encrypted_mnemonic(m_id, sd_card=True)
                    ),
                )
            )
        submenu = Menu(self.ctx, mnemonic_ids_menu)
        index, status = submenu.run_loop()
        if index == len(submenu.menu) - 1:
            return MENU_CONTINUE
        return status

    def _load_encrypted_mnemonic(self, mnemonic_id, sd_card=False):
        """Uses encryption module to load and decrypt a mnemonic"""
        from ..encryption import MnemonicStorage

        error_txt = t("Failed to decrypt")

        key_capture = EncryptionKey(self.ctx)
        key = key_capture.encryption_key()
        if key in (None, "", ESC_KEY):
            self.flash_error(t("Key was not provided"))
            return MENU_CONTINUE
        self.ctx.display.clear()
        self.ctx.display.draw_centered_text(t("Processing.."))
        mnemonic_storage = MnemonicStorage()
        try:
            words = mnemonic_storage.decrypt(key, mnemonic_id, sd_card).split()
        except:
            self.flash_error(error_txt)
            return MENU_CONTINUE

        if len(words) not in (12, 24):
            self.flash_error(error_txt)
            return MENU_CONTINUE
        del mnemonic_storage
        return words

    def _remove_encrypted_mnemonic(self, mnemonic_id, sd_card=False):
        """Deletes a mnemonic"""
        from ..encryption import MnemonicStorage

        mnemonic_storage = MnemonicStorage()
        self.ctx.display.clear()
        if self.prompt(t("Remove %s?") % mnemonic_id, self.ctx.display.height() // 2):
            mnemonic_storage.del_mnemonic(mnemonic_id, sd_card)
            message = t("%s removed.") % mnemonic_id
            message += "\n\n"
            if sd_card:
                message += t(
                    "Fully erase your SD card in another device to ensure data is unrecoverable"
                )
            else:
                message += t("To ensure data is unrecoverable use Wipe Device feature")
            self.ctx.display.clear()
            self.ctx.display.draw_centered_text(message)
            self.ctx.input.wait_for_button()
        del mnemonic_storage
