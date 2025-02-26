from . import create_ctx
from .home_pages.test_home import tdata
import pytest


def test_type_passphrase(m5stickv, mocker):
    from krux.pages.wallet_settings import PassphraseEditor

    TEST_VALUE = "Test value"
    ctx = create_ctx(mocker, TEST_VALUE)
    passphrase_editor = PassphraseEditor(ctx)
    mocker.patch.object(
        passphrase_editor,
        "capture_from_keypad",
        return_value=TEST_VALUE,
    )
    test_passphrase = passphrase_editor._load_passphrase()

    assert test_passphrase == TEST_VALUE


def test_type_passphrase_esc(m5stickv, mocker):
    from krux.pages.wallet_settings import PassphraseEditor
    from krux.pages import BUTTON_ENTER, BUTTON_PAGE_PREV

    BTN_SEQUENCE = [
        BUTTON_ENTER,  # Type BIP39 Passphrase
        *([BUTTON_PAGE_PREV] * 2),  # Go to "Esc"
        BUTTON_ENTER,  # Press Esc
        BUTTON_ENTER,  # Confirm Esc
    ]
    ctx = create_ctx(mocker, BTN_SEQUENCE)
    passphrase_editor = PassphraseEditor(ctx)
    test_passphrase = passphrase_editor.load_passphrase_menu()

    assert test_passphrase is None


def test_qr_passphrase(m5stickv, mocker):
    from krux.pages.wallet_settings import PassphraseEditor
    from krux.pages.qr_capture import QRCodeCapture

    TEST_VALUE = "Test value"
    QR_DATA = (TEST_VALUE, None)
    ctx = create_ctx(mocker, None)
    passphrase_editor = PassphraseEditor(ctx)
    mocker.patch.object(QRCodeCapture, "qr_capture_loop", new=lambda self: (QR_DATA))
    qr_capturer = mocker.spy(QRCodeCapture, "qr_capture_loop")
    test_passphrase = passphrase_editor._load_qr_passphrase()

    assert test_passphrase == TEST_VALUE
    qr_capturer.assert_called_once()


def test_qr_passphrase_too_long(m5stickv, mocker):
    from krux.pages.wallet_settings import (
        PassphraseEditor,
        MENU_CONTINUE,
        PASSPHRASE_MAX_LEN,
    )
    from krux.pages.qr_capture import QRCodeCapture

    TEST_VALUE = "Test value" * 25
    QR_DATA = (TEST_VALUE, None)
    ctx = create_ctx(mocker, None)
    passphrase_editor = PassphraseEditor(ctx)
    mocker.patch.object(QRCodeCapture, "qr_capture_loop", new=lambda self: (QR_DATA))
    qr_capturer = mocker.spy(QRCodeCapture, "qr_capture_loop")

    error_message = "Maximum length exceeded (%s)" % PASSPHRASE_MAX_LEN
    with pytest.raises(ValueError) as error:
        test_passphrase = passphrase_editor._load_qr_passphrase()

        assert error_message in str(error.value)
        assert test_passphrase == MENU_CONTINUE
        qr_capturer.assert_called_once()


def test_qr_passphrase_fail(m5stickv, mocker):
    from krux.pages.wallet_settings import PassphraseEditor, MENU_CONTINUE
    from krux.pages.qr_capture import QRCodeCapture

    TEST_VALUE = None
    QR_DATA = (TEST_VALUE, None)
    ctx = create_ctx(mocker, None)
    passphrase_editor = PassphraseEditor(ctx)
    mocker.patch.object(QRCodeCapture, "qr_capture_loop", new=lambda self: (QR_DATA))
    qr_capturer = mocker.spy(QRCodeCapture, "qr_capture_loop")
    test_passphrase = passphrase_editor._load_qr_passphrase()

    assert test_passphrase == MENU_CONTINUE
    qr_capturer.assert_called_once()


def test_change_policy_types(m5stickv, mocker, tdata):
    from krux.pages.wallet_settings import WalletSettings
    from krux.wallet import Wallet
    from krux.key import Key, TYPE_SINGLESIG, TYPE_MULTISIG, TYPE_MINISCRIPT
    from krux.pages import BUTTON_ENTER, BUTTON_PAGE, BUTTON_PAGE_PREV

    BTN_SEQUENCE = [
        BUTTON_PAGE,  # Go to "Policy Type"
        BUTTON_ENTER,  # Enter "Policy Type"
        BUTTON_PAGE,  # Change to Multisig
        BUTTON_ENTER,  # Confirm Multisig
        BUTTON_PAGE_PREV,  # Go to Back
        BUTTON_ENTER,  # Leave
    ]

    ctx = create_ctx(mocker, BTN_SEQUENCE, Wallet(tdata.SINGLESIG_12_WORD_KEY))

    # assert wallet starts as single-sig, native segwit
    assert ctx.wallet.is_multisig() is False
    assert ctx.wallet.is_miniscript() is False
    assert ctx.wallet.key.policy_type == TYPE_SINGLESIG
    assert ctx.wallet.key.script_type == "p2wpkh"

    mnemonic = ctx.wallet.key.mnemonic
    wallet_settings = WalletSettings(ctx)
    network, policy_type, script_type, account, derivation_path = (
        wallet_settings.customize_wallet(ctx.wallet.key)
    )
    ctx.wallet = Wallet(
        Key(
            mnemonic,
            policy_type,
            network,
            "",  # passphrase
            account,
            script_type,
            derivation_path,
        )
    )

    # Assert wallet is now multisig and changed to p2wsh
    assert ctx.wallet.is_multisig() is True
    assert ctx.wallet.is_miniscript() is False
    assert ctx.wallet.key.policy_type == TYPE_MULTISIG
    assert ctx.wallet.key.script_type == "p2wsh"
    assert ctx.input.wait_for_button.call_count == len(BTN_SEQUENCE)

    # Change to miniscript
    BTN_SEQUENCE = [
        BUTTON_PAGE,  # Go to "Policy Type"
        BUTTON_ENTER,  # Enter "Policy Type"
        *([BUTTON_PAGE] * 2),  # Change to Miniscript
        BUTTON_ENTER,  # Confirm Miniscript
        BUTTON_PAGE_PREV,  # Go to Back
        BUTTON_ENTER,  # Leave
    ]
    ctx = create_ctx(mocker, BTN_SEQUENCE, ctx.wallet)
    wallet_settings = WalletSettings(ctx)
    network, policy_type, script_type, account, derivation_path = (
        wallet_settings.customize_wallet(ctx.wallet.key)
    )
    ctx.wallet = Wallet(
        Key(
            mnemonic,
            policy_type,
            network,
            "",  # passphrase
            account,
            script_type,
            derivation_path,
        )
    )

    # Assert wallet is now miniscript and remained p2wsh
    assert ctx.wallet.is_multisig() is False
    assert ctx.wallet.is_miniscript() is True
    assert ctx.wallet.key.policy_type == TYPE_MINISCRIPT
    assert ctx.wallet.key.script_type == "p2wsh"
    assert ctx.input.wait_for_button.call_count == len(BTN_SEQUENCE)

    # Change back to singlesig
    BTN_SEQUENCE = [
        BUTTON_PAGE,  # Go to "Single/Multisig"
        BUTTON_ENTER,  # Enter "Single/Multisig"
        BUTTON_ENTER,  # Confirm Single
        *([BUTTON_PAGE] * 2),  # Choose Native Segwit
        BUTTON_ENTER,  # Confirm Native Segwit
        BUTTON_PAGE_PREV,  # Go to Back
        BUTTON_ENTER,  # Leave
    ]

    ctx = create_ctx(mocker, BTN_SEQUENCE, ctx.wallet)
    wallet_settings = WalletSettings(ctx)
    network, policy_type, script_type, account, derivation_path = (
        wallet_settings.customize_wallet(ctx.wallet.key)
    )
    ctx.wallet = Wallet(
        Key(
            mnemonic,
            policy_type,
            network,
            "",  # passphrase
            account,
            script_type,
            derivation_path,
        )
    )
    assert ctx.wallet.is_multisig() is False
    assert ctx.wallet.is_miniscript() is False
    assert ctx.wallet.key.policy_type == TYPE_SINGLESIG
    assert ctx.wallet.key.script_type == "p2wpkh"
    assert ctx.input.wait_for_button.call_count == len(BTN_SEQUENCE)

    # Going from single-sig to miniscript forces to change to script type
    BTN_SEQUENCE = [
        BUTTON_PAGE,  # Go to "Policy Type"
        BUTTON_ENTER,  # Enter "Policy Type"
        *([BUTTON_PAGE] * 2),  # Change to Miniscript
        BUTTON_ENTER,  # Confirm Miniscript
        BUTTON_PAGE,  # Change from Native Segwit to Taproot
        BUTTON_ENTER,  # Confirm Taproot
        BUTTON_PAGE_PREV,  # Go to Back
        BUTTON_ENTER,  # Leave
    ]

    ctx = create_ctx(mocker, BTN_SEQUENCE, ctx.wallet)
    wallet_settings = WalletSettings(ctx)
    network, policy_type, script_type, account, derivation_path = (
        wallet_settings.customize_wallet(ctx.wallet.key)
    )
    ctx.wallet = Wallet(
        Key(
            mnemonic,
            policy_type,
            network,
            "",  # passphrase
            account,
            script_type,
            derivation_path,
        )
    )
    assert ctx.wallet.is_multisig() is False
    assert ctx.wallet.is_miniscript() is True
    assert ctx.wallet.key.policy_type == TYPE_MINISCRIPT
    assert ctx.wallet.key.script_type == "p2tr"
    assert ctx.input.wait_for_button.call_count == len(BTN_SEQUENCE)


def test_change_script_type(m5stickv, mocker, tdata):
    from krux.pages.wallet_settings import WalletSettings
    from krux.wallet import Wallet
    from krux.key import Key
    from krux.pages import BUTTON_ENTER, BUTTON_PAGE, BUTTON_PAGE_PREV

    BTN_SEQUENCE_1 = [
        *([BUTTON_PAGE] * 2),  # Go to "Script Type"
        BUTTON_ENTER,  # Enter "Script Type"
        *([BUTTON_PAGE] * 3),  # Move to Taproot
        BUTTON_ENTER,  # Confirm Taproot
        BUTTON_PAGE_PREV,  # Go to Back
        BUTTON_ENTER,  # Leave
    ]
    ctx = create_ctx(mocker, BTN_SEQUENCE_1, Wallet(tdata.SINGLESIG_12_WORD_KEY))
    mnemonic = ctx.wallet.key.mnemonic
    wallet_settings = WalletSettings(ctx)
    network, policy_type, script_type, account, derivation_path = (
        wallet_settings.customize_wallet(ctx.wallet.key)
    )
    ctx.wallet = Wallet(
        Key(
            mnemonic,
            policy_type,
            network,
            "",  # passphrase
            account,
            script_type,
        )
    )

    assert ctx.wallet.key.script_type == "p2tr"
    assert ctx.input.wait_for_button.call_count == len(BTN_SEQUENCE_1)

    # Change back to legacy
    BTN_SEQUENCE_2 = [
        *([BUTTON_PAGE] * 2),  # Go to "Script Type"
        BUTTON_ENTER,  # Enter "Script Type"
        BUTTON_ENTER,  # Confirm Legacy
        BUTTON_PAGE_PREV,  # Go to Back
        BUTTON_ENTER,  # Leave
    ]
    ctx = create_ctx(mocker, BTN_SEQUENCE_2, ctx.wallet)
    wallet_settings = WalletSettings(ctx)
    network, policy_type, script_type, account, derivation_path = (
        wallet_settings.customize_wallet(ctx.wallet.key)
    )
    ctx.wallet = Wallet(
        Key(
            mnemonic,
            policy_type,
            network,
            "",  # passphrase
            account,
            script_type,
        )
    )
    assert ctx.wallet.key.script_type == "p2pkh"
    assert ctx.input.wait_for_button.call_count == len(BTN_SEQUENCE_2)


def test_change_account(m5stickv, mocker, tdata):
    from krux.pages.wallet_settings import WalletSettings
    from krux.wallet import Wallet
    from krux.key import Key
    from krux.pages import BUTTON_ENTER, BUTTON_PAGE, BUTTON_PAGE_PREV

    BTN_SEQUENCE_1 = [
        *([BUTTON_PAGE] * 3),  # Go to "Account"
        BUTTON_ENTER,  # Enter "Account"
        BUTTON_PAGE,  # Move to number 2
        BUTTON_ENTER,  # Confirm number 2
        *([BUTTON_PAGE_PREV] * 2),  # Move to "Go"
        BUTTON_ENTER,  # Go
        BUTTON_PAGE_PREV,  # Go to Back
        BUTTON_ENTER,  # Leave
    ]
    ctx = create_ctx(mocker, BTN_SEQUENCE_1, Wallet(tdata.SINGLESIG_12_WORD_KEY))
    mnemonic = ctx.wallet.key.mnemonic
    wallet_settings = WalletSettings(ctx)
    network, policy_type, script_type, account, derivation_path = (
        wallet_settings.customize_wallet(ctx.wallet.key)
    )
    ctx.wallet = Wallet(
        Key(
            mnemonic,
            policy_type,
            network,
            "",  # passphrase
            account,
            script_type,
        )
    )

    assert ctx.wallet.key.account_index == 2
    assert ctx.input.wait_for_button.call_count == len(BTN_SEQUENCE_1)

    # Change back to account 0
    BTN_SEQUENCE_2 = [
        *([BUTTON_PAGE] * 3),  # Go to "Account"
        BUTTON_ENTER,  # Enter "Account"
        *([BUTTON_PAGE_PREV] * 3),  # Move to del number
        BUTTON_ENTER,  # Confirm del number
        BUTTON_PAGE_PREV,  # Move to "0"
        BUTTON_ENTER,  # Enter 0
        *([BUTTON_PAGE] * 3),  # Move to "Go"
        BUTTON_ENTER,  # Go
        BUTTON_PAGE_PREV,  # Move to Back
        BUTTON_ENTER,  # Leave
    ]
    ctx = create_ctx(mocker, BTN_SEQUENCE_2, ctx.wallet)
    wallet_settings = WalletSettings(ctx)
    network, policy_type, script_type, account, derivation_path = (
        wallet_settings.customize_wallet(ctx.wallet.key)
    )
    ctx.wallet = Wallet(
        Key(
            mnemonic,
            policy_type,
            network,
            "",  # passphrase
            account,
            script_type,
        )
    )
    assert ctx.wallet.key.account_index == 0
    assert ctx.input.wait_for_button.call_count == len(BTN_SEQUENCE_2)


def test_change_account_esc(m5stickv, mocker, tdata):
    from krux.pages.wallet_settings import WalletSettings
    from krux.wallet import Wallet
    from krux.key import Key
    from krux.pages import BUTTON_ENTER, BUTTON_PAGE, BUTTON_PAGE_PREV

    BTN_SEQUENCE_1 = [
        *([BUTTON_PAGE] * 3),  # Go to "Account"
        BUTTON_ENTER,  # Enter "Account"
        *([BUTTON_PAGE_PREV] * 2),  # Move to Esc
        BUTTON_ENTER,  # Press Esc
        BUTTON_ENTER,  # Confirm Esc
        BUTTON_PAGE_PREV,  # Move to Back
        BUTTON_ENTER,  # Leave
    ]

    ctx = create_ctx(mocker, BTN_SEQUENCE_1, Wallet(tdata.SINGLESIG_12_WORD_KEY))
    mnemonic = ctx.wallet.key.mnemonic
    wallet_settings = WalletSettings(ctx)
    network, policy_type, script_type, account, derivation_path = (
        wallet_settings.customize_wallet(ctx.wallet.key)
    )
    ctx.wallet = Wallet(
        Key(
            mnemonic,
            policy_type,
            network,
            "",  # passphrase
            account,
            script_type,
        )
    )
    assert ctx.wallet.key.account_index == 0
    assert ctx.input.wait_for_button.call_count == len(BTN_SEQUENCE_1)


def test_account_out_of_range(m5stickv, mocker, tdata):
    from krux.pages.wallet_settings import WalletSettings
    from krux.wallet import Wallet
    from krux.key import Key
    from krux.pages import BUTTON_ENTER, BUTTON_PAGE, BUTTON_PAGE_PREV

    BTN_SEQUENCE_1 = [
        *([BUTTON_PAGE] * 3),  # Go to "Account"
        BUTTON_ENTER,  # Enter "Account"
        BUTTON_PAGE,  # Move to number 2
        *([BUTTON_ENTER] * 11),  # Press number 2 11 times
        *([BUTTON_PAGE_PREV] * 2),  # Move to "Go"
        BUTTON_ENTER,  # Go
        BUTTON_PAGE_PREV,  # Go to Back
        BUTTON_ENTER,  # Leave
    ]

    ctx = create_ctx(mocker, BTN_SEQUENCE_1, Wallet(tdata.SINGLESIG_12_WORD_KEY))
    mnemonic = ctx.wallet.key.mnemonic
    wallet_settings = WalletSettings(ctx)
    wallet_settings.flash_error = mocker.MagicMock()
    network, policy_type, script_type, account, derivation_path = (
        wallet_settings.customize_wallet(ctx.wallet.key)
    )
    ctx.wallet = Wallet(
        Key(
            mnemonic,
            policy_type,
            network,
            "",  # passphrase
            account,
            script_type,
        )
    )

    wallet_settings.flash_error.assert_called_with(
        "Value 22222222222 out of range: [0, 2147483647]"
    )
    assert ctx.wallet.key.account_index == 0
    assert ctx.input.wait_for_button.call_count == len(BTN_SEQUENCE_1)


def test_change_derivation_path(amigo, mocker, tdata):
    from krux.pages.wallet_settings import WalletSettings
    from krux.wallet import Wallet
    from krux.key import Key
    from krux.pages import BUTTON_ENTER, BUTTON_PAGE, BUTTON_PAGE_PREV

    BTN_SEQUENCE = [
        BUTTON_PAGE,  # Go to "Policy Type"
        BUTTON_ENTER,  # Enter "Policy Type"
        *([BUTTON_PAGE] * 2),  # Change to Miniscript
        BUTTON_ENTER,  # Confirm Miniscript
        BUTTON_PAGE,  # Change from Native Segwit to Taproot
        BUTTON_ENTER,  # Confirm Taproot
        *([BUTTON_PAGE] * 3),  # Go to "Derivation Path"
        BUTTON_ENTER,  # Enter "Derivation Path"
        *([BUTTON_PAGE_PREV] * 3),  # Move to "Del"
        *([BUTTON_ENTER] * 2),  # Del "2h" from the derivation path
        *([BUTTON_PAGE] * 2),  # Move to "Go"
        BUTTON_ENTER,  # Go
        # Get invalid derivation path (m/48h/0h/0h/), we need to delete trailing "/"
        *([BUTTON_PAGE_PREV] * 3),  # Move to "Del" again
        BUTTON_ENTER,  # Del "/"
        *([BUTTON_PAGE] * 2),  # Move to "Go"
        BUTTON_ENTER,  # Go
        BUTTON_PAGE_PREV,  # Go to Back
        BUTTON_ENTER,  # Leave
    ]

    ctx = create_ctx(mocker, BTN_SEQUENCE, Wallet(tdata.SINGLESIG_12_WORD_KEY))
    mnemonic = ctx.wallet.key.mnemonic
    wallet_settings = WalletSettings(ctx)
    network, policy_type, script_type, account, derivation_path = (
        wallet_settings.customize_wallet(ctx.wallet.key)
    )
    ctx.wallet = Wallet(
        Key(
            mnemonic,
            policy_type,
            network,
            "",  # passphrase
            account,
            script_type,
            derivation_path,
        )
    )

    assert ctx.wallet.key.derivation_str() == "m/48h/0h/0h"
    assert ctx.input.wait_for_button.call_count == len(BTN_SEQUENCE)


def test_change_derivation_path_not_hardened_node(amigo, mocker, tdata):
    from krux.pages.wallet_settings import WalletSettings
    from krux.wallet import Wallet
    from krux.key import Key
    from krux.pages import BUTTON_ENTER, BUTTON_PAGE, BUTTON_PAGE_PREV

    BTN_SEQUENCE = [
        BUTTON_PAGE,  # Go to "Policy Type"
        BUTTON_ENTER,  # Enter "Policy Type"
        *([BUTTON_PAGE] * 2),  # Change to Miniscript
        BUTTON_ENTER,  # Confirm Miniscript
        BUTTON_PAGE,  # Change from Native Segwit to Taproot
        BUTTON_ENTER,  # Confirm Taproot
        *([BUTTON_PAGE] * 3),  # Go to "Derivation Path"
        BUTTON_ENTER,  # Enter "Derivation Path"
        *([BUTTON_PAGE_PREV] * 3),  # Move to "Del"
        BUTTON_ENTER,  # Del last "h" from the derivation path
        *([BUTTON_PAGE] * 2),  # Move to "Go"
        BUTTON_ENTER,  # Go
        # Get not hardened warning/pompt
        BUTTON_ENTER,  # Accept warning
        BUTTON_PAGE_PREV,  # Go to Back
        BUTTON_ENTER,  # Leave
    ]

    ctx = create_ctx(mocker, BTN_SEQUENCE, Wallet(tdata.SINGLESIG_12_WORD_KEY))
    mnemonic = ctx.wallet.key.mnemonic
    wallet_settings = WalletSettings(ctx)
    network, policy_type, script_type, account, derivation_path = (
        wallet_settings.customize_wallet(ctx.wallet.key)
    )
    ctx.wallet = Wallet(
        Key(
            mnemonic,
            policy_type,
            network,
            "",  # passphrase
            account,
            script_type,
            derivation_path,
        )
    )

    assert ctx.wallet.key.derivation_str() == "m/48h/0h/0h/2"
    assert ctx.input.wait_for_button.call_count == len(BTN_SEQUENCE)
