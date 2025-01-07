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
import board
import binascii
from .settings import (
    SettingsNamespace,
    CategorySetting,
    NumberSetting,
    SD_PATH,
    FLASH_PATH,
    MAIN_TXT,
    TEST_TXT,
    NAME_SINGLE_SIG,
    POLICY_TYPE_NAMES,
)
from .key import SCRIPT_LONG_NAMES

BAUDRATES = [1200, 2400, 4800, 9600, 19200, 38400, 57600, 115200]

TC_CODE_PATH = "/" + FLASH_PATH + "/tcc"
TC_CODE_PBKDF2_ITERATIONS = 100000

DEFAULT_LOCALE = "en-US"

DEFAULT_TX_PIN = (
    board.config["board_info"]["CONNEXT_A"]
    if "CONNEXT_A" in board.config["board_info"]
    else 35
)
DEFAULT_RX_PIN = (
    board.config["board_info"]["CONNEXT_B"]
    if "CONNEXT_B" in board.config["board_info"]
    else 34
)

# Encription Versions
PBKDF2_HMAC_ECB = 0
PBKDF2_HMAC_CBC = 1

THERMAL_ADAFRUIT_TXT = "thermal/adafruit"


def t(slug):
    """Translates a slug according to the current locale"""
    if not locale_control.translation:
        return slug
    slug_id = binascii.crc32(slug.encode("utf-8"))
    try:
        translation_index = locale_control.reference.index(slug_id)
    except:
        return slug
    return locale_control.translation[translation_index]


class LocaleControl:
    """Manages the current locale and available translations"""

    def __init__(self):
        self.reference = None
        self.translation = None
        self.locales = []
        self.update_locales()

    def update_locales(self):
        """Updates the list of available locales"""
        from .translations import available_languages

        self.locales = []
        self.locales.append(DEFAULT_LOCALE)
        self.locales.extend(available_languages)

    def load_locale(self, locale):
        """Loads translation based on the given locale"""

        if locale == DEFAULT_LOCALE:
            self.reference = None
            self.translation = None
            return
        module_path = "krux.translations.{}".format(locale[:2])
        translation_module = __import__(module_path)
        # Navigate to the nested module (translations.<locale>)
        for part in module_path.split(".")[1:]:
            translation_module = getattr(translation_module, part)

        self.translation = getattr(translation_module, "translation_array")
        if self.reference is None:
            from .translations import ref_array

            self.reference = ref_array


locale_control = LocaleControl()


class I18nSettings(SettingsNamespace):
    """I18n-specific settings"""

    namespace = "settings.i18n"
    locale = CategorySetting("locale", DEFAULT_LOCALE, locale_control.locales)

    def label(self, attr):
        """Returns a label for UI when given a setting name or namespace"""
        return {
            "locale": t("Locale"),
        }[attr]


class DefaultWallet(SettingsNamespace):
    """Bitcoin-specific settings"""

    namespace = "settings.wallet"
    network = CategorySetting("network", MAIN_TXT, [MAIN_TXT, TEST_TXT])
    policy_type = CategorySetting("policy_type", NAME_SINGLE_SIG, POLICY_TYPE_NAMES)
    script_type = CategorySetting(
        "script_type", "Native Segwit - 84", list(SCRIPT_LONG_NAMES.keys())
    )

    def label(self, attr):
        """Returns a label for UI when given a setting name or namespace"""
        return {
            "network": t("Network"),
            "policy_type": t("Policy Type"),
            "script_type": t("Script Type"),
        }[attr]


class ThermalSettings(SettingsNamespace):
    """Thermal printer settings"""

    namespace = "settings.printer.thermal"

    def __init__(self):
        self.adafruit = AdafruitPrinterSettings()

    def label(self, attr):
        """Returns a label for UI when given a setting name or namespace"""
        return {
            "adafruit": "Adafruit",
        }[attr]


class AdafruitPrinterSettings(SettingsNamespace):
    """Adafruit thermal printer settings"""

    namespace = "settings.printer.thermal.adafruit"
    baudrate = CategorySetting("baudrate", 9600, BAUDRATES)
    paper_width = NumberSetting(int, "paper_width", 384, [100, 1000])
    tx_pin = NumberSetting(int, "tx_pin", DEFAULT_TX_PIN, [0, 10000])
    rx_pin = NumberSetting(int, "rx_pin", DEFAULT_RX_PIN, [0, 10000])
    line_delay = NumberSetting(int, "line_delay", 20, [0, 255])
    scale = NumberSetting(int, "scale", 75, [25, 100])

    def label(self, attr):
        """Returns a label for UI when given a setting name or namespace"""
        return {
            "baudrate": t("Baudrate"),
            "paper_width": t("Paper Width"),
            "tx_pin": t("TX Pin"),
            "rx_pin": t("RX Pin"),
            "line_delay": t("Line Delay"),
            "scale": t("Scale"),
        }[attr]


class CNCSettings(SettingsNamespace):
    """CNC "printer" settings"""

    namespace = "settings.printer.cnc"
    invert = CategorySetting("invert", False, [False, True])
    cut_method = CategorySetting("cut_method", "spiral", ["spiral", "row"])
    unit = CategorySetting("unit", "in", ["in", "mm"])
    flute_diameter = NumberSetting(float, "flute_diameter", 0.02, [0.0001, 10000])
    plunge_rate = NumberSetting(float, "plunge_rate", 30, [0.0001, 10000])
    feed_rate = NumberSetting(float, "feed_rate", 65, [0.0001, 10000])
    cut_depth = NumberSetting(float, "cut_depth", 0.0625, [0.0001, 10000])
    depth_per_pass = NumberSetting(float, "depth_per_pass", 0.03125, [0.0001, 10000])
    part_size = NumberSetting(float, "part_size", 3.5, [0.0001, 10000])
    border_padding = NumberSetting(float, "border_padding", 0.0625, [0.0001, 10000])

    def __init__(self):
        self.grbl = GRBLSettings()

    def label(self, attr):
        """Returns a label for UI when given a setting name or namespace"""
        return {
            "invert": t("Invert"),
            "cut_method": t("Cut Method"),
            "unit": t("Unit"),
            "flute_diameter": t("Flute Diameter"),
            "plunge_rate": t("Plunge Rate"),
            "feed_rate": t("Feed Rate"),
            "cut_depth": t("Cut Depth"),
            "depth_per_pass": t("Depth Per Pass"),
            "part_size": t("Part Size"),
            "border_padding": t("Border Padding"),
            "grbl": "GRBL",
        }[attr]


class GRBLSettings(SettingsNamespace):
    """GRBL settings"""

    namespace = "settings.printer.cnc.grbl"
    baudrate = CategorySetting("baudrate", 115200, BAUDRATES)
    tx_pin = NumberSetting(int, "tx_pin", DEFAULT_TX_PIN, [0, 10000])
    rx_pin = NumberSetting(int, "rx_pin", DEFAULT_RX_PIN, [0, 10000])

    def label(self, attr):
        """Returns a label for UI when given a setting name or namespace"""
        return {
            "baudrate": t("Baudrate"),
            "tx_pin": t("TX Pin"),
            "rx_pin": t("RX Pin"),
        }[attr]


class PrinterSettings(SettingsNamespace):
    """Printer-specific settings"""

    PRINTERS = {
        "none": ("none", None),
        THERMAL_ADAFRUIT_TXT: ("thermal", "AdafruitPrinter"),
        "cnc/file": ("cnc", "FilePrinter"),
    }
    namespace = "settings.printer"
    driver = CategorySetting("driver", "none", list(PRINTERS.keys()))

    def __init__(self):
        self.thermal = ThermalSettings()
        self.cnc = CNCSettings()

    def label(self, attr):
        """Returns a label for UI when given a setting name or namespace"""
        return {
            "thermal": t("Thermal"),
            "driver": t("Driver"),
            "cnc": "CNC",
        }[attr]


class ButtonsSettings(SettingsNamespace):
    """Buttons debounce settings"""

    namespace = "settings.buttons"
    debounce = NumberSetting(int, "debounce", 100, [100, 500])

    def label(self, attr):
        """Returns a label for UI when given a setting name or namespace"""
        return {
            "debounce": t("Buttons Debounce"),
        }[attr]


class TouchSettings(SettingsNamespace):
    """Touch sensitivity settings"""

    namespace = "settings.touchscreen"
    threshold = NumberSetting(int, "threshold", 22, [10, 200])

    def label(self, attr):
        """Returns a label for UI when given a setting name or namespace"""
        return {
            "threshold": t("Touch Threshold"),
        }[attr]


class DisplayAmgSettings(SettingsNamespace):
    """Custom display settings for Maix Amigo"""

    namespace = "settings.display_amg"
    flipped_x_coordinates = CategorySetting("flipped_x", True, [False, True])
    inverted_colors = CategorySetting("inverted_colors", True, [False, True])
    bgr_colors = CategorySetting("bgr_colors", True, [False, True])
    lcd_type = CategorySetting("lcd_type", 0, [0, 1])

    def label(self, attr):
        """Returns a label for UI when given a setting name or namespace"""
        return {
            "flipped_x": t("Flipped X Coordinates"),
            "inverted_colors": t("Inverted Colors"),
            "bgr_colors": t("BGR Colors"),
            "lcd_type": t("LCD Type"),
        }[attr]


class DisplaySettings(SettingsNamespace):
    """Custom display settings for Maix Cube"""

    namespace = "settings.display"
    default_brightness = "1" if board.config["type"] == "m5stickv" else "3"
    brightness = CategorySetting(
        "brightness", default_brightness, ["1", "2", "3", "4", "5"]
    )

    def label(self, attr):
        """Returns a label for UI when given a setting name or namespace"""
        return {
            "brightness": t("Brightness"),
        }[attr]


class HardwareSettings(SettingsNamespace):
    """Hardware Related Settings"""

    namespace = "settings.hardware"

    def __init__(self):
        self.printer = PrinterSettings()
        self.buttons = ButtonsSettings()
        if board.config["type"] in ["amigo", "yahboom", "wonder_mv"]:
            self.touch = TouchSettings()
        if board.config["type"] == "amigo":
            self.display = DisplayAmgSettings()
        elif board.config["type"] in ["cube", "m5stickv", "wonder_mv"]:
            self.display = DisplaySettings()

    def label(self, attr):
        """Returns a label for UI when given a setting name or namespace"""

        hardware_menu = {
            "printer": t("Printer"),
        }
        hardware_menu["buttons"] = t("Buttons")
        if board.config["type"] in ["amigo", "yahboom", "wonder_mv"]:
            hardware_menu["touchscreen"] = t("Touchscreen")
        if board.config["type"] == "amigo":
            hardware_menu["display_amg"] = t("Display")
        elif board.config["type"] in ["cube", "m5stickv", "wonder_mv"]:
            hardware_menu["display"] = t("Display")

        return hardware_menu[attr]


class PersistSettings(SettingsNamespace):
    """Persistent settings"""

    namespace = "settings.persist"
    location = CategorySetting("location", FLASH_PATH, [FLASH_PATH, SD_PATH])

    def label(self, attr):
        """Returns a label for UI when given a setting name or namespace"""
        return {
            "location": t("Location"),
        }[attr]


class EncryptionSettings(SettingsNamespace):
    """Encryption settings"""

    AES_ECB_NAME = "AES-ECB"
    AES_CBC_NAME = "AES-CBC"
    VERSION_NAMES = {
        PBKDF2_HMAC_ECB: AES_ECB_NAME,
        PBKDF2_HMAC_CBC: AES_CBC_NAME,
    }
    namespace = "settings.encryption"
    version = CategorySetting("version", AES_ECB_NAME, list(VERSION_NAMES.values()))
    pbkdf2_iterations = NumberSetting(int, "pbkdf2_iterations", 100000, [1, 500000])

    def label(self, attr):
        """Returns a label for UI when given a setting name or namespace"""
        return {
            "version": t("Encryption Mode"),
            "pbkdf2_iterations": t("PBKDF2 Iter."),
        }[attr]


class ThemeSettings(SettingsNamespace):
    """Theme settings"""

    DARK_THEME = 0
    LIGHT_THEME = 1
    ORANGE_THEME = 3
    GREEN_THEME = 4
    PINK_THEME = 5
    DARK_THEME_NAME = "Dark"
    LIGHT_THEME_NAME = "Light"
    ORANGE_THEME_NAME = "Orange"
    GREEN_THEME_NAME = "CypherPunk"
    PINK_THEME_NAME = "CypherPink"
    THEME_NAMES = {
        DARK_THEME: DARK_THEME_NAME,
        LIGHT_THEME: LIGHT_THEME_NAME,
        ORANGE_THEME: ORANGE_THEME_NAME,
        GREEN_THEME: GREEN_THEME_NAME,
        PINK_THEME: PINK_THEME_NAME,
    }
    namespace = "settings.appearance"
    theme = CategorySetting("theme", DARK_THEME_NAME, list(THEME_NAMES.values()))
    screensaver_time = NumberSetting(int, "screensaver_time", 5, [0, 30])

    def label(self, attr):
        """Returns a label for UI when given a setting name or namespace"""
        return {
            "theme": t("Theme"),
            "screensaver_time": t("Screensaver Time"),
        }[attr]


class SecuritySettings(SettingsNamespace):
    """Security settings"""

    namespace = "settings.security"
    auto_shutdown = NumberSetting(int, "auto_shutdown", 10, [0, 60])
    hide_mnemonic = CategorySetting("hide_mnemonic", False, [False, True])
    boot_flash_hash = CategorySetting("boot_flash_hash", False, [False, True])
    allow_kapp = CategorySetting("allow_kapp", False, [False, True])

    def label(self, attr):
        """Returns a label for UI when given a setting name or namespace"""
        return {
            "auto_shutdown": t("Shutdown Time"),
            "hide_mnemonic": t("Hide Mnemonics"),
            "boot_flash_hash": t("TC Flash Hash at Boot"),
            "allow_kapp": t("Allow Krux apps"),
        }[attr]


class Settings(SettingsNamespace):
    """The top-level settings namespace under which other namespaces reside"""

    namespace = "settings"

    def __init__(self):
        self.wallet = DefaultWallet()
        self.security = SecuritySettings()
        self.hardware = HardwareSettings()
        self.i18n = I18nSettings()
        self.encryption = EncryptionSettings()
        self.persist = PersistSettings()
        self.appearance = ThemeSettings()

    def label(self, attr):
        """Returns a label for UI when given a setting name or namespace"""
        main_menu = {
            "wallet": t("Default Wallet"),
            "security": t("Security"),
            "hardware": t("Hardware"),
            "i18n": t("Language"),
            "encryption": t("Encryption"),
            "persist": t("Persist"),
            "appearance": t("Appearance"),
        }

        return main_menu[attr]


locale_control.load_locale(Settings().i18n.locale)
