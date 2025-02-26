import pytest
from ..shared_mocks import mock_context
from . import create_ctx

TEST_QR_DATA = "test"
TEST_QR_DATA_IMAGE = bytearray(
    b"\x7f\xd3?H\nvU\xdd\xae\xa4\xdbut\x83\x80\xe0_\xf5\x070\x00O%7\x97\xd2\xd6\xd1\xe7\xc6\x1ae\xe5\xb2\x00J\xd5\x1f\xd9\t\xd23]N\xbckdu\xb5\x94\xa0\xaf\xf9\xb7\t\x00"
)


@pytest.fixture
def mock_page_cls(mocker):
    from krux.pages import Page, Menu

    class MockPage(Page):
        def __init__(self, ctx):
            Page.__init__(
                self,
                ctx,
                Menu(
                    ctx,
                    [
                        (("Test"), mocker.MagicMock()),
                    ],
                ),
            )

    return MockPage


def test_init(mocker, m5stickv, mock_page_cls):
    from krux.pages import Page

    page = mock_page_cls(mock_context(mocker))

    assert isinstance(page, Page)


def test_flash_text(mocker, m5stickv, mock_page_cls):
    from krux.display import FLASH_MSG_TIME
    from krux.themes import WHITE, RED

    ctx = mock_context(mocker)
    mocker.patch("time.ticks_ms", new=lambda: 0)
    page = mock_page_cls(ctx)

    page.flash_text("Hello world", duration=1000)

    ctx.display.flash_text.assert_called_with("Hello world", WHITE, 1000)

    page.flash_error("Error")

    assert ctx.display.flash_text.call_count == 2
    ctx.display.flash_text.assert_called_with("Error", RED, FLASH_MSG_TIME)


def test_prompt_m5stickv(mocker, m5stickv, mock_page_cls):
    from krux.input import BUTTON_ENTER, BUTTON_PAGE

    ctx = mock_context(mocker)
    page = mock_page_cls(ctx)

    # Enter pressed
    ctx.input.wait_for_button = mocker.MagicMock(side_effect=[BUTTON_ENTER])
    assert page.prompt("test prompt") == True

    # Page pressed
    ctx.input.wait_for_button = mocker.MagicMock(side_effect=[BUTTON_PAGE])
    assert page.prompt("test prompt") == False


def test_prompt_amigo(mocker, amigo, mock_page_cls):
    from krux.input import BUTTON_ENTER, BUTTON_PAGE, BUTTON_TOUCH

    ctx = mock_context(mocker)
    page = mock_page_cls(ctx)

    # Enter pressed
    ctx.input.wait_for_button = mocker.MagicMock(side_effect=[BUTTON_ENTER])
    assert page.prompt("test prompt") == True

    # Page, than Enter pressed
    page_press = [BUTTON_PAGE, BUTTON_ENTER]
    ctx.input.wait_for_button = mocker.MagicMock(side_effect=page_press)
    assert page.prompt("test prompt") == False

    ctx.input.buttons_active = False
    # Index 1 = YES pressed
    ctx.input.touch = mocker.MagicMock(current_index=mocker.MagicMock(side_effect=[1]))
    ctx.input.wait_for_button = mocker.MagicMock(side_effect=[BUTTON_TOUCH])
    assert page.prompt("test prompt") == True

    # Index 0 = No pressed
    ctx.input.touch = mocker.MagicMock(current_index=mocker.MagicMock(side_effect=[0]))
    ctx.input.wait_for_button = mocker.MagicMock(side_effect=[BUTTON_TOUCH])
    assert page.prompt("test prompt") == False


def test_display_qr_code(mocker, m5stickv, mock_page_cls):
    from krux.input import BUTTON_ENTER
    from krux.qr import FORMAT_NONE

    ctx = create_ctx(mocker, [BUTTON_ENTER])
    page = mock_page_cls(ctx)

    # Test QR code display
    page.display_qr_codes(TEST_QR_DATA, FORMAT_NONE)

    assert ctx.input.wait_for_button.call_count == 1
    assert ctx.display.draw_qr_code.call_count == 1
    assert ctx.display.draw_qr_code.call_args == mocker.call(0, TEST_QR_DATA_IMAGE)


def test_display_qr_code_light_theme(mocker, m5stickv, mock_page_cls):
    from krux.input import BUTTON_ENTER
    from krux.qr import FORMAT_NONE
    from krux.themes import theme, WHITE

    ctx = create_ctx(mocker, [BUTTON_ENTER])
    page = mock_page_cls(ctx)

    # Mock light theme background color
    theme.bg_color = WHITE
    # Test QR code display
    page.display_qr_codes(TEST_QR_DATA, FORMAT_NONE)

    assert ctx.input.wait_for_button.call_count == 1
    assert ctx.display.draw_qr_code.call_count == 1
    assert ctx.display.draw_qr_code.call_args == mocker.call(
        0, TEST_QR_DATA_IMAGE, light_color=WHITE
    )


def test_display_qr_code_loop_through_brightness(mocker, m5stickv, mock_page_cls):
    from krux.input import BUTTON_ENTER, BUTTON_PAGE
    from krux.qr import FORMAT_NONE
    from krux.themes import WHITE, DARKGREY

    BTN_SEQUENCE = [
        *([BUTTON_PAGE] * 3),  # Loop through brightness
        BUTTON_ENTER,  # Exit
    ]

    ctx = create_ctx(mocker, BTN_SEQUENCE)
    page = mock_page_cls(ctx)

    # Test QR code display
    page.display_qr_codes(TEST_QR_DATA, FORMAT_NONE)

    assert ctx.input.wait_for_button.call_count == len(BTN_SEQUENCE)
    assert ctx.display.draw_qr_code.call_count == len(BTN_SEQUENCE)
    assert ctx.display.draw_qr_code.call_args_list == [
        mocker.call(0, TEST_QR_DATA_IMAGE),  # Default
        mocker.call(0, TEST_QR_DATA_IMAGE, light_color=WHITE),  # Brighter
        mocker.call(0, TEST_QR_DATA_IMAGE, light_color=DARKGREY),  # Darker
        mocker.call(0, TEST_QR_DATA_IMAGE),  # Default
    ]


def get_frame_titles_resulting_from_input(
    mocker, mock_page_cls, title, input_seq, use_buttons=False, has_touch=True
):
    from krux.input import BUTTON_TOUCH, SWIPE_RIGHT, BUTTON_PAGE, BUTTON_ENTER
    from krux.pages.keypads import Keypad

    def get_button_seq(key_index):
        return [*([BUTTON_PAGE] * (key_index - 1))] + [BUTTON_ENTER]

    keysets = ["123", "456"]  # both should be the same length
    pad = Keypad(create_ctx(mocker, None), keysets, None)

    button_seq = []
    touch_seq = [] if has_touch else None
    input_seq.append("go key")  # to exit capture_from_keypad

    if has_touch and not use_buttons:
        for i in input_seq:
            if i == "more key":
                button_seq.append(BUTTON_TOUCH)
                touch_seq.append(pad.more_index)
            elif i == "go key":
                button_seq.append(BUTTON_TOUCH)
                touch_seq.append(pad.go_index)
            elif i == "normal key":
                button_seq.append(BUTTON_TOUCH)
                touch_seq.append(1)
            elif i == "swipe":
                button_seq.append(SWIPE_RIGHT)
    else:
        for i in input_seq:
            if i == "more key":
                button_seq = button_seq + get_button_seq(pad.more_index)
            elif i == "go key":
                button_seq = button_seq + get_button_seq(pad.go_index)
            elif i == "normal key":
                button_seq = button_seq + get_button_seq(1)

    ctx = create_ctx(mocker, button_seq, None, None, touch_seq)
    if not has_touch:
        ctx.input.touch = None
    page = mock_page_cls(ctx)
    captured = page.capture_from_keypad(title, keysets)
    frame_titles = [
        t[0][0] for t in ctx.display.draw_hcentered_text.call_args_list if t[0][1] == 10
    ]
    return frame_titles


def test_keypad_esc_no_exit(mocker, amigo):
    from krux.pages import Page, LETTERS
    from krux.input import BUTTON_ENTER, BUTTON_PAGE_PREV

    btn_seq = (
        [BUTTON_PAGE_PREV] * 2  # go to ESC
        + [BUTTON_ENTER]  # press ESC to exit
        + [BUTTON_PAGE_PREV, BUTTON_ENTER]  # No
        + [BUTTON_ENTER]  # press ESC to exit
        + [BUTTON_ENTER]  # Yes
    )

    ctx = create_ctx(mocker, btn_seq)
    assert ctx.input.touch is not None

    page = Page(ctx)
    page.capture_from_keypad("test", [LETTERS])

    assert ctx.input.touch.set_regions.call_count == 4


def test_keypad_swipe_hint_is_shown_after_more_keypress_and_cleared_after_other_keypress(
    mocker, amigo, mock_page_cls
):
    frame_titles = get_frame_titles_resulting_from_input(
        mocker,
        mock_page_cls,
        "title",
        ["more key", "normal key", "normal key", "more key"],
    )
    assert frame_titles[0] == "title"  # initial
    assert frame_titles[1] == "« swipe »"  # after more key
    assert frame_titles[2] == "title"  # after normal key
    assert frame_titles[3] == "title"  # after normal key
    assert frame_titles[4] == "« swipe »"  # after more key


def test_keypad_swipe_hint_is_not_shown_once_user_has_swiped(
    mocker, amigo, mock_page_cls
):
    frame_titles = get_frame_titles_resulting_from_input(
        mocker,
        mock_page_cls,
        "title",
        ["normal key", "more key", "normal key", "swipe", "more key"],
    )
    assert frame_titles[0] == "title"  # initial
    assert frame_titles[1] == "title"  # after normal key
    assert frame_titles[2] == "« swipe »"  # after more key
    assert frame_titles[3] == "title"  # after normal key
    assert frame_titles[4] == "title"  # after swipe
    assert frame_titles[5] == "title"  # after more key (NO MORE HINT)


def test_keypad_swipe_hint_is_not_shown_on_nontouch_device(
    mocker, amigo, mock_page_cls
):
    # first check we get a hint if we have a touchscreen
    frame_titles = get_frame_titles_resulting_from_input(
        mocker,
        mock_page_cls,
        "title",
        ["more key"],
        use_buttons=True,  # force use of buttons so that we're using non-touch input
        has_touch=True,
    )
    assert "« swipe »" in frame_titles

    # now check that the same input does *not* show hint if we don't have a touchscreen
    frame_titles = get_frame_titles_resulting_from_input(
        mocker,
        mock_page_cls,
        "title",
        ["more key"],
        use_buttons=True,
        has_touch=False,  # this time no touch screen
    )
    assert "« swipe »" not in frame_titles
