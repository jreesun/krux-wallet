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
import math
import time
import board
import lcd
import _thread
from .keypads import Keypad
from ..themes import theme, WHITE, GREEN, DARKGREY
from ..input import (
    BUTTON_ENTER,
    BUTTON_PAGE,
    BUTTON_PAGE_PREV,
    BUTTON_TOUCH,
    SWIPE_DOWN,
    SWIPE_UP,
    ONE_MINUTE,
)
from ..display import (
    DEFAULT_PADDING,
    MINIMAL_PADDING,
    MINIMAL_DISPLAY,
    FLASH_MSG_TIME,
    FONT_HEIGHT,
    FONT_WIDTH,
    NARROW_SCREEN_WITH,
    STATUS_BAR_HEIGHT,
)
from ..qr import to_qr_codes
from ..krux_settings import t, Settings
from ..sd_card import SDHandler

MENU_CONTINUE = 0
MENU_EXIT = 1
MENU_SHUTDOWN = 2

ESC_KEY = 1
FIXED_KEYS = 3  # 'More' key only appears when there are multiple keysets

SHUTDOWN_WAIT_TIME = 300

TOGGLE_BRIGHTNESS = (BUTTON_PAGE, BUTTON_PAGE_PREV)
PROCEED = (BUTTON_ENTER, BUTTON_TOUCH)

LETTERS = "abcdefghijklmnopqrstuvwxyz"
UPPERCASE_LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
NUM_SPECIAL_1 = "1234567890 !#$%&'()*"
NUM_SPECIAL_2 = '+,-./:;<=>?@[\\]^_"{|}~'
NUM_SPECIAL_3 = " !#$%&'()*"  # NUM_SPECIAL_1 without numbers
DIGITS = "1234567890"

BATTERY_WIDTH = 22
BATTERY_HEIGHT = 7

LOAD_FROM_CAMERA = 0
LOAD_FROM_SD = 1


class Page:
    """Represents a page in the app, with helper methods for common display and
    input operations.

    Must be subclassed.
    """

    def __init__(self, ctx, menu=None):
        self.ctx = ctx
        self.menu = menu
        # context has its own keypad mapping in case touch is not used
        self.y_keypad_map = []
        self.x_keypad_map = []

    def esc_prompt(self):
        """Prompts user for leaving"""
        self.ctx.display.clear()
        answer = self.prompt(t("Are you sure?"), self.ctx.display.height() // 2)
        if self.ctx.input.touch is not None:
            self.ctx.input.touch.clear_regions()
        if answer:
            return ESC_KEY
        return None

    def load_method(self):
        """Prompts user to choose a method to load data from"""
        load_menu = Menu(
            self.ctx,
            [
                (t("Load from camera"), lambda: None),
                (
                    t("Load from SD card"),
                    None if not self.has_sd_card() else lambda: None,
                ),
            ],
            back_status=lambda: None,
        )
        index, _ = load_menu.run_loop()
        return index

    def flash_text(
        self,
        text,
        color=theme.fg_color,
        duration=FLASH_MSG_TIME,
    ):
        """Flashes text centered on the display for duration ms"""
        self.ctx.display.flash_text(text, color, duration)
        # Discard button presses that occurred during the message
        self.ctx.input.reset_ios_state()

    def flash_error(self, text):
        """Flashes text centered on the display for duration ms"""
        self.flash_text(text, theme.error_color)

    def capture_from_keypad(
        self,
        title,
        keysets,
        autocomplete_fn=None,
        possible_keys_fn=None,
        delete_key_fn=None,
        progress_bar_fn=None,
        go_on_change=False,
        starting_buffer="",
        esc_prompt=True,
    ):
        """Displays a key pad and captures a series of keys until the user returns.
        Returns a string.
        """
        buffer = starting_buffer
        pad = Keypad(self.ctx, keysets, possible_keys_fn)
        big_title = len(self.ctx.display.to_lines(title)) > 1
        while True:
            self.ctx.display.clear()
            offset_y = MINIMAL_PADDING if big_title else DEFAULT_PADDING
            if lcd.string_width_px(buffer) < self.ctx.display.width():
                self.ctx.display.draw_hcentered_text(title, offset_y)
                if big_title:
                    offset_y += 2 * FONT_HEIGHT
                else:
                    offset_y += FONT_HEIGHT * 3 // 2
            self.ctx.display.draw_hcentered_text(buffer, offset_y)

            if progress_bar_fn:
                progress_bar_fn()
            pad.compute_possible_keys(buffer)
            pad.get_valid_index()
            pad.draw_keys()
            pad.draw_keyset_index()
            btn = self.ctx.input.wait_for_button()
            if btn == BUTTON_TOUCH:
                btn = pad.touch_to_physical()
            if btn == BUTTON_ENTER:
                pad.moving_forward = True
                changed = False
                if pad.cur_key_index == pad.del_index:
                    if delete_key_fn is not None:
                        buffer = delete_key_fn(buffer)
                    else:
                        buffer = buffer[: len(buffer) - 1]
                    changed = True
                elif pad.cur_key_index == pad.esc_index:
                    if esc_prompt:
                        if self.esc_prompt() == ESC_KEY:
                            return ESC_KEY
                    else:
                        return ESC_KEY
                    # remap keypad touch array
                    pad.map_keys_array(pad.width, pad.height)
                elif pad.cur_key_index == pad.go_index:
                    break
                elif pad.cur_key_index == pad.more_index:
                    pad.next_keyset()
                elif pad.cur_key_index < len(pad.keys):
                    buffer += pad.keys[pad.cur_key_index]
                    changed = True

                    # Don't autocomplete if deleting
                    if autocomplete_fn is not None:
                        new_buffer = autocomplete_fn(buffer)
                        if new_buffer is not None:
                            buffer = new_buffer
                            break  # auto-Go for load "Via Text"

                if changed and go_on_change:
                    break
            else:
                pad.navigate(btn)

        if self.ctx.input.touch is not None:
            self.ctx.input.touch.clear_regions()
        return buffer

    def display_qr_codes(self, data, qr_format, title=""):
        """Displays a QR code or an animated series of QR codes to the user, encoding them
        in the specified format
        """
        done = False
        i = 0
        code_generator = to_qr_codes(data, self.ctx.display.qr_data_width(), qr_format)
        self.ctx.display.clear()
        if theme.bg_color == WHITE:
            qr_foreground = WHITE
        else:
            qr_foreground = None
        extra_debounce_flag = True
        self.ctx.input.buttons_active = True
        while not done:
            code = None
            num_parts = 0
            btn = None
            try:
                code, num_parts = next(code_generator)
            except:
                code_generator = to_qr_codes(
                    data, self.ctx.display.qr_data_width(), qr_format
                )
                code, num_parts = next(code_generator)
            if qr_foreground:
                self.ctx.display.draw_qr_code(0, code, light_color=qr_foreground)
            else:
                self.ctx.display.draw_qr_code(0, code)
            subtitle = (
                t("Part") + "\n%d / %d" % (i + 1, num_parts) if not title else title
            )
            offset_y = self.ctx.display.qr_offset()
            if subtitle and self.ctx.display.height() > self.ctx.display.width():
                offset_y += FONT_HEIGHT
                # Clean area below QR code to refresh subtitle/part
                self.ctx.display.fill_rectangle(
                    0,
                    offset_y,
                    self.ctx.display.width(),
                    self.ctx.display.height() - offset_y,
                    theme.bg_color,
                )
                self.ctx.display.draw_hcentered_text(subtitle, offset_y)
                i = (i + 1) % num_parts
            if extra_debounce_flag:
                # Animated QR codes disable debounce
                # so this is required to avoid double presses
                time.sleep_ms(self.ctx.input.debounce_value)
                self.ctx.input.reset_ios_state()
                extra_debounce_flag = False
            btn = self.ctx.input.wait_for_button(num_parts == 1)
            if btn in TOGGLE_BRIGHTNESS:
                if qr_foreground == WHITE:
                    qr_foreground = DARKGREY
                elif not qr_foreground:
                    qr_foreground = WHITE
                elif qr_foreground == DARKGREY:
                    qr_foreground = None
                extra_debounce_flag = True
            elif btn in PROCEED:
                if self.ctx.input.touch is not None:
                    self.ctx.input.buttons_active = False
                done = True
            # interval done in input.py using timers

    def display_mnemonic(
        self, mnemonic: str, suffix="", display_mnemonic: str = None, fingerprint=""
    ):
        """Displays the 12 or 24-word list of words to the user"""
        from ..wallet import is_double_mnemonic

        if display_mnemonic is None:
            display_mnemonic = mnemonic
        words = display_mnemonic.split(" ")
        word_list = [
            str(i + 1) + "." + ("  " if i + 1 < 10 else " ") + word
            for i, word in enumerate(words)
        ]

        if is_double_mnemonic(mnemonic):
            suffix += "*"
        if fingerprint:
            fingerprint = "\n" + fingerprint
        header = "BIP39" + " " + suffix + fingerprint
        self.ctx.display.clear()
        self.ctx.display.draw_hcentered_text(header)
        starting_y_offset = DEFAULT_PADDING // 4 + (
            len(self.ctx.display.to_lines(header)) * FONT_HEIGHT + FONT_HEIGHT
        )
        for i, word in enumerate(word_list[:12]):
            offset_x = DEFAULT_PADDING
            offset_y = starting_y_offset + (i * FONT_HEIGHT)
            self.ctx.display.draw_string(offset_x, offset_y, word)
        if len(word_list) > 12:
            if board.config["type"] == "m5stickv":
                self.ctx.input.wait_for_button()
                self.ctx.display.clear()
                self.ctx.display.draw_hcentered_text(header)
                for i, word in enumerate(word_list[12:]):
                    offset_x = DEFAULT_PADDING
                    offset_y = starting_y_offset + (i * FONT_HEIGHT)
                    self.ctx.display.draw_string(offset_x, offset_y, word)
            else:
                for i, word in enumerate(word_list[12:]):
                    offset_x = self.ctx.display.width() // 2
                    offset_y = starting_y_offset + (i * FONT_HEIGHT)
                    self.ctx.display.draw_string(offset_x, offset_y, word)

    def print_prompt(self, text):
        """Prompts the user to print a QR code in the specified format
        if a printer is connected
        """
        if not self.has_printer():
            return False

        self.ctx.display.clear()
        if self.prompt(
            (text + "\n\n%s\n\n") % Settings().hardware.printer.driver,
            self.ctx.display.height() // 2,
        ):
            return True
        return False

    def prompt(self, text, offset_y=0):
        """Prompts user to answer Yes or No"""
        # Go up if question has multiple lines
        offset_y -= (len(self.ctx.display.to_lines(text)) - 1) * FONT_HEIGHT
        self.ctx.display.draw_hcentered_text(
            text, offset_y, theme.fg_color, theme.bg_color
        )
        self.y_keypad_map = []
        self.x_keypad_map = []
        if MINIMAL_DISPLAY:
            return self.ctx.input.wait_for_button() == BUTTON_ENTER
        offset_y += (len(self.ctx.display.to_lines(text)) + 1) * FONT_HEIGHT
        self.x_keypad_map.append(0)
        self.x_keypad_map.append(self.ctx.display.width() // 2)
        self.x_keypad_map.append(self.ctx.display.width())
        y_key_map = offset_y - (3 * FONT_HEIGHT // 2)
        self.y_keypad_map.append(y_key_map)
        y_key_map += 4 * FONT_HEIGHT
        y_key_map = min(y_key_map, self.ctx.display.height())
        self.y_keypad_map.append(y_key_map)
        if self.ctx.input.touch is not None:
            self.ctx.input.touch.clear_regions()
            self.ctx.input.touch.x_regions = self.x_keypad_map
            self.ctx.input.touch.y_regions = self.y_keypad_map

        btn = None
        answer = True
        while btn != BUTTON_ENTER:
            offset_x = (self.ctx.display.width() * 3) // 4
            offset_x -= (lcd.string_width_px(t("Yes"))) // 2
            self.ctx.display.draw_string(
                offset_x, offset_y, t("Yes"), theme.go_color, theme.bg_color
            )
            offset_x = self.ctx.display.width() // 4
            offset_x -= (lcd.string_width_px(t("No"))) // 2
            self.ctx.display.draw_string(
                offset_x, offset_y, t("No"), theme.no_esc_color, theme.bg_color
            )
            if self.ctx.input.buttons_active:
                if answer:
                    self.ctx.display.outline(
                        self.ctx.display.width() // 2,
                        offset_y - FONT_HEIGHT // 2,
                        self.ctx.display.usable_width() // 2,
                        2 * FONT_HEIGHT - 2,
                        theme.go_color,
                    )
                else:
                    self.ctx.display.outline(
                        DEFAULT_PADDING,
                        offset_y - FONT_HEIGHT // 2,
                        self.ctx.display.usable_width() // 2,
                        2 * FONT_HEIGHT - 2,
                        theme.no_esc_color,
                    )
            elif self.ctx.input.touch is not None:
                self.ctx.display.draw_vline(
                    self.ctx.display.width() // 2,
                    self.y_keypad_map[0] + FONT_HEIGHT,
                    2 * FONT_HEIGHT,
                    theme.frame_color,
                )
            btn = self.ctx.input.wait_for_button()
            if btn in (BUTTON_PAGE, BUTTON_PAGE_PREV):
                answer = not answer
                # erase yes/no area for next loop
                self.ctx.display.fill_rectangle(
                    0,
                    offset_y - FONT_HEIGHT,
                    self.ctx.display.width(),
                    3 * FONT_HEIGHT,
                    theme.bg_color,
                )
            elif btn == BUTTON_TOUCH:
                self.ctx.input.touch.clear_regions()
                # index 0 = No
                # index 1 = Yes
                if self.ctx.input.touch.current_index():
                    return True
                return False
        # BUTTON_ENTER
        return answer

    def fit_to_line(self, text, prefix="", fixed_chars=0, crop_middle=True):
        """Fits text with prefix plus fixed_chars at the beginning into one line,
        removing the central content and leaving the ends"""

        add_chars_amount = self.ctx.display.usable_width() // FONT_WIDTH
        if len(text) + len(prefix) <= add_chars_amount:
            return prefix + text
        if not crop_middle:  # Crop from the end
            return prefix + text[: add_chars_amount - 2] + ".."
        add_chars_amount -= len(prefix) + fixed_chars + 2
        add_chars_amount //= 2
        return (
            prefix
            + text[: add_chars_amount + fixed_chars]
            + ".."
            + text[-add_chars_amount:]
        )

    def has_printer(self):
        """Checks if the device has a printer setup"""
        return Settings().hardware.printer.driver != "none"

    def has_sd_card(self):
        """Checks if the device has a SD card inserted"""
        self.ctx.display.clear()
        self.ctx.display.draw_centered_text(t("Checking for SD card.."))
        try:
            # Check for SD hot-plug
            with SDHandler():
                return True
        except:
            return False

    def shutdown_menu_item(self, ctx):
        """Returns the Shutdown or Reboot Menu item"""
        label = t("Shutdown") if ctx.power_manager.has_battery() else t("Reboot")
        return (label, self.shutdown)

    def shutdown(self):
        """Handler for the 'shutdown' menu item"""
        if self.prompt(t("Are you sure?"), self.ctx.display.height() // 2):
            self.ctx.display.clear()
            self.ctx.display.draw_centered_text(t("Shutting down.."))
            time.sleep_ms(SHUTDOWN_WAIT_TIME)
            return MENU_SHUTDOWN
        return MENU_CONTINUE

    def run(self, start_from_index=None):
        """Runs the page's menu loop"""
        _, status = self.menu.run_loop(start_from_index)
        return status != MENU_SHUTDOWN


class ListView:
    """Acts as a fixed-size, sliding window over an underlying list"""

    def __init__(self, lst, max_size):
        self.list = lst
        self.max_size = max_size
        self.offset = 0
        self.iter_index = 0

    def __getitem__(self, key):
        return self.list[self.offset + key]

    def __iter__(self):
        self.iter_index = 0
        return self

    def __next__(self):
        if self.iter_index < len(self):
            self.iter_index += 1
            return self.__getitem__(self.iter_index - 1)
        raise StopIteration

    def __len__(self):
        return min(self.max_size, len(self.list[self.offset :]))

    def move_forward(self):
        """Slides the window one size-increment forward, wrapping around"""
        self.offset += self.max_size
        if self.offset >= len(self.list):
            self.offset = 0

    def move_backward(self):
        """Slides the window one size-increment backward, wrapping around"""
        self.offset -= self.max_size
        if self.offset < 0:
            self.offset = int(
                (math.ceil(len(self.list) / self.max_size) - 1) * self.max_size
            )

    def index(self, i):
        """Returns the true index of an element in the underlying list"""
        return self.offset + i


class Menu:
    """Represents a menu that can render itself to the screen, handle item selection,
    and invoke menu item callbacks that return a status
    """

    def __init__(
        self,
        ctx,
        menu,
        offset=None,
        disable_statusbar=False,
        back_label="Back",
        back_status=lambda: MENU_EXIT,
    ):
        self.ctx = ctx
        self.menu = menu
        if back_label:
            back_label = t("Back") if back_label == "Back" else back_label
            self.menu += [("< " + back_label, back_status)]

        self.disable_statusbar = disable_statusbar
        if offset is None:
            # Default offset for status bar
            self.menu_offset = STATUS_BAR_HEIGHT
        else:
            # Always diasble status bar if menu has non standard offset
            self.disable_statusbar = True
            self.menu_offset = offset
        max_viewable = min(
            self.ctx.display.max_menu_lines(self.menu_offset),
            len(self.menu),
        )
        self.menu_view = ListView(self.menu, max_viewable)

    def screensaver(self):
        """Loads and starts screensaver"""
        from .screensaver import ScreenSaver

        screen_saver = ScreenSaver(self.ctx)
        screen_saver.start()

    def run_loop(self, start_from_index=None):
        """Runs the menu loop until one of the menu items returns either a MENU_EXIT
        or MENU_SHUTDOWN status
        """
        start_from_submenu = False
        selected_item_index = 0
        if start_from_index is not None:
            start_from_submenu = True
            selected_item_index = start_from_index
        while True:
            gc.collect()
            if self.menu_offset > STATUS_BAR_HEIGHT:
                # Clear only the menu area
                self.ctx.display.fill_rectangle(
                    0,
                    self.menu_offset,
                    self.ctx.display.width(),
                    self.ctx.display.height() - self.menu_offset,
                    theme.bg_color,
                )
            else:
                self.ctx.display.clear()
            if self.ctx.input.touch is not None:
                self._draw_touch_menu(selected_item_index)
            else:
                self._draw_menu(selected_item_index)

            self.draw_status_bar()
            self.ctx.input.reset_ios_state()

            if start_from_submenu:
                status = self._clicked_item(selected_item_index)
                if status != MENU_CONTINUE:
                    return (self.menu_view.index(selected_item_index), status)
                start_from_submenu = False
            else:
                btn = self.ctx.input.wait_for_button(
                    # Block if screen saver not active
                    block=Settings().appearance.screensaver_time == 0,
                    wait_duration=Settings().appearance.screensaver_time * ONE_MINUTE,
                )
                if self.ctx.input.touch is not None:
                    if btn == BUTTON_TOUCH:
                        selected_item_index = self.ctx.input.touch.current_index()
                        btn = BUTTON_ENTER
                    self.ctx.input.touch.clear_regions()
                if btn == BUTTON_ENTER:
                    status = self._clicked_item(selected_item_index)
                    if status != MENU_CONTINUE:
                        return (self.menu_view.index(selected_item_index), status)
                elif btn == BUTTON_PAGE:
                    selected_item_index = (selected_item_index + 1) % len(
                        self.menu_view
                    )
                    if selected_item_index == 0:
                        self.menu_view.move_forward()
                elif btn == BUTTON_PAGE_PREV:
                    selected_item_index = (selected_item_index - 1) % len(
                        self.menu_view
                    )
                    if selected_item_index == len(self.menu_view) - 1:
                        self.menu_view.move_backward()
                        # Update selected item index to be the last viewable item,
                        # which may be a different index than before we moved backward
                        selected_item_index = len(self.menu_view) - 1
                elif btn == SWIPE_UP:
                    self.menu_view.move_forward()
                elif btn == SWIPE_DOWN:
                    self.menu_view.move_backward()
                elif btn is None and self.menu_offset == STATUS_BAR_HEIGHT:
                    # Activates screensaver if there's no info_box(other things draw on the screen)
                    self.screensaver()

    def _clicked_item(self, selected_item_index):
        if self.menu_view[selected_item_index][1] is None:
            return MENU_CONTINUE
        try:
            self.ctx.display.clear()
            status = self.menu_view[selected_item_index][1]()
            if status != MENU_CONTINUE:
                return status
        except Exception as e:
            self.ctx.display.to_portrait()
            self.ctx.display.clear()
            self.ctx.display.draw_centered_text(
                t("Error:") + "\n%s" % repr(e), theme.error_color
            )
            self.ctx.input.wait_for_button()
        return MENU_CONTINUE

    def draw_status_bar(self):
        """Draws a status bar along the top of the UI"""
        if not self.disable_statusbar:
            self.ctx.display.fill_rectangle(
                0,
                0,
                self.ctx.display.width(),
                STATUS_BAR_HEIGHT,
                theme.info_bg_color,
            )
            self.draw_network_indicator()
            self.draw_wallet_indicator()
            if self.ctx.power_manager.has_battery():
                _thread.start_new_thread(self.draw_battery_indicator, ())

    #     self.draw_ram_indicator()

    # def draw_ram_indicator(self):
    #     """Draws the amount of free RAM in the status bar +recently-collected"""

    #     def strnum(_in):
    #         large_units = ("", "K", "M")

    #         value = _in
    #         for i in range(len(large_units)):
    #             unit = large_units[i]
    #             if value < 2**10:
    #                 break
    #             if i + 1 < len(large_units):
    #                 value /= 2**10

    #         if value == int(value):
    #             fmt = "%d" + unit
    #         else:
    #             if value < 1:
    #                 fmt = "%0.3f" + unit
    #             elif value < 10:
    #                 fmt = "%.2f" + unit
    #             elif value < 100:
    #                 fmt = "%.1f" + unit
    #             else:
    #                 fmt = "%d" + unit

    #         return fmt % value

    #     pre_collect = gc.mem_free()
    #     gc.collect()
    #     post_collect = gc.mem_free()
    #     ram_text = (
    #         "RAM: " + strnum(post_collect) + " +" + strnum(post_collect - pre_collect)
    #     )
    #     self.ctx.display.draw_string(12, 0, ram_text, GREEN)

    def draw_battery_indicator(self):
        """Draws a battery icon with depletion proportional to battery voltage"""
        charge = self.ctx.power_manager.battery_charge_remaining()
        if self.ctx.power_manager.usb_connected():
            battery_color = theme.go_color
        else:
            if charge < 0.3:
                battery_color = theme.error_color
            else:
                battery_color = theme.fg_color

        # Draw (filled) outline of battery in top-right corner of display
        x_padding = FONT_HEIGHT // 3
        y_padding = (STATUS_BAR_HEIGHT // 2) - (BATTERY_HEIGHT // 2)
        self.ctx.display.outline(
            self.ctx.display.width() - x_padding - BATTERY_WIDTH,
            y_padding,
            BATTERY_WIDTH,
            BATTERY_HEIGHT,
            battery_color,
        )
        self.ctx.display.fill_rectangle(
            self.ctx.display.width() - x_padding + 1,
            y_padding + 2,
            2,
            BATTERY_HEIGHT - 3,
            battery_color,
        )

        # Indicate how much battery is depleted
        charge_length = int((BATTERY_WIDTH - 3) * charge)
        self.ctx.display.fill_rectangle(
            self.ctx.display.width() - x_padding - BATTERY_WIDTH + 2,
            y_padding + 2,
            charge_length,
            BATTERY_HEIGHT - 3,
            battery_color,
        )

    def draw_wallet_indicator(self):
        """Draws wallet fingerprint or BIP85 child at top if wallet is loaded"""
        if self.ctx.is_logged_in():
            if self.ctx.display.width() > NARROW_SCREEN_WITH:
                self.ctx.display.draw_hcentered_text(
                    self.ctx.wallet.key.fingerprint_hex_str(True),
                    STATUS_BAR_HEIGHT - FONT_HEIGHT - 1,
                    theme.highlight_color,
                    theme.info_bg_color,
                )
            else:
                self.ctx.display.draw_string(
                    24,
                    STATUS_BAR_HEIGHT - FONT_HEIGHT - 1,
                    self.ctx.wallet.key.fingerprint_hex_str(True),
                    theme.highlight_color,
                    theme.info_bg_color,
                )

    def draw_network_indicator(self):
        """Draws test at top if testnet is enabled"""
        if self.ctx.is_logged_in() and self.ctx.wallet.key.network["name"] == "Testnet":
            if self.ctx.display.width() > NARROW_SCREEN_WITH:
                self.ctx.display.draw_string(
                    12,
                    STATUS_BAR_HEIGHT - FONT_HEIGHT - 1,
                    "Test",
                    GREEN,
                    theme.info_bg_color,
                )
            else:
                self.ctx.display.draw_string(
                    6,
                    STATUS_BAR_HEIGHT - FONT_HEIGHT - 1,
                    "T",
                    GREEN,
                    theme.info_bg_color,
                )

    def _draw_touch_menu(self, selected_item_index):
        # map regions with dynamic height to fill screen
        self.ctx.input.touch.clear_regions()
        offset_y = 0
        Page.y_keypad_map = [offset_y]
        for menu_item in self.menu_view:
            offset_y += len(self.ctx.display.to_lines(menu_item[0])) + 1
            Page.y_keypad_map.append(offset_y)
        height_multiplier = self.ctx.display.height()
        height_multiplier -= self.menu_offset  # Top offset
        height_multiplier -= DEFAULT_PADDING  # Bottom padding
        height_multiplier /= max(offset_y, 1)
        Page.y_keypad_map = [
            int(n * height_multiplier) + self.menu_offset for n in Page.y_keypad_map
        ]
        # Expand last region to the bottom of the screen
        Page.y_keypad_map[-1] = self.ctx.display.height()
        self.ctx.input.touch.y_regions = Page.y_keypad_map

        # draw dividers and outline
        for i, y in enumerate(Page.y_keypad_map[:-1]):
            if i and not self.ctx.input.buttons_active:
                self.ctx.display.draw_line(
                    0, y, self.ctx.display.width(), y, theme.frame_color
                )

        # draw centralized strings in regions
        for i, menu_item in enumerate(self.menu_view):
            menu_item_lines = self.ctx.display.to_lines(menu_item[0])
            offset_y = Page.y_keypad_map[i + 1] - Page.y_keypad_map[i]
            offset_y -= len(menu_item_lines) * FONT_HEIGHT
            if i == len(self.menu_view) - 1:
                # Compensate for the expanded last region
                offset_y -= DEFAULT_PADDING
            offset_y //= 2
            offset_y += Page.y_keypad_map[i]
            fg_color = (
                theme.fg_color if menu_item[1] is not None else theme.disabled_color
            )
            if selected_item_index == i and self.ctx.input.buttons_active:
                self.ctx.display.fill_rectangle(
                    0,
                    offset_y + 1 - FONT_HEIGHT // 2,
                    self.ctx.display.width(),
                    (len(menu_item_lines) + 1) * FONT_HEIGHT,
                    fg_color,
                )
            for j, text in enumerate(menu_item_lines):
                if selected_item_index == i and self.ctx.input.buttons_active:
                    self.ctx.display.draw_hcentered_text(
                        text,
                        offset_y + FONT_HEIGHT * j,
                        theme.bg_color,
                        fg_color,
                    )
                else:
                    self.ctx.display.draw_hcentered_text(
                        text, offset_y + FONT_HEIGHT * j, fg_color
                    )

    def _draw_menu(self, selected_item_index):
        extra_lines = 0
        for menu_item in self.menu_view:
            # Count extra lines for multi-line menu items
            extra_lines += len(self.ctx.display.to_lines(menu_item[0])) - 1
        if self.menu_offset > STATUS_BAR_HEIGHT:
            offset_y = self.menu_offset + FONT_HEIGHT
        else:
            offset_y = len(self.menu_view) * 2
            offset_y += extra_lines
            offset_y *= FONT_HEIGHT
            offset_y = self.ctx.display.height() - offset_y
            offset_y //= 2
            offset_y += FONT_HEIGHT // 2
        offset_y = max(offset_y, STATUS_BAR_HEIGHT)
        # Usable pixels height
        items_pad = self.ctx.display.height() - STATUS_BAR_HEIGHT
        # Usable pixes for padding
        items_pad -= (len(self.menu_view) + extra_lines) * FONT_HEIGHT
        # Ensure padding is positive
        items_pad = max(items_pad, 0)
        # Padding between items
        items_pad //= max(len(self.menu_view) - 1, 1)
        # Limit padding to font height
        items_pad = min(items_pad, FONT_HEIGHT)
        for i, menu_item in enumerate(self.menu_view):
            fg_color = (
                theme.fg_color if menu_item[1] is not None else theme.disabled_color
            )
            menu_item_lines = self.ctx.display.to_lines(menu_item[0])
            delta_y = len(menu_item_lines) * FONT_HEIGHT
            delta_y += items_pad
            if selected_item_index == i:
                self.ctx.display.fill_rectangle(
                    0,
                    offset_y + 1 - items_pad // 2,
                    self.ctx.display.width(),
                    delta_y - 2,
                    fg_color,
                )
                for j, text in enumerate(menu_item_lines):
                    self.ctx.display.draw_hcentered_text(
                        text,
                        offset_y + FONT_HEIGHT * j,
                        theme.bg_color,
                        fg_color,
                    )
            else:
                for j, text in enumerate(menu_item_lines):
                    self.ctx.display.draw_hcentered_text(
                        text, offset_y + FONT_HEIGHT * j, fg_color
                    )
            offset_y += delta_y


def choose_len_mnemonic(ctx, extra_option=""):
    """Reusable '12 or 24 words?" menu choice"""
    items = [
        (t("12 words"), lambda: 12),
        (t("24 words"), lambda: 24),
    ]
    if extra_option:
        items += [(extra_option, lambda: 48)]
    submenu = Menu(
        ctx,
        items,
        back_status=lambda: None,
    )
    _, num_words = submenu.run_loop()
    ctx.display.clear()
    return num_words


def proceed_menu(
    ctx, y_offset=0, menu_index=None, proceed_txt="Go", esc_txt="Esc", go_enabled=True
):
    """Reusable 'Esc' and 'Go' menu choice"""

    go_x_offset = ctx.display.width() // 2
    go_x_offset -= lcd.string_width_px(proceed_txt)
    go_x_offset //= 2
    go_x_offset += ctx.display.width() // 2
    esc_x_offset = ctx.display.width() // 2
    esc_x_offset -= lcd.string_width_px(esc_txt)
    esc_x_offset //= 2
    go_esc_y_offset = ctx.display.height()
    go_esc_y_offset -= y_offset + FONT_HEIGHT + MINIMAL_PADDING
    go_esc_y_offset //= 2
    go_esc_y_offset += y_offset
    if menu_index == 0 and ctx.input.buttons_active:
        ctx.display.outline(
            DEFAULT_PADDING,
            go_esc_y_offset - FONT_HEIGHT // 2,
            ctx.display.width() // 2 - 2 * DEFAULT_PADDING,
            FONT_HEIGHT + FONT_HEIGHT,
            theme.error_color,
        )
    ctx.display.draw_string(esc_x_offset, go_esc_y_offset, esc_txt, theme.error_color)
    if menu_index == 1 and ctx.input.buttons_active:
        ctx.display.outline(
            ctx.display.width() // 2 + DEFAULT_PADDING,
            go_esc_y_offset - FONT_HEIGHT // 2,
            ctx.display.width() // 2 - 2 * DEFAULT_PADDING,
            FONT_HEIGHT + FONT_HEIGHT,
            theme.go_color,
        )
    go_color = theme.go_color if go_enabled else theme.disabled_color
    ctx.display.draw_string(go_x_offset, go_esc_y_offset, proceed_txt, go_color)
    if not ctx.input.buttons_active:
        ctx.display.draw_vline(
            ctx.display.width() // 2,
            go_esc_y_offset,
            FONT_HEIGHT,
            theme.frame_color,
        )
