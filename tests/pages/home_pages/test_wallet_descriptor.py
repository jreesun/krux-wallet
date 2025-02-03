from ...shared_mocks import MockPrinter
from .test_home import tdata, create_ctx
from ...test_wallet import tdata as wallet_tdata


def test_wallet(mocker, m5stickv, tdata):
    from krux.pages.home_pages.wallet_descriptor import WalletDescriptor
    from krux.wallet import Wallet
    from krux.input import BUTTON_ENTER, BUTTON_PAGE
    from krux.qr import FORMAT_PMOFN
    from krux.pages.qr_capture import QRCodeCapture

    cases = [
        # 0 Don't load
        (
            False,
            tdata.SINGLESIG_12_WORD_KEY,
            tdata.SPECTER_SINGLESIG_WALLET_DATA,
            None,
            [BUTTON_PAGE],
        ),
        # 1 Load, from camera, good data - accept
        (
            False,
            tdata.SINGLESIG_12_WORD_KEY,
            tdata.SPECTER_SINGLESIG_WALLET_DATA,
            None,
            [BUTTON_ENTER, BUTTON_ENTER, BUTTON_ENTER],
        ),
        # 2 Load, from camera, good data, decline
        (
            False,
            tdata.SINGLESIG_12_WORD_KEY,
            tdata.SPECTER_SINGLESIG_WALLET_DATA,
            None,
            [BUTTON_ENTER, BUTTON_ENTER, BUTTON_PAGE],
        ),
        # 3 Load, from camera, bad capture
        (False, tdata.SINGLESIG_12_WORD_KEY, None, None, [BUTTON_ENTER, BUTTON_ENTER]),
        # 4 Load, from camera, bad wallet data
        (
            False,
            tdata.SINGLESIG_12_WORD_KEY,
            "{}",
            None,
            [BUTTON_ENTER, BUTTON_ENTER, BUTTON_ENTER],
        ),
        # 5 No print prompt
        (
            True,
            tdata.SINGLESIG_12_WORD_KEY,
            tdata.SPECTER_SINGLESIG_WALLET_DATA,
            None,
            [BUTTON_ENTER],
        ),
        # 6 Print
        (
            True,
            tdata.SINGLESIG_12_WORD_KEY,
            tdata.SPECTER_SINGLESIG_WALLET_DATA,
            MockPrinter(),
            [BUTTON_ENTER, BUTTON_ENTER],
        ),
        # 7 Decline to print
        (
            True,
            tdata.SINGLESIG_12_WORD_KEY,
            tdata.SPECTER_SINGLESIG_WALLET_DATA,
            MockPrinter(),
            [BUTTON_ENTER, BUTTON_PAGE],
        ),
        # 8 Multisig wallet, no print prompt
        (
            True,
            tdata.MULTISIG_12_WORD_KEY,
            tdata.SPECTER_MULTISIG_WALLET_DATA,
            None,
            [BUTTON_ENTER],
        ),
        # 9 vague BlueWallet-ish p2pkh, requires allow_assumption
        (
            False,
            tdata.LEGACY1_KEY,
            tdata.VAGUE_LEGACY1_XPUB,
            None,
            [BUTTON_ENTER, BUTTON_ENTER, BUTTON_ENTER, BUTTON_ENTER],
        ),
        # 10 vague BlueWallet-ish p2pkh w/o key loaded, requires allow_assumption
        (
            False,
            None,
            tdata.VAGUE_LEGACY1_XPUB,
            None,
            [BUTTON_ENTER, BUTTON_ENTER, BUTTON_ENTER, BUTTON_ENTER],
        ),
        # 11 vague BlueWallet-ish p2sh-p2wpkh ypub
        (
            False,
            tdata.NESTEDSW1_KEY,
            tdata.VAGUE_NESTEDSW1_YPUB,
            None,
            [BUTTON_ENTER, BUTTON_ENTER, BUTTON_ENTER],
        ),
        # 12 vague BlueWallet-ish p2sh-p2wpkh ypub w/o key loaded
        (
            False,
            None,
            tdata.VAGUE_NESTEDSW1_YPUB,
            None,
            [BUTTON_ENTER, BUTTON_ENTER, BUTTON_ENTER],
        ),
        # 13 vague BlueWallet-ish p2wpkh zpub
        (
            False,
            tdata.NATIVESW1_KEY,
            tdata.VAGUE_NATIVESW1_ZPUB,
            None,
            [BUTTON_ENTER, BUTTON_ENTER, BUTTON_ENTER],
        ),
        # 14 vague BlueWallet-ish p2wpkh zpub w/o key loaded
        (
            False,
            None,
            tdata.VAGUE_NATIVESW1_ZPUB,
            None,
            [BUTTON_ENTER, BUTTON_ENTER, BUTTON_ENTER],
        ),
        # 1 Load, from SD card, good data, accept
        (
            False,
            tdata.SINGLESIG_12_WORD_KEY,
            tdata.SPECTER_SINGLESIG_WALLET_DATA,
            None,
            [BUTTON_ENTER, BUTTON_PAGE, BUTTON_ENTER, BUTTON_ENTER],
        ),
    ]

    num = 0
    for case in cases:
        print("case: %d" % num)
        num = num + 1
        wallet = Wallet(case[1])
        if case[0]:
            wallet.load(case[2], FORMAT_PMOFN)

        ctx = create_ctx(mocker, case[4], wallet, case[3])
        wallet_descriptor = WalletDescriptor(ctx)
        mocker.patch.object(wallet_descriptor, "has_sd_card", return_value=True)
        mocker.patch.object(
            QRCodeCapture, "qr_capture_loop", new=lambda self: (case[2], FORMAT_PMOFN)
        )
        qr_capturer = mocker.spy(QRCodeCapture, "qr_capture_loop")
        mocker.patch.object(
            wallet_descriptor,
            "display_qr_codes",
            new=lambda data, qr_format, title=None: ctx.input.wait_for_button(),
        )
        mocker.spy(wallet_descriptor, "display_loading_wallet")
        mocker.spy(wallet_descriptor, "display_wallet")

        # Mock SD card descriptor loading
        if case[4][:3] == [BUTTON_ENTER, BUTTON_PAGE, BUTTON_ENTER]:
            mock_utils = mocker.patch("krux.pages.utils.Utils")
            mock_utils.return_value.load_file.return_value = (None, case[2])

        wallet_descriptor.wallet()

        if case[0]:
            # If wallet is already loaded
            wallet_descriptor.display_wallet.assert_called_once()
        else:
            # If accepted the message and choose to load from camera
            if case[4][:2] == [BUTTON_ENTER, BUTTON_ENTER]:
                qr_capturer.assert_called_once()
                if case[2] is not None and case[2] != "{}":
                    wallet_descriptor.display_loading_wallet.assert_called_once()
            # If accepted the message and choose to load from SD
            elif case[4][:3] == [BUTTON_ENTER, BUTTON_PAGE, BUTTON_ENTER]:
                if case[2] is not None and case[2] != "{}":
                    wallet_descriptor.display_loading_wallet.assert_called_once()
        assert ctx.input.wait_for_button.call_count == len(case[4])


def test_loading_miniscript_descriptors(mocker, amigo, wallet_tdata):
    """Miniscript specific tests. Always load from camera"""
    from krux.pages.home_pages.wallet_descriptor import WalletDescriptor
    from krux.wallet import Wallet
    from krux.input import BUTTON_ENTER, BUTTON_PAGE
    from krux.qr import FORMAT_PMOFN
    from krux.pages.qr_capture import QRCodeCapture

    TRIDENT_DESCRIPTOR = "wsh(andor(multi(2,[fbf14e49/45h/1h/0h/3h]tpubDEPmZmWcL9G3XEbhBy6A5UG7tR4hAT7zvhu4cVmCSbVPhjkfuYRgqFnUfG4Gm1NSaoo412nzyRe3UAtC73BHQbVDLz4nAkrhJDSxcYSpUnz/<0;1>/*,[525cb3d5/45h/1h/0h/3h]tpubDF4yVr6ohjK1hQgyHvtLpanC4JxkshsMVUDHfmDvpXcBzdD2peXKdhfLFVNWQekAYAN1vU81dUNfgokZb1foUQfDMtf6X8mb3vMs7cYHbcr/<0;1>/*,[5fc83bce/45h/1h/0h/3h]tpubDFMqbP9gd34rd5Db2hHVYsJA3LnBD2fZo6zWFzeAA2kUC27cndyN2axBs55K9qJSghbvZx1Nyrrvb2ixgLXRzyK7dLLnXHGAmHe7apv4XwU/<0;1>/*),or_i(and_v(v:pkh([5acaced1/49h/1h/0h]tpubDDXMHf1PVPUPYHKyR9b5pbsfcd4SDC5FHtx7msTwazX4gkZPCRjoTYB2mFR4HsiybdptPtKH7yyoogx9d2gvc92SaoCYANEdZYqRR6FJKGx/<0;1>/*),after(230436)),thresh(2,pk([5ecc195f/48h/1h/0h/2h]tpubDFfTpjFSFT9FFvWwXand2JfnRBSpekQQpzdoz5qm8fy6cUhjLdTBuNrqxdsFgyTJ6xr5oeUAqa28VHPMprbosXLhGEgJW4SPa31tuSmp9Ub/<0;1>/*),s:pk([a1088994/48h/1h/0h/2h]tpubDFE64qjVGZ8L31gXFNtRUUpbaZ5viPgkFpth8j3XfGNWgaM6Vsm3F4z1nNE1soY3cQc6YZtNqMqfrywkeAQMiiYnR8N1oyFP5YuuFYTQ2nx/<0;1>/*),s:pk([8faeabe8/48h/1h/0h/2h]tpubDEMz5Gib3V3i1xzY4yaKH2k2J4MBRjNYNSace1YHMr6MgaM1oLZ4qiF7mWQvGPm9gH5bgroqPMr44viw16XWYoig6rbCQrkzakJw6hsapFw/<0;1>/*),snl:after(230220))),and_v(v:thresh(2,pkh([2bd4a49f/84h/1h/1h]tpubDCtwDKhf7tMtt2NDNrWsN7tFQSEvoKt9qvSBMUPuZVnoR52FwSaQS37UT5skDddUyzhVEGJozGxu8CBJPPc8MXhXidD7azaubMHgNCPvq28/<0;1>/*),a:pkh([d38f3599/84h/1h/2h]tpubDDYgycbJd7DgJjKFd4W8Dp8RRNhDDYfLs93cjhBP6boyXiZxdUyZc8fuLMJyetQXq6i9xfYSJwEf1GYxmND6jXExLS9q9ibP2YXZxtqe7mK/<0;1>/*),a:pkh([001ceab0/84h/1h/3h]tpubDCuJUyHrMq4PY4fXEHyADTkFwgy498AnuhrhFzgT7tWuuwp9JAeopqMTre99nzEVnqJNsJk21VRLeLsGz4cA5hboULrupdHqiZdxKRLJV9R/<0;1>/*)),after(230775))))#5flg0r73"

    cases = [
        # 0 - Key
        # 1 - Wallet
        # 2 - Button presses
        (  # Miniscript key, Liana miniscript descriptor
            wallet_tdata.MINISCRIPT_KEY,
            wallet_tdata.LIANA_MINISCRIPT_DESCRIPTOR,
            [
                BUTTON_ENTER,  # Load? Yes
                BUTTON_ENTER,  # Load from camera
                BUTTON_ENTER,  # Accept
            ],
        ),
        (  # No key, Liana miniscript descriptor
            None,
            wallet_tdata.LIANA_MINISCRIPT_DESCRIPTOR,
            [
                BUTTON_ENTER,  # Load? Yes
                BUTTON_ENTER,  # Load from camera
                BUTTON_ENTER,  # Accept
            ],
        ),
        (  # No Key, Trident descriptor
            None,
            TRIDENT_DESCRIPTOR,
            [
                BUTTON_ENTER,  # Load? Yes
                BUTTON_ENTER,  # Load from camera
                BUTTON_ENTER,  # To next page
                BUTTON_ENTER,  # To next page
                BUTTON_ENTER,  # To next page
                BUTTON_ENTER,  # Accept
            ],
        ),
        (  # Taproot miniscript key, Liana taproot miniscript descriptor
            wallet_tdata.TAP_MINISCRIPT_KEY,
            wallet_tdata.LIANA_TAPROOT_MINISCRIPT_DESCRIPTOR,
            [
                BUTTON_ENTER,  # Load? Yes
                BUTTON_ENTER,  # Load from camera
                BUTTON_ENTER,  # Accept
            ],
        ),
        (  # Taproot miniscript key, Liana taproot expanding multisig miniscript descriptor
            wallet_tdata.TAP_MINISCRIPT_KEY,
            wallet_tdata.LIANA_TAP_EXPANDING_MINISCRIPT_DESCRIPTOR,
            [
                BUTTON_ENTER,  # Load? Yes
                BUTTON_ENTER,  # Load from camera
                BUTTON_ENTER,  # To next page
                BUTTON_ENTER,  # Accept
            ],
        ),
    ]

    for case in cases:
        ctx = create_ctx(mocker, case[2], Wallet(case[0]))
        wallet_descriptor = WalletDescriptor(ctx)
        mocker.patch.object(
            QRCodeCapture, "qr_capture_loop", new=lambda self: (case[1], FORMAT_PMOFN)
        )
        mocker.patch.object(
            wallet_descriptor,
            "display_qr_codes",
            new=lambda data, qr_format, title=None: ctx.input.wait_for_button(),
        )
        mocker.spy(wallet_descriptor, "display_loading_wallet")
        wallet_descriptor.wallet()
        wallet_descriptor.display_loading_wallet.assert_called_once()
        assert ctx.input.wait_for_button.call_count == len(case[2])
