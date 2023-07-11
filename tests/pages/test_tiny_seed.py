from ..shared_mocks import MockPrinter, mock_context


def create_ctx(mocker, btn_seq, wallet=None, printer=None, touch_seq=None):
    """Helper to create mocked context obj"""
    ctx = mock_context(mocker)
    ctx.power_manager.battery_charge_remaining.return_value = 1
    ctx.input.wait_for_button = mocker.MagicMock(side_effect=btn_seq)

    ctx.wallet = wallet
    ctx.printer = printer

    if touch_seq:
        ctx.input.touch = mocker.MagicMock(
            current_index=mocker.MagicMock(side_effect=touch_seq)
        )
    return ctx


def test_export_tiny_seed(m5stickv, mocker):
    from krux.pages.tiny_seed import TinySeed
    from krux.input import BUTTON_ENTER
    from krux.wallet import Wallet
    from krux.key import Key
    from embit.networks import NETWORKS

    BTN_SEQUENCE = [
        BUTTON_ENTER,  # Page 1
        BUTTON_ENTER,  # Page 2
        BUTTON_ENTER,  # Print - yes
    ]
    TEST_24_WORD_MNEMONIC = "brush badge sing still venue panther kitchen please help panel bundle excess sign couch stove increase human once effort candy goat top tiny major"
    # Amount of rectangles filled for this mnemonic + menus
    FILLED_RECTANGLES = 189
    SINGLEKEY_24_WORD_KEY = Key(TEST_24_WORD_MNEMONIC, False, NETWORKS["main"])
    ctx = create_ctx(mocker, BTN_SEQUENCE, Wallet(SINGLEKEY_24_WORD_KEY), MockPrinter())
    tiny_seed = TinySeed(ctx)
    tiny_seed.export()

    assert ctx.display.fill_rectangle.call_count == FILLED_RECTANGLES


def test_enter_tiny_seed_12w_m5stickv(m5stickv, mocker):
    from krux.pages.tiny_seed import TinySeed
    from krux.input import BUTTON_ENTER, BUTTON_PAGE, BUTTON_PAGE_PREV

    BTN_SEQUENCE = (
        # Toggle line 1 bit "1024"
        [BUTTON_PAGE]
        + [BUTTON_ENTER]
        # Move to last editable bit and togle
        + [BUTTON_PAGE_PREV] * 4
        + [BUTTON_ENTER]
        # Move to line 2 and toggle bit "512"
        + [BUTTON_PAGE] * 17
        + [BUTTON_ENTER]
        # Move to line 3 and toggle bit "512"
        + [BUTTON_PAGE] * 12
        + [BUTTON_ENTER]
        # Press Enter to toggle again and reset line 3 to 2048 word
        + [BUTTON_ENTER]
        # Move to line 1 , toggle bit 2048 to reset line 1
        + [BUTTON_PAGE_PREV] * 26
        + [BUTTON_ENTER]
        # Move to "Go" and proceed
        + [BUTTON_PAGE_PREV]
        + [BUTTON_ENTER]
    )
    TEST_12_WORDS = [
        "zoo",
        "divide",
        "zoo",
        "zoo",
        "zoo",
        "zoo",
        "zoo",
        "zoo",
        "zoo",
        "zoo",
        "zoo",
        "crouch",
    ]

    ctx = create_ctx(mocker, BTN_SEQUENCE)
    tiny_seed = TinySeed(ctx)
    words = tiny_seed.enter_tiny_seed()

    assert ctx.input.wait_for_button.call_count == len(BTN_SEQUENCE)
    assert words == TEST_12_WORDS


def test_enter_tiny_seed_24w_m5stickv(m5stickv, mocker):
    from krux.pages.tiny_seed import TinySeed
    from krux.input import BUTTON_ENTER, BUTTON_PAGE, BUTTON_PAGE_PREV

    BTN_SEQUENCE = (
        # Toggle line 1 bit "1024"
        [BUTTON_PAGE]
        + [BUTTON_ENTER]
        # Move to last editable bit and togle
        + [BUTTON_PAGE_PREV] * 4
        + [BUTTON_ENTER]
        # Move to line 2 and toggle bit "512"
        + [BUTTON_PAGE] * 17
        + [BUTTON_ENTER]
        # Move to "Go" and proceed to next page
        + [BUTTON_PAGE_PREV] * 15
        + [BUTTON_ENTER]
        # Toggle line 1 bit "256"
        + [BUTTON_PAGE] * 4
        + [BUTTON_ENTER]
        # Move to last editable bit and togle
        + [BUTTON_PAGE_PREV] * 6
        + [BUTTON_ENTER]
        # Move to "Go" and proceed
        + [BUTTON_PAGE] * 2
        + [BUTTON_ENTER]
    )
    TEST_24_WORDS = [
        "lend",
        "divide",
        "zoo",
        "zoo",
        "zoo",
        "zoo",
        "zoo",
        "zoo",
        "zoo",
        "zoo",
        "zoo",
        "abandon",
        "cable",
        "zoo",
        "zoo",
        "zoo",
        "zoo",
        "zoo",
        "zoo",
        "zoo",
        "zoo",
        "zoo",
        "zoo",
        "core",
    ]

    ctx = create_ctx(mocker, BTN_SEQUENCE)
    tiny_seed = TinySeed(ctx)
    words = tiny_seed.enter_tiny_seed(w24=True)

    assert ctx.input.wait_for_button.call_count == len(BTN_SEQUENCE)
    assert words == TEST_24_WORDS


def test_enter_tiny_seed_24w_amigo(amigo_tft, mocker):
    from krux.pages.tiny_seed import TinySeed
    from krux.input import BUTTON_TOUCH

    TOUCH_SEQUENCE = (
        # Toggle line 1 bit "1024"
        [1]
        # Toggle last editable bit
        + [143]
        # On line 2 and toggle bit "512"
        + [14]
        # "Go" and proceed to next page
        + [165]
        # Toggle line 1 bit "256"
        + [3]
        # Toggle to last editable bit
        + [135]
        # Press on invalid location
        + [146]
        # Press ESC
        + [158]
        # Give up from ESC
        + [1]  # Press "No"
        # "Go" and proceed
        + [165]
    )
    BTN_SEQUENCE = [BUTTON_TOUCH] * len(TOUCH_SEQUENCE)

    TEST_24_WORDS = [
        "lend",
        "divide",
        "zoo",
        "zoo",
        "zoo",
        "zoo",
        "zoo",
        "zoo",
        "zoo",
        "zoo",
        "zoo",
        "abandon",
        "cable",
        "zoo",
        "zoo",
        "zoo",
        "zoo",
        "zoo",
        "zoo",
        "zoo",
        "zoo",
        "zoo",
        "zoo",
        "core",
    ]

    ctx = create_ctx(mocker, BTN_SEQUENCE, touch_seq=TOUCH_SEQUENCE)
    tiny_seed = TinySeed(ctx)
    words = tiny_seed.enter_tiny_seed(w24=True)

    assert ctx.input.wait_for_button.call_count == len(BTN_SEQUENCE)
    assert words == TEST_24_WORDS


def test_enter_tiny_seed_24w_pre_loaded_numbers(m5stickv, mocker):
    # This will be used when scanning 24 TinySeed
    # First scanned page will be loaded to be edited, then proceed to scan second page
    # Seed will be returned as its word index
    from krux.pages.tiny_seed import TinySeed
    from krux.input import BUTTON_ENTER, BUTTON_PAGE, BUTTON_PAGE_PREV

    BTN_SEQUENCE = (
        # [BUTTON_ENTER]
        # Toggle line 1 bit "1024"
        [BUTTON_PAGE] * 2
        + [BUTTON_ENTER]
        # Move to last editable bit from page 1 and togle
        + [BUTTON_PAGE_PREV] * 4
        + [BUTTON_ENTER]
        # Move to line 2 and toggle bit "512"
        + [BUTTON_PAGE] * 17
        + [BUTTON_ENTER]
        # Move to "Go" and proceed to scan second page
        + [BUTTON_PAGE_PREV] * 15
        + [BUTTON_ENTER]
    )
    TEST_12_WORDS = [
        1025,
        513,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        2048,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
    ]

    ctx = create_ctx(mocker, BTN_SEQUENCE)
    tiny_seed = TinySeed(ctx)
    words = tiny_seed.enter_tiny_seed(w24=True, seed_numbers=[1] * 24, scanning_24=True)

    assert ctx.input.wait_for_button.call_count == len(BTN_SEQUENCE)
    assert words == TEST_12_WORDS


def test_scan_tiny_seed_12w(m5stickv, mocker):
    # This will be used when scanning 24 TinySeed
    # First scanned page will be loaded to be edited, then proceed to scan second page
    # Seed will be returned as its word index
    import time
    from krux.pages.tiny_seed import TinyScanner
    from krux.input import BUTTON_ENTER, BUTTON_PAGE, BUTTON_PAGE_PREV

    BTN_SEQUENCE = (
        [BUTTON_ENTER]
        + [BUTTON_ENTER]
        # # Toggle line 1 bit "1024"
        # [BUTTON_ENTER] * 2
        # + [BUTTON_ENTER]
        # # Move to last editable bit from page 1 and togle
        # + [BUTTON_PAGE_PREV] * 4
        # + [BUTTON_ENTER]
        # # Move to line 2 and toggle bit "512"
        # + [BUTTON_PAGE] * 17
        # + [BUTTON_ENTER]
        # # Move to "Go" and proceed to scan second page
        # + [BUTTON_PAGE_PREV] * 15
        # + [BUTTON_ENTER]
    )
    TIME_STAMPS = (0, 1, 100)
    TINYSEED_RECTANGLE = (10, 10, 100, 100)
    TEST_12_WORDS_NUMBERS = [
        335,
        1884,
        1665,
        1811,
        1198,
        1397,
        1292,
        1559,
        48,
        1069,
        794,
        1678,
    ]
    TEST_12_WORDS = [
        "clap",
        "twin",
        "source",
        "time",
        "noble",
        "purse",
        "pause",
        "security",
        "album",
        "machine",
        "glimpse",
        "spider",
    ]
    mocker.patch.object(time, "ticks_ms", mocker.MagicMock(side_effect=TIME_STAMPS))
    ctx = create_ctx(mocker, BTN_SEQUENCE)
    tiny_seed = TinyScanner(ctx)
    mocker.patch.object(
        tiny_seed, "_detect_tiny_seed", new=lambda image: TINYSEED_RECTANGLE
    )
    mocker.patch.object(
        tiny_seed, "_detect_and_draw_punches", new=lambda image: TEST_12_WORDS_NUMBERS
    )
    mocker.patch.object(tiny_seed, "_check_buttons", new=lambda w24, page: None)
    words = tiny_seed.scanner()

    assert ctx.input.wait_for_button.call_count == len(BTN_SEQUENCE)
    assert words == TEST_12_WORDS
