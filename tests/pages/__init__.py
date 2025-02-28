from ..shared_mocks import mock_context


def create_ctx(mocker, btn_seq, wallet=None, printer=None, touch_seq=None):
    """Helper to create mocked context obj"""
    from krux.krux_settings import Settings, THERMAL_ADAFRUIT_TXT

    HASHED_IMAGE_BYTES = b"3\x0fr\x7fKY\x15\t\x83\xaab\x92\x0f&\x820\xb4\x14\x87\x19\xee\x95F\x9c\x8f\x0c\xbdo\xbc\x1d\xcbT"

    ctx = mock_context(mocker)
    ctx.power_manager.battery_charge_remaining.return_value = 1
    ctx.input.wait_for_button = mocker.MagicMock(side_effect=btn_seq)
    ctx.camera.capture_entropy = mocker.MagicMock(return_value=HASHED_IMAGE_BYTES)
    ctx.display.qr_offset = mocker.MagicMock(return_value=250)
    ctx.is_logged_in.return_value = False

    ctx.wallet = wallet
    ctx.printer = printer
    if printer is not None:
        mocker.patch("krux.printers.create_printer", new=mocker.MagicMock())
        Settings().hardware.printer.driver = THERMAL_ADAFRUIT_TXT
    elif Settings().hardware.printer.driver != "none":
        Settings().hardware.printer.driver = "none"

    if touch_seq:
        ctx.input.touch = mocker.MagicMock(
            current_index=mocker.MagicMock(side_effect=touch_seq)
        )
    return ctx
