def mock_modules(mocker):
    mocker.patch("krux.context.display", new=mocker.MagicMock())
    mocker.patch("krux.context.Camera", new=mocker.MagicMock())
    mocker.patch("krux.context.Light", new=mocker.MagicMock())
    mocker.patch("krux.context.Input", new=mocker.MagicMock())


def test_init(mocker, m5stickv):
    mock_modules(mocker)
    from krux.context import Context

    c = Context()

    assert isinstance(c, Context)


def test_clear(mocker, m5stickv):
    mock_modules(mocker)
    from krux.context import Context
    from krux.wallet import Wallet

    c = Context()
    c.wallet = Wallet(None)

    c.clear()

    assert c.wallet is None


def test_clear_clears_printer(mocker, m5stickv):
    mock_modules(mocker)
    from krux.context import Context
    from krux.printers import Printer

    c = Context()
    c.printer = mocker.MagicMock(clear=mocker.MagicMock())

    c.clear()

    assert c.wallet is None
    c.printer.clear.assert_called()


def test_is_logged_in(mocker, m5stickv):
    from krux.key import TYPE_SINGLESIG

    mock_modules(mocker)
    from krux.context import Context
    from krux.wallet import Wallet
    from krux.key import Key

    c = Context()

    c.wallet = Wallet(None)
    assert c.is_logged_in() == False

    c.wallet = Wallet(
        Key(mnemonic="abandon " * 11 + "about", policy_type=TYPE_SINGLESIG)
    )
    assert c.is_logged_in() == True
