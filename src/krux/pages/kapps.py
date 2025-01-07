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

from krux.pages import (
    Page,
    Menu,
    MENU_CONTINUE,
)
from krux.krux_settings import t
from krux.display import BOTTOM_PROMPT_LINE
from krux.sd_card import MPY_FILE_EXTENSION, SIGNATURE_FILE_EXTENSION, SD_PATH
from krux.settings import FLASH_PATH
import os

READABLEBUFFER_SIZE = 128


class Kapps(Page):
    """Krux standalone apps manager"""

    def __init__(self, ctx):
        self.ctx = ctx

        items = []
        signed_apps = self.parse_all_flash_apps()
        for app_name in signed_apps:
            clean_name = app_name[:-4]
            items += [
                (clean_name, lambda name=clean_name: self.execute_flash_kapp(name))
            ]
        items += [
            (
                t("Load from SD card"),
                None if not self.has_sd_card() else self.load_sd_kapp,
            )
        ]

        super().__init__(
            ctx,
            Menu(ctx, items),
        )

    def parse_all_flash_apps(self):
        """Check if any .mpy app present in flash is signed.
        If not, ask for deletion to prevent importing and executing malicious code"""

        from krux.firmware import sha256

        unsigned_apps = []
        signed_apps = []
        flash_path_prefix = "/%s/" % FLASH_PATH
        for file in os.listdir(flash_path_prefix):
            if file.endswith(MPY_FILE_EXTENSION):
                # Check if signature file exists for the .mpy file
                try:
                    sig_data = None
                    with open(
                        flash_path_prefix + file + SIGNATURE_FILE_EXTENSION,
                        "rb",
                        buffering=0,
                    ) as sigfile:
                        sig_data = sigfile.read()
                    if self.valid_signature(sig_data, sha256(flash_path_prefix + file)):
                        signed_apps += [file]
                    else:
                        unsigned_apps += [file]
                except:
                    unsigned_apps += [file]

        if len(unsigned_apps) > 0:
            # Prompts user about deleting as it will change flash memory and TC hash
            self.ctx.display.clear()
            if not self.prompt(
                t("Unsigned apps found in flash will be deleted.")
                + "\n\n"
                + t("Proceed?"),
                self.ctx.display.height() // 2,
            ):
                raise ValueError("Unsigned apps found in flash")

            # Delete any .mpy files from flash VFS to avoid malicious code import/execution
            for app in unsigned_apps:
                os.remove(flash_path_prefix + app)

        return signed_apps

    def valid_signature(self, sig, data_hash):
        """Return if signature of data_hash is valid"""

        from krux.firmware import get_pubkey, check_signature

        pubkey = get_pubkey()
        if pubkey is None:
            raise ValueError("Invalid public key")

        if not check_signature(pubkey, sig, data_hash):
            return False

        return True

    def execute_flash_kapp(self, app_name):
        """Prompt user to load and 'execute' a .mpy Krux app"""

        self.ctx.display.clear()
        if not self.prompt(
            t("Execute %s Krux app?") % app_name, self.ctx.display.height() // 2
        ):
            return MENU_CONTINUE

        # Allows import of files in flash VFS
        # TODO: Dinamically enable vsf->execution
        os.chdir("/" + FLASH_PATH)

        # Import and exec the kapp
        i_kapp = None
        try:
            i_kapp = __import__(app_name)
            i_kapp.run(self.ctx)
        except:
            # avoids importing from flash VSF
            os.chdir("/")

            from krux.themes import theme

            self.ctx.display.to_portrait()
            self.ctx.display.clear()
            self.ctx.display.draw_centered_text(
                t("Error:") + "\n" + "Could not execute %s" % app_name,
                theme.error_color,
            )
            self.ctx.input.wait_for_button()

        # avoids importing from flash VSF
        os.chdir("/")

        # After execution restart Krux (better safe than sorry)
        from ..power import power_manager

        power_manager.shutdown()
        return None

    def load_sd_kapp(self):
        """Loads kapp from SD to flash, then executes"""

        # Prompt user for .mpy file
        from krux.pages.utils import Utils

        filename, _ = Utils(self.ctx).load_file(
            MPY_FILE_EXTENSION, prompt=False, only_get_filename=True
        )

        if not filename:
            return MENU_CONTINUE

        from krux.firmware import sha256
        import binascii

        sd_path_prefix = "/%s/" % SD_PATH
        data_hash = sha256(sd_path_prefix + filename)

        # Confirm hash string
        self.ctx.display.clear()
        self.ctx.display.draw_hcentered_text(
            filename + "\n\n" + "SHA256:\n" + binascii.hexlify(data_hash).decode()
        )
        if not self.prompt(t("Proceed?"), BOTTOM_PROMPT_LINE):
            return MENU_CONTINUE

        # Check signature of .mpy file in SD
        sig_data = None
        try:
            with open(
                sd_path_prefix + filename + SIGNATURE_FILE_EXTENSION, "rb", buffering=0
            ) as sigfile:
                sig_data = sigfile.read()
        except:
            self.flash_error(t("Missing signature file"))
            return MENU_CONTINUE

        if not self.valid_signature(sig_data, data_hash):
            self.flash_error(t("Bad signature"))
            return MENU_CONTINUE

        # Check if app is already installed in flash
        found_in_flash_vfs = False
        flash_path_prefix = "/%s/" % FLASH_PATH
        for file in os.listdir(flash_path_prefix):
            if file.endswith(MPY_FILE_EXTENSION):
                if sha256(flash_path_prefix + file) == data_hash:
                    found_in_flash_vfs = True
                    filename_flash = file
                    break

        # Copy kapp + sig from SD to flash VFS, if app not found
        if not found_in_flash_vfs:
            # Warns user about changing users's flash internal memory region
            self.ctx.display.clear()
            if not self.prompt(
                t("App will be stored internally on flash.") + "\n\n" + t("Proceed?"),
                self.ctx.display.height() // 2,
            ):
                return MENU_CONTINUE

            # Save APP .mpy
            filename_flash = filename.rsplit("/", maxsplit=1)[-1]
            with open(
                flash_path_prefix + filename_flash,
                "wb",
                buffering=0,
            ) as flash_file:
                with open(sd_path_prefix + filename, "rb", buffering=0) as sd_file:
                    while True:
                        chunk = sd_file.read(READABLEBUFFER_SIZE)
                        if not chunk:
                            break
                        flash_file.write(chunk)

            # Save SIG .mpy.sig
            with open(
                flash_path_prefix + filename_flash + SIGNATURE_FILE_EXTENSION,
                "wb",
                buffering=0,
            ) as kapp_sig_file:
                kapp_sig_file.write(sig_data)

        del sig_data
        import gc

        gc.collect()

        clean_name = filename_flash[:-4]
        return self.execute_flash_kapp(clean_name)
