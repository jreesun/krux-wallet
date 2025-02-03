import pytest
from unittest.mock import patch
from . import create_ctx
from ..shared_mocks import mock_context
from ..test_sd_card import mocker_sd_card_ok
from .test_login import mocker_printer


################### Test menus
class RebootException(Exception):
    """Exception to simulate rebooting the device."""

    pass


def test_settings_m5stickv(m5stickv, mocker, mocker_printer):
    from krux.pages.settings_page import SettingsPage
    from krux.input import BUTTON_ENTER, BUTTON_PAGE, BUTTON_PAGE_PREV
    from krux.krux_settings import Settings, CategorySetting, NumberSetting
    from krux.translations import available_languages

    index_pt = available_languages.index("pt-BR")
    index_next = (index_pt + 1) % (len(available_languages))

    cases = [
        (  # 0 - Change Network
            (
                # Default Wallet
                BUTTON_ENTER,
                # Go to Network
                BUTTON_ENTER,
                # Change network
                *([BUTTON_PAGE] * 2),  # Cycle through 2 options
                BUTTON_PAGE_PREV,  # Go back to the second option - testnet
                BUTTON_ENTER,
                # Leave Default Wallet
                *([BUTTON_PAGE] * 3),
                BUTTON_ENTER,
                # Leave Settings
                BUTTON_PAGE_PREV,
                BUTTON_ENTER,
            ),
            lambda: Settings().wallet.network == "test",
        ),
        (  # 1 Printer Settings
            (
                # Hardware
                *([BUTTON_PAGE] * 2),
                BUTTON_ENTER,
                # Printer
                *([BUTTON_PAGE] * 2),
                BUTTON_ENTER,
                # Thermal (printer)
                BUTTON_PAGE,
                BUTTON_ENTER,
                # Change Baudrate
                BUTTON_ENTER,
                BUTTON_PAGE,
                BUTTON_ENTER,
                # Back to Thermal
                BUTTON_PAGE_PREV,
                BUTTON_ENTER,
                # Back to Printer
                *([BUTTON_PAGE] * 2),
                BUTTON_ENTER,
                # Back to settings
                BUTTON_PAGE,
                BUTTON_ENTER,
                # Leave Settings
                *([BUTTON_PAGE_PREV] * 3),
                BUTTON_ENTER,
            ),
            lambda: Settings().hardware.printer.thermal.adafruit.baudrate == 19200,
        ),
        (  # 2 Language Settings
            (
                # Language
                *([BUTTON_PAGE] * 3),
                BUTTON_ENTER,
                # Change Locale
                BUTTON_PAGE,
                BUTTON_ENTER,
            ),
            lambda: Settings().i18n.locale == available_languages[index_next],
        ),
        (  # 3  Printer numeric settings
            (
                # Hardware
                *([BUTTON_PAGE] * 2),
                BUTTON_ENTER,
                # Printer
                *([BUTTON_PAGE] * 2),
                BUTTON_ENTER,
                # Thermal (printer)
                BUTTON_PAGE,
                BUTTON_ENTER,
                # Paper Width
                *([BUTTON_PAGE] * 2),
                BUTTON_ENTER,
                # Change width
                # Remove digit (become 38)
                *([BUTTON_PAGE_PREV] * 3),
                BUTTON_ENTER,
                # Add 0 (become 380)
                BUTTON_PAGE_PREV,
                BUTTON_ENTER,
                # Go
                *([BUTTON_PAGE] * 3),
                BUTTON_ENTER,
                # Back to Thermal
                *([BUTTON_PAGE] * 4),
                BUTTON_ENTER,
                # Back to Printer
                *([BUTTON_PAGE] * 2),
                BUTTON_ENTER,
                # Back to settings
                BUTTON_PAGE,
                BUTTON_ENTER,
                # Leave Settings
                *([BUTTON_PAGE_PREV] * 3),
                BUTTON_ENTER,
            ),
            lambda: Settings().hardware.printer.thermal.adafruit.paper_width == 380,
        ),
        (  # 4 Change theme
            (
                *([BUTTON_PAGE] * 6),  # Move to "Appearance"
                BUTTON_ENTER,  # Enter "Appearance"
                BUTTON_PAGE,  # Move to "Theme"
                BUTTON_ENTER,  # Enter "Theme"
                BUTTON_PAGE,  # Change to "Light"
                BUTTON_ENTER,  # Confirm "Light"
                BUTTON_ENTER,  # Confirm reboot
            ),
            lambda: Settings().appearance.theme == "Light",
        ),
    ]
    case_num = 0
    for case in cases:
        print("test_settings cases[" + str(case_num) + "]")
        case_num = case_num + 1

        ctx = create_ctx(mocker, case[0])
        settings_page = SettingsPage(ctx)
        Settings().i18n.locale = "pt-BR"
        settings_page.settings()

        assert ctx.input.wait_for_button.call_count == len(case[0])
        assert case[1]()


@pytest.fixture(params=["m5stickv", "cube", "wonder_mv"])
def bkl_control_devices(request):
    return request.getfixturevalue(request.param)


def test_change_brightness(bkl_control_devices, mocker):
    from krux.pages.settings_page import SettingsPage
    from krux.input import BUTTON_ENTER, BUTTON_PAGE, BUTTON_PAGE_PREV
    from krux.krux_settings import Settings
    import board

    BTN_SEQUENCE = [
        *([BUTTON_PAGE] * 2),  # Move to "Hardware"
        BUTTON_ENTER,  # Enter "Hardware"
        BUTTON_PAGE,  # Move to "Display"
        BUTTON_ENTER,  # Enter "Display"
        BUTTON_PAGE,  # Change "Brightness"
        BUTTON_ENTER,  # Enter "Brightness"
        *([BUTTON_PAGE_PREV] * 2),  # Move to "Back"
        BUTTON_ENTER,  # Confirm "Back"
        *([BUTTON_PAGE_PREV] * 3),  # Move to "Back"
        BUTTON_ENTER,  # Confirm "Back"
    ]
    BTN_SEQUENCE_WONDER_MV = [
        *([BUTTON_PAGE] * 2),  # Move to "Hardware"
        BUTTON_ENTER,  # Enter "Hardware"
        BUTTON_PAGE,  # Move to "Display"
        BUTTON_ENTER,  # Enter "Display"
        BUTTON_ENTER,  # Enter "Brightness"
        BUTTON_PAGE,  # Change "Brightness"
        BUTTON_ENTER,  # Enter "Brightness"
        BUTTON_PAGE_PREV,  # Move to "Back"
        BUTTON_ENTER,  # Confirm "Back"
        *([BUTTON_PAGE_PREV] * 2),  # Move to "Back"
        BUTTON_ENTER,  # Confirm "Back"
        *([BUTTON_PAGE_PREV] * 3),  # Move to "Back"
        BUTTON_ENTER,  # Confirm "Back"
    ]
    if board.config["type"] == "wonder_mv":
        ctx = create_ctx(mocker, BTN_SEQUENCE_WONDER_MV)
    else:
        ctx = create_ctx(mocker, BTN_SEQUENCE)
    settings_page = SettingsPage(ctx)
    previous_brightness = int(Settings().hardware.display.brightness)
    settings_page.settings()

    len_sequence = (
        len(BTN_SEQUENCE)
        if board.config["type"] != "wonder_mv"
        else len(BTN_SEQUENCE_WONDER_MV)
    )
    assert ctx.input.wait_for_button.call_count == len_sequence
    assert Settings().hardware.display.brightness == str(previous_brightness + 1)


def test_settings_on_amigo_tft(amigo, mocker, mocker_printer):
    import krux
    from krux.pages.settings_page import SettingsPage
    from krux.input import BUTTON_TOUCH
    from krux.krux_settings import Settings, CategorySetting
    from krux.translations import available_languages, ref_array
    from krux.translations.pt import translation_array as br_array
    from krux.themes import WHITE, GREEN, ORANGE

    index_pt = available_languages.index("pt-BR")
    index_next = (index_pt + 1) % (len(available_languages))
    slug_index = ref_array.index(1177338798)
    text_pt = br_array[slug_index] + "\n" + available_languages[index_pt]

    # Get translations for the next language
    next_language = available_languages[index_next]
    # Construct the path to the nested module
    next_module_path = f"krux.translations.{next_language[:2]}"
    # Import the top-level module (krux)
    next_trans_module = __import__(next_module_path, fromlist=[""])
    # Access the translation_array variable from the nested module
    next_trans_array = getattr(next_trans_module, "translation_array")
    text_next = next_trans_array[slug_index] + "\n" + available_languages[index_next]

    PREV_INDEX = 0
    GO_INDEX = 1
    NEXT_INDEX = 2

    HARDWARE_INDEX = 2
    LOCALE_INDEX = 3
    PRINTER_INDEX = 2
    LEAVE_INDEX = 8

    cases = [
        (
            # Case 0
            (
                # Enter Wallet
                0,
                # Go to Network
                0,
                # Change network
                NEXT_INDEX,
                GO_INDEX,
                # Back from wallet
                3,
                # Leave Settings
                LEAVE_INDEX,
            ),
            [
                mocker.call("Network\nmain", ORANGE),
                mocker.call("Network\ntest", GREEN),
            ],
            lambda: Settings().wallet.network == "test",
            CategorySetting,
        ),
        (
            # Case 1
            (
                # Hardware
                HARDWARE_INDEX,
                # Printer
                PRINTER_INDEX,
                # Thermal
                1,
                # Change Baudrate
                0,
                NEXT_INDEX,
                GO_INDEX,
                # Back from Thermal
                6,
                # Back from Printer
                3,
                # Back from Hardware
                4,
                # Leave Settings
                LEAVE_INDEX,
            ),
            [
                mocker.call("Baudrate\n9600", WHITE),
                mocker.call("Baudrate\n19200", WHITE),
            ],
            lambda: Settings().hardware.printer.thermal.adafruit.baudrate == 19200,
            CategorySetting,
        ),
        (
            # Case 2
            (
                # Language
                LOCALE_INDEX,
                # Change Locale
                NEXT_INDEX,
                GO_INDEX,
            ),
            [
                mocker.call(text_pt, WHITE),
                mocker.call(text_next, WHITE),
            ],
            lambda: Settings().i18n.locale == available_languages[index_next],
            CategorySetting,
        ),
    ]
    case_num = 0
    for case in cases:
        print("test_settings_on_amigo_tft cases[" + str(case_num) + "]")
        case_num = case_num + 1

        ctx = mock_context(mocker)
        ctx.power_manager.battery_charge_remaining.return_value = 1
        ctx.input.wait_for_button = mocker.MagicMock(return_value=BUTTON_TOUCH)
        ctx.input.touch = mocker.MagicMock(
            current_index=mocker.MagicMock(side_effect=case[0])
        )

        mocker.patch.object(ctx.input.touch, "x_regions", (0, 100, 200, 300))
        mocker.patch.object(ctx.input.touch, "y_regions", (100, 200))

        settings_page = SettingsPage(ctx)

        Settings().i18n.locale = "pt-BR"
        settings_page.settings()

        assert ctx.input.wait_for_button.call_count == len(case[0])

        assert case[2]()


def test_change_display_type_on_amigo(amigo, mocker):
    from krux.pages.settings_page import SettingsPage
    from krux.input import BUTTON_ENTER, BUTTON_PAGE, BUTTON_PAGE_PREV
    from krux.krux_settings import Settings, CategorySetting, NumberSetting

    BTN_SEQUENCE = [
        *([BUTTON_PAGE] * 2),  # Move to "Hardware"
        BUTTON_ENTER,  # Enter "Hardware"
        BUTTON_PAGE,  # Change to "Display"
        BUTTON_ENTER,  # Enter "Display"
        BUTTON_ENTER,  # Enter "BGR colors"
        BUTTON_PAGE,  # Change "BGR Type"
        BUTTON_ENTER,  # Enter "BGR Type"
        BUTTON_PAGE,  # Go to "Flipped X ..."
        BUTTON_ENTER,  # Enter "Flipped X ..."
        BUTTON_PAGE,  # Change "Flipped X ..."
        BUTTON_ENTER,  # Enter "Flipped X ..."
        BUTTON_PAGE,  # Go to "Inverted Colors"
        BUTTON_ENTER,  # Enter "Inverted Colors"
        BUTTON_PAGE,  # Change "Inverted Colors"
        BUTTON_ENTER,  # Enter "Inverted Colors"
        BUTTON_PAGE,  # Go to "Type"
        BUTTON_ENTER,  # Enter "Type"
        BUTTON_PAGE,  # Change "Type"
        BUTTON_ENTER,  # Confirm "Warning"
        BUTTON_PAGE_PREV,  # Confirm new setting
        BUTTON_ENTER,  # Confirm "Type"
        BUTTON_PAGE,  # Move to "Back"
        BUTTON_ENTER,  # Confirm "Back" from display
        *([BUTTON_PAGE_PREV] * 2),  # Move to "Back"
        BUTTON_ENTER,  # Confirm "Back" from hardware
        *([BUTTON_PAGE_PREV] * 3),  # Move to "Back"
        BUTTON_ENTER,  # Confirm "Back" from settings
    ]
    ctx = create_ctx(mocker, BTN_SEQUENCE)
    settings_page = SettingsPage(ctx)
    settings_page.settings()

    assert ctx.input.wait_for_button.call_count == len(BTN_SEQUENCE)
    # assert Settings().hardware.display.bgr_type == "RGB"


def test_encryption_pbkdf2_setting(m5stickv, mocker):
    from krux.pages.settings_page import SettingsPage
    from krux.krux_settings import Settings, EncryptionSettings

    ctx = mock_context(mocker)
    settings_page = SettingsPage(ctx)

    mocker.spy(SettingsPage, "flash_error")

    # pbkdf2_iterations has default value
    assert Settings().encryption.pbkdf2_iterations == 100000

    # try to change the value
    settings_page.capture_from_keypad = mocker.MagicMock(return_value=100001)
    settings_page.number_setting(
        EncryptionSettings(), EncryptionSettings.pbkdf2_iterations
    )

    # continue with default value because it must be multiple of 10000
    assert Settings().encryption.pbkdf2_iterations == 100000

    # error msg is shown
    settings_page.flash_error.assert_called()

    # try to change the value to a multiple of 10000
    settings_page.capture_from_keypad = mocker.MagicMock(return_value=110000)
    settings_page.number_setting(
        EncryptionSettings(), EncryptionSettings.pbkdf2_iterations
    )

    # value changed!
    assert Settings().encryption.pbkdf2_iterations == 110000

    # try to change the value to a value out of range
    settings_page.capture_from_keypad = mocker.MagicMock(return_value=0)
    settings_page.number_setting(
        EncryptionSettings(), EncryptionSettings.pbkdf2_iterations
    )

    # value remain unchanged!
    assert Settings().encryption.pbkdf2_iterations == 110000


def test_restore_settings(amigo, mocker, mocker_sd_card_ok):
    from krux.pages.settings_page import SettingsPage
    from krux.settings import FLASH_PATH, SETTINGS_FILENAME
    from krux.input import BUTTON_ENTER

    BTN_SEQUENCE = [BUTTON_ENTER]  # Confirm restore

    with patch("os.remove") as mock_remove:
        with patch("krux.sd_card.SDHandler.delete") as mock_delete_sd:
            ctx = create_ctx(mocker, BTN_SEQUENCE)
            settings_page = SettingsPage(ctx)
            settings_page.restore_settings()
    mock_delete_sd.assert_called_once_with(SETTINGS_FILENAME)
    mock_remove.assert_called_once_with("/" + FLASH_PATH + "/" + SETTINGS_FILENAME)


def test_set_first_tc_code(amigo, mocker):
    from krux.pages.settings_page import SettingsPage
    from krux.input import BUTTON_ENTER, BUTTON_PAGE
    from ..shared_mocks import MockFile, mock_open

    TC_CODE_EXTENDED_HASH = b"z\xc0\x99\xac\x01\x1f\xef\x91\xb6\xd5\xbd\xa8\xdc\xfc\x14\xcco-A\x9d\xba\xde\xaf\xe3\xe1{@0t\xb2\x85{"
    mocker.patch(
        "krux.pages.fill_flash.FillFlash.fill_flash_with_camera_entropy",
        new=mocker.MagicMock(),
    )
    mocker.patch("machine.unique_id", return_value=b"\x01" * 32)
    mocker.patch("krux.pages.flash_tools.FlashHash", new=mocker.MagicMock())
    mock_file = MockFile()
    mocker.patch("builtins.open", mock_open(mock_file))
    ctx = create_ctx(
        mocker,
        [
            BUTTON_ENTER,
            BUTTON_ENTER,
        ],  # Confirm TC Flash Hash at boot
    )
    ctx.tc_code_enabled = False
    settings_page = SettingsPage(ctx)
    settings_page.capture_from_keypad = mocker.MagicMock(return_value="123456")
    settings_page.enter_modify_tc_code()
    assert ctx.tc_code_enabled == True
    assert mock_file.previous_data[-1] == TC_CODE_EXTENDED_HASH
    assert (
        mock_file.write_data == '{"settings": {"security": {"boot_flash_hash": true}}}'
    )


def test_set_first_tc_code_not_match(amigo, mocker):
    from krux.pages.settings_page import SettingsPage
    from krux.input import BUTTON_ENTER
    from ..shared_mocks import MockFile, mock_open

    CODES = ["123456", "654321"]

    mock_file = MockFile()
    ctx = create_ctx(mocker, [BUTTON_ENTER])
    ctx.tc_code_enabled = False
    settings_page = SettingsPage(ctx)
    settings_page.capture_from_keypad = mocker.MagicMock(side_effect=CODES)
    settings_page.enter_modify_tc_code()
    assert ctx.tc_code_enabled == False
    assert mock_file.write_data == b""


def test_set_new_tc_code(amigo, mocker):
    from krux.pages.settings_page import SettingsPage
    from krux.input import BUTTON_ENTER, BUTTON_PAGE
    from ..shared_mocks import MockFile, mock_open

    TC_CODE_EXTENDED_HASH = b"z\xc0\x99\xac\x01\x1f\xef\x91\xb6\xd5\xbd\xa8\xdc\xfc\x14\xcco-A\x9d\xba\xde\xaf\xe3\xe1{@0t\xb2\x85{"
    mocker.patch(
        "krux.pages.fill_flash.FillFlash.fill_flash_with_camera_entropy",
        new=mocker.MagicMock(),
    )
    mocker.patch(
        "krux.pages.tc_code_verification.TCCodeVerification.capture", return_value=True
    )
    mocker.patch("krux.pages.flash_tools.FlashHash", new=mocker.MagicMock())
    mocker.patch("machine.unique_id", return_value=b"\x01" * 32)
    mock_file = MockFile()
    mocker.patch("builtins.open", mock_open(mock_file))
    ctx = create_ctx(
        mocker,
        [
            BUTTON_ENTER,
            BUTTON_ENTER,
        ],  # Confirm TC Flash Hash at boot
    )
    ctx.tc_code_enabled = True
    settings_page = SettingsPage(ctx)
    settings_page.capture_from_keypad = mocker.MagicMock(return_value="123456")
    settings_page.enter_modify_tc_code()
    assert ctx.tc_code_enabled == True
    assert mock_file.previous_data[-1] == TC_CODE_EXTENDED_HASH
    assert (
        mock_file.write_data == '{"settings": {"security": {"boot_flash_hash": true}}}'
    )


def test_wrong_code_set_new_tc_code(amigo, mocker):
    from krux.pages.settings_page import SettingsPage
    from krux.input import BUTTON_ENTER
    from ..shared_mocks import MockFile, mock_open

    # TC Code check returns false
    mocker.patch(
        "krux.pages.tc_code_verification.TCCodeVerification.capture", return_value=False
    )
    mock_file = MockFile()
    ctx = create_ctx(mocker, [BUTTON_ENTER])
    ctx.tc_code_enabled = True
    settings_page = SettingsPage(ctx)
    settings_page.enter_modify_tc_code()
    assert mock_file.write_data == b""


def test_save_settings_on_sd(amigo, mocker, mocker_sd_card_ok):
    from krux.pages.settings_page import SettingsPage
    from krux.krux_settings import Settings, SD_PATH
    from krux.input import BUTTON_ENTER, BUTTON_PAGE_PREV

    BTN_SEQUENCE = [
        BUTTON_PAGE_PREV,  # Move to "Back"
        BUTTON_ENTER,  # Confirm "Back"
    ]

    ctx = create_ctx(mocker, BTN_SEQUENCE)
    settings_page = SettingsPage(ctx)
    settings_page.flash_text = mocker.MagicMock()
    Settings().persist.location = SD_PATH
    settings_page.settings()
    settings_page.flash_text.assert_has_calls(
        [
            mocker.call("Settings stored on SD card.", duration=2500),
        ]
    )


def test_leave_settings_without_changes(amigo, mocker):
    from krux.pages.settings_page import SettingsPage
    from krux.input import BUTTON_ENTER, BUTTON_PAGE, BUTTON_PAGE_PREV

    mocker.patch(
        "os.listdir",
        new=mocker.MagicMock(return_value=["somefile", "otherfile"]),
    )

    BTN_SEQUENCES = [
        [
            # Change something then give up
            BUTTON_ENTER,  # Change "Default Wallet"
            BUTTON_PAGE,  # Move to "Network"
            BUTTON_ENTER,  # Enter "Network"
            BUTTON_PAGE,  # Change to testnet
            BUTTON_ENTER,  # Confirm "testnet"
            BUTTON_ENTER,  # Change "Network" again
            BUTTON_PAGE,  # Change back to mainnet
            BUTTON_ENTER,  # Confirm mainnet
            *([BUTTON_PAGE] * 2),  # Move to "Back"
            BUTTON_ENTER,  # Confirm "Back"
            BUTTON_PAGE_PREV,  # Move to "Back"
            BUTTON_ENTER,  # Leave settings
        ],
        [
            # Change persist then give up
            *([BUTTON_PAGE] * 4),  # Move to "Persist"
            BUTTON_ENTER,  # Enter "Persist"
            BUTTON_PAGE,  # Change to SD
            BUTTON_ENTER,  # Confirm SD
            BUTTON_ENTER,  # Change "Persist" again
            BUTTON_PAGE,  # Change back to flash
            BUTTON_ENTER,  # Confirm flash
            *([BUTTON_PAGE] * 4),  # Move to "Back"
            BUTTON_ENTER,  # Leave settings
        ],
        [
            # Don't change anything
            BUTTON_PAGE_PREV,  # Move to "Back"
            BUTTON_ENTER,  # Confirm "Back"
        ],
    ]

    for btn_sequence in BTN_SEQUENCES:
        ctx = create_ctx(mocker, btn_sequence)
        settings_page = SettingsPage(ctx)
        settings_page.flash_text = mocker.MagicMock()
        settings_page.settings()
        persisted_to_flash_call = mocker.call(
            "Settings stored internally on flash.", duration=2500
        )
        assert ctx.input.wait_for_button.call_count == len(btn_sequence)
        assert persisted_to_flash_call not in settings_page.flash_text.call_args_list


def test_leave_settings_with_changes(amigo, mocker, mocker_sd_card_ok):
    # mocker_sd_card_ok will mock os.listdir so it will also mock flash storage
    from krux.pages.settings_page import SettingsPage
    from krux.input import BUTTON_ENTER, BUTTON_PAGE, BUTTON_PAGE_PREV

    BTN_SEQUENCE = [
        BUTTON_ENTER,  # Go to "Default Wallet"
        BUTTON_PAGE,  # Go to "Network"
        BUTTON_ENTER,  # Enter "Network"
        BUTTON_PAGE,  # Change to testnet
        BUTTON_ENTER,  # Confirm "testnet"
        *([BUTTON_PAGE] * 2),  # Move to back
        BUTTON_ENTER,  # Leave "Wallet"
        BUTTON_PAGE_PREV,  # Move to "Back"
        BUTTON_ENTER,  # Confirm "Back"
    ]
    ctx = create_ctx(mocker, BTN_SEQUENCE)
    settings_page = SettingsPage(ctx)
    settings_page.flash_text = mocker.MagicMock()

    # Leave settings without changes
    settings_page.settings()
    assert ctx.input.wait_for_button.call_count == len(BTN_SEQUENCE)
    settings_page.flash_text.assert_has_calls(
        [
            mocker.call("Settings stored internally on flash.", duration=2500),
        ]
    )


def test_persist_to_sd_without_sd(amigo, mocker):
    from krux.pages.settings_page import SettingsPage
    from krux.krux_settings import Settings, SD_PATH
    from krux.input import BUTTON_ENTER, BUTTON_PAGE_PREV

    BTN_SEQUENCE = [
        BUTTON_PAGE_PREV,  # Move to "Back"
        BUTTON_ENTER,  # Confirm "Back"
    ]

    ctx = create_ctx(mocker, BTN_SEQUENCE)
    settings_page = SettingsPage(ctx)
    settings_page.flash_text = mocker.MagicMock()
    Settings().persist.location = SD_PATH
    settings_page.settings()
    settings_page.flash_text.assert_has_calls(
        [
            mocker.call(
                "SD card not detected.\n\nChanges will last until shutdown.",
                duration=2500,
            ),
        ]
    )
