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
import os

# avoids importing from flash VSF
os.chdir("/")

VERSION = "0.1"
NAME = "Nostr app"

from krux.pages import Menu, MENU_CONTINUE, MENU_EXIT, LETTERS
from krux.pages.login import Login, DIGITS_HEX, DIGITS
from krux.pages.home_pages.home import Home
from krux.krux_settings import t, Settings
from krux.display import (
    NARROW_SCREEN_WITH,
    STATUS_BAR_HEIGHT,
    FONT_HEIGHT,
    BOTTOM_PROMPT_LINE,
)
from krux.themes import theme


NSEC_SIZE = 63
HEX_SIZE = 64

NSEC = "nsec"
PRIV_HEX = "priv-hex"
NPUB = "npub"
PUB_HEX = "pub-hex"
HEX = "hex"
MNEMONIC = "mnemonic"
DEFAULT_MNEMONIC = "action action action action action action action action action action action action"

FILE_SUFFIX = "-nostr"
FILE_EXTENSION = ".txt"

class NostrKey:

    def __init__(self):
        self.update()

    def update(self, key = "none", value = None):
        self.key = key
        self.value = value

    def loaded(self):
        return self.key in (NSEC, PRIV_HEX, MNEMONIC)
    
    def loaded_mnemonic(self):
        print("loaded_mnemonic", self.key, self.value)
        return self.key == MNEMONIC


class KMenu(Menu):
    """Customizes the page's menu"""

    def draw_wallet_indicator(self):
        """Customize the top bar"""
        text = NAME
        if nostrKey.loaded_mnemonic():
            super().draw_wallet_indicator()
        elif nostrKey.loaded():
            text = nostrKey.key.upper()
        else:
            if self.ctx.display.width() > NARROW_SCREEN_WITH:
                self.ctx.display.draw_hcentered_text(
                    text,
                    STATUS_BAR_HEIGHT - FONT_HEIGHT - 1,
                    theme.highlight_color,
                    theme.info_bg_color,
                )
            else:
                self.ctx.display.draw_string(
                    24,
                    STATUS_BAR_HEIGHT - FONT_HEIGHT - 1,
                    text,
                    theme.highlight_color,
                    theme.info_bg_color,
                )


class Klogin(Login):
    """The page to insert the Key"""

    def __init__(self, ctx):
        super().__init__(ctx)
        self.menu = KMenu(
            ctx,
            [
                (t("Load Mnemonic"), self.load_key),
                (t("New Mnemonic"), self.new_key),
                (t("Load nsec or hex"), self.load_nsec),
                (t("About"), self.about),
                self.shutdown_menu_item(ctx),
            ],
            back_label=None,
        )

    # Follow NIP-06 ?
    # Basic key derivation from mnemonic seed phrase
    # https://github.com/nostr-protocol/nips/blob/master/06.md
    # https://github.com/vitorpamplona/amethyst/tree/main/quartz/src/main/java/com/vitorpamplona/quartz/crypto/nip06
    def _confirm_wallet_key(self, mnemonic):
        from krux.key import Key
        from embit.networks import NETWORKS
        from krux.settings import MAIN_TXT

        return Key(mnemonic, False, NETWORKS[MAIN_TXT])

    def load_nsec(self):
        """Load nsec or hex menu item"""

        submenu = Menu(
            self.ctx,
            [
                (t("QR Code"), self._load_nostr_priv_cam),
                (t("Via Manual Input"), self._pre_load_nostr_priv_manual),
                (
                    t("Load from SD card"),
                    None if not self.has_sd_card() else self._load_nostr_priv_sd,
                ),
            ],
        )
        index, status = submenu.run_loop()
        if index == len(submenu.menu) - 1:
            return MENU_CONTINUE
        return status

    def _pre_load_nostr_priv_manual(self):
        submenu = Menu(
            self.ctx,
            [
                (NSEC, lambda ver=NSEC: self._load_nostr_priv_manual(ver)),
                (HEX, lambda ver=HEX: self._load_nostr_priv_manual(ver)),
            ],
        )
        index, status = submenu.run_loop()
        if index == len(submenu.menu) - 1:
            return MENU_CONTINUE
        return status

    def _load_nostr_priv_cam(self):
        from krux.pages.qr_capture import QRCodeCapture

        error_msg = t("Failed to load")
        qr_capture = QRCodeCapture(self.ctx)
        data, _ = qr_capture.qr_capture_loop()
        if data is None:
            self.flash_error(error_msg)
            return MENU_CONTINUE

        try:
            data_str = data.decode() if not isinstance(data, str) else data
            if not self._load_nostr_priv_key(data_str):
                raise ValueError()
        except:
            self.flash_error(error_msg)
            return MENU_CONTINUE

        return MENU_EXIT

    def _load_nostr_priv_manual(self, version):
        title = t("Private Key")

        data = ""
        if version == NSEC:
            data = self.capture_from_keypad(
                title, [LETTERS, DIGITS], starting_buffer=NSEC
            )
        else:
            data = self.capture_from_keypad(title, [DIGITS_HEX])

        data = str(data)
        if len(data) > HEX_SIZE:
            raise ValueError("Maximum length exceeded (%s)" % HEX_SIZE)
        if version == NSEC and len(data) > NSEC_SIZE:
            raise ValueError("Maximum length exceeded (%s)" % NSEC_SIZE)

        self.ctx.display.clear()
        self.ctx.display.draw_hcentered_text(t("Private Key") + ":\n\n" + data)
        if not self.prompt(
            t("Proceed?"),
            BOTTOM_PROMPT_LINE,
        ):
            return MENU_CONTINUE

        try:
            if not self._load_nostr_priv_key(data):
                raise ValueError()
        except:
            self.flash_error(t("Failed to load"))
            return MENU_CONTINUE

        return MENU_EXIT

    def _load_nostr_priv_sd(self):
        from krux.pages.utils import Utils

        # Prompt user for file
        filename, _ = Utils(self.ctx).load_file(prompt=False, only_get_filename=True)

        if not filename:
            return MENU_CONTINUE

        from krux.sd_card import SDHandler

        data = None
        mnemonic = ""
        try:
            with SDHandler() as sd:
                data = sd.read(filename)

            data = data.replace("\r\n", "").replace("\n", "")
            if not self._load_nostr_priv_key(data):
                raise ValueError()
        except:
            self.flash_error(t("Failed to load"))
            return MENU_CONTINUE

        from krux.wallet import Wallet

        self.ctx.wallet = Wallet(self._confirm_wallet_key(mnemonic))

        return MENU_EXIT

    def _load_nostr_priv_key(self, data):
        if data.startswith(NSEC) and len(data) == NSEC_SIZE:
            nostrKey.update(NSEC, data)
            self._load_fake_mnemonic()
            return True
        if len(data) == HEX_SIZE:
            nostrKey.update(PRIV_HEX, data)
            self._load_fake_mnemonic()
            return True

        return False
    
    def _load_fake_mnemonic(self):
        from krux.wallet import Wallet

        self.ctx.wallet = Wallet(self._confirm_wallet_key(DEFAULT_MNEMONIC))

    def about(self):
        """Handler for the 'about' menu item"""

        self.ctx.display.clear()
        self.ctx.display.draw_centered_text(
            "Krux app\n" + NAME + "\n\n" + t("Version") + "\n%s" % VERSION
        )
        self.ctx.input.wait_for_button()
        return MENU_CONTINUE


class Khome(Home):
    """The page after loading the Key"""

    def __init__(self, ctx):
        super().__init__(ctx)

        self.menu = KMenu(
            ctx,
            [
                (
                    t("Backup Mnemonic"),
                    (
                        self.backup_mnemonic
                        if not Settings().security.hide_mnemonic and
                        nostrKey.loaded_mnemonic()
                        else None
                    ),
                ),
                (t("Nostr Keys"), self.nostr_keys),
                ("BIP85", self.bip85),
                (t("Sign Event"), self.sign_message),
                self.shutdown_menu_item(ctx),
            ],
            back_label=None,
        )

    def nostr_keys(self):
        """Handler for Nostr Keys menu item"""

        try:
            self._get_private_key()
        except:
            raise ValueError("This mnemonic cannot be converted, try another")

        submenu = Menu(
            self.ctx,
            [
                (
                    t("Private Key"),
                    (
                        None
                        if Settings().security.hide_mnemonic
                        else lambda: self.show_key_formats([NSEC, PRIV_HEX])
                    ),
                ),
                (t("Public Key"), lambda: self.show_key_formats([NPUB, PUB_HEX])),
            ],
        )
        index, status = submenu.run_loop()
        if index == len(submenu.menu) - 1:
            return MENU_CONTINUE
        return status

    def show_key_formats(self, versions):
        """Create menu to select Nostr keys in text or QR"""

        def _nostr_key_text(version):
            def _save_nostr_to_sd(version):
                from krux.pages.file_operations import SaveFile

                save_page = SaveFile(self.ctx)
                title = version + FILE_SUFFIX
                save_page.save_file(
                    self._get_nostr_key(version),
                    title,
                    title,
                    title + ":",
                    FILE_EXTENSION,
                    save_as_binary=False,
                )

            nostr_text_menu_items = [
                (
                    t("Save to SD card"),
                    (
                        None
                        if not self.has_sd_card()
                        else lambda ver=version: _save_nostr_to_sd(ver)
                    ),
                ),
            ]
            full_nostr_key = (
                self._get_nostr_title(version)
                + ":\n\n"
                + str(self._get_nostr_key(version))
            )
            menu_offset = 5 + len(self.ctx.display.to_lines(full_nostr_key))
            menu_offset *= FONT_HEIGHT
            nostr_key_menu = Menu(self.ctx, nostr_text_menu_items, offset=menu_offset)
            self.ctx.display.clear()
            self.ctx.display.draw_hcentered_text(
                full_nostr_key,
                offset_y=FONT_HEIGHT,
                info_box=True,
            )
            nostr_key_menu.run_loop()

        def _nostr_key_qr(version):
            title = self._get_nostr_title(version)
            nostr_key = str(self._get_nostr_key(version))
            from krux.pages.qr_view import SeedQRView

            seed_qr_view = SeedQRView(self.ctx, data=nostr_key, title=title)
            seed_qr_view.display_qr(allow_export=True, transcript_tools=False)

        pub_key_menu_items = []
        for version in versions:
            title = version if version not in (PRIV_HEX, PUB_HEX) else HEX
            pub_key_menu_items.append(
                (title + " - " + t("Text"), lambda ver=version: _nostr_key_text(ver))
            )
            pub_key_menu_items.append(
                (title + " - " + t("QR Code"), lambda ver=version: _nostr_key_qr(ver))
            )
        pub_key_menu = Menu(self.ctx, pub_key_menu_items)
        while True:
            _, status = pub_key_menu.run_loop()
            if status == MENU_EXIT:
                break

        return MENU_CONTINUE

    def _get_nostr_title(self, version):
        if version == NPUB:
            return "Public Key npub"
        if version == PUB_HEX:
            return "Public Key hex"
        if version == NSEC:
            return "Private Key nsec"
        return "Private Key hex"

    def _get_nostr_key(self, version):

        def _encode_nostr_key(bits, version):
            from embit import bech32

            converted_bits = bech32.convertbits(bits, 8, 5)
            return bech32.bech32_encode(bech32.Encoding.BECH32, version, converted_bits)

        if version in (NPUB, PUB_HEX):
            pub_key = self._get_private_key().get_public_key().serialize()[1:]
            if version == NPUB:
                return _encode_nostr_key(pub_key, version)
            return pub_key.hex()
        if version == NSEC:
            return _encode_nostr_key(self._get_mnemonic_bytes(), version)
        return self._get_mnemonic_bytes().hex()

    def _get_mnemonic_bytes(self):
        from embit import bip39

        mnemonic = self.ctx.wallet.key.mnemonic
        return bip39.mnemonic_to_bytes(mnemonic, ignore_checksum=True)

    def _get_private_key(self):
        from embit import ec

        return ec.PrivateKey(self._get_mnemonic_bytes())


def run(ctx):
    """Runs this kapp"""

    Klogin(ctx).run()

    if ctx.is_logged_in():
        while True:
            if not Khome(ctx).run():
                break

    print("Exited!!!!")


nostrKey = NostrKey()