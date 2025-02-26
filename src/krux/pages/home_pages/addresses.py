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

import gc
from ...display import BOTTOM_PROMPT_LINE
from ...krux_settings import t
from ...settings import THIN_SPACE
from ...qr import FORMAT_NONE
from .. import (
    Page,
    Menu,
    MENU_CONTINUE,
    MENU_EXIT,
)

SCAN_ADDRESS_LIMIT = 50


class Addresses(Page):
    """UI to show and scan wallet addresses"""

    def addresses_menu(self):
        """Handler for the 'address' menu item"""
        # only show address for single-sig or multisig with wallet output descriptor loaded
        if not self.ctx.wallet.is_loaded() and (
            self.ctx.wallet.is_multisig() or self.ctx.wallet.is_miniscript()
        ):
            self.flash_error(t("Please load a wallet output descriptor"))
            return MENU_CONTINUE

        submenu = Menu(
            self.ctx,
            [
                (t("Scan Address"), self.pre_scan_address),
                (t("Receive Addresses"), self.list_address_type),
                (t("Change Addresses"), lambda: self.list_address_type(1)),
            ],
        )
        submenu.run_loop()
        return MENU_CONTINUE

    def list_address_type(self, addr_type=0):
        """Handler for the 'receive addresses' or 'change addresses' menu item"""
        if self.ctx.wallet.is_multisig() and not self.ctx.wallet.is_loaded():
            return MENU_CONTINUE

        loading_txt = (
            t("Loading change addresses..")
            if addr_type == 1
            else t("Loading receive addresses..")
        )
        max_addresses = self.ctx.display.max_menu_lines() - 3
        address_index = 0
        while True:
            items = []
            if address_index >= max_addresses:
                items.append(
                    (
                        "%d..%d" % (address_index - max_addresses, address_index - 1),
                        lambda: MENU_EXIT,
                    )
                )

            self.ctx.display.clear()
            self.ctx.display.draw_centered_text(loading_txt)
            addresses = self.ctx.wallet.obtain_addresses(
                address_index, limit=max_addresses, branch_index=addr_type
            )
            for addr in addresses:
                pos_str = str(address_index) + "." + THIN_SPACE
                qr_title = pos_str + addr
                items.append(
                    (
                        self.fit_to_line(addr, pos_str, fixed_chars=3),
                        lambda address=addr, title=qr_title: self.show_address(
                            address, title
                        ),
                    )
                )
                address_index += 1

            items.append(
                (
                    "%d..%d" % (address_index, address_index + max_addresses - 1),
                    lambda: MENU_EXIT,
                )
            )

            submenu = Menu(self.ctx, items)
            stay_on_this_addr_menu = True
            while stay_on_this_addr_menu:
                index, _ = submenu.run_loop()

                if index == len(submenu.menu) - 1:  # Back
                    del submenu, items
                    gc.collect()
                    return MENU_CONTINUE
                if index == len(submenu.menu) - 2:  # Next
                    stay_on_this_addr_menu = False
                if index == 0 and address_index > max_addresses:  # Prev
                    stay_on_this_addr_menu = False
                    address_index -= 2 * max_addresses

    def show_address(self, addr, title="", quick_exit=False):
        """Show addr provided as a QRCode"""
        from ..qr_view import SeedQRView

        seed_qr_view = SeedQRView(self.ctx, data=addr, title=title)
        seed_qr_view.display_qr(
            allow_export=True, transcript_tools=False, quick_exit=quick_exit
        )
        return MENU_CONTINUE

    def pre_scan_address(self):
        """Handler for the 'scan address' menu item"""

        submenu = Menu(
            self.ctx,
            [
                (t("Receive"), self.scan_address),
                (t("Change"), lambda: self.scan_address(1)),
            ],
        )
        submenu.run_loop()
        return MENU_CONTINUE

    def scan_address(self, addr_type=0):
        """Handler for the 'receive' or 'change' menu item"""
        from ..qr_capture import QRCodeCapture

        qr_capture = QRCodeCapture(self.ctx)
        data, qr_format = qr_capture.qr_capture_loop()
        if data is None or qr_format != FORMAT_NONE:
            self.flash_error(t("Failed to load"))
            return MENU_CONTINUE

        addr = None
        try:
            from ...wallet import parse_address

            addr = parse_address(data)
        except:
            self.flash_error(t("Invalid address"))
            return MENU_CONTINUE

        self.show_address(data, title=addr, quick_exit=True)

        if self.ctx.wallet.is_loaded() or not self.ctx.wallet.is_multisig():
            self.ctx.display.clear()
            if not self.prompt(
                t("Check that address belongs to this wallet?"),
                self.ctx.display.height() // 2,
            ):
                return MENU_CONTINUE

            checking_match_txt = t("Verifying..") + " " + t("%d to %d")
            checked_no_match_txt = t("Checked %d addresses with no matches.")
            is_valid_txt = "%s\n\n" + t("is a valid address!")
            not_found_txt = "%s\n\n" + t("was NOT FOUND in the first %d addresses")

            found = False
            num_checked = 0
            while not found:
                self.ctx.display.clear()
                self.ctx.display.draw_centered_text(
                    checking_match_txt
                    % (num_checked, num_checked + SCAN_ADDRESS_LIMIT - 1)
                )
                for some_addr in self.ctx.wallet.obtain_addresses(
                    num_checked, limit=SCAN_ADDRESS_LIMIT, branch_index=addr_type
                ):
                    num_checked += 1

                    found = addr == some_addr
                    if found:
                        break

                gc.collect()

                if not found:
                    self.ctx.display.clear()
                    self.ctx.display.draw_centered_text(
                        checked_no_match_txt % num_checked
                    )
                    if not self.prompt(t("Try more?"), BOTTOM_PROMPT_LINE):
                        break

            self.ctx.display.clear()
            result_message = (
                is_valid_txt % (str(num_checked - 1) + ". \n\n" + addr)
                if found
                else not_found_txt % (addr, num_checked)
            )
            self.ctx.display.draw_centered_text(result_message)
            self.ctx.input.wait_for_button()
        return MENU_CONTINUE
