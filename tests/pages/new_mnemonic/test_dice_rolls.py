from .. import create_ctx
from embit import bip39

# rolls which will result in good entropy
PATTERN_ROLLS_TOUCH_SEQUENCE = (
    [0] * 9  # 9 number 1 presses
    + [1] * 9  # 9 number 2 presses
    + [2] * 6  # 6 number 3 presses
    + [3] * 10  # 10 number 4 presses
    + [4] * 7  # 7 number 5 presses
    + [5] * 9  # 9 number 6 presses
)

# rolls which will result in poor entropy
POOR_ROLLS_TOUCH_SEQUENCE = (
    [0] * 10  # 10 number 1 presses
    + [1] * 10  # 10 number 2 presses
    + [2] * 10  # 10 number 3 presses
    + [3] * 10  # 16 number 4 presses
    + [4] * 6  # 2 number 5 presses
    + [5] * 4  # 2 number 6 presses
)

GOOD_ROLLS_SEQUENCE = [
    1,
    4,
    5,
    2,
    0,
    3,
    2,
    4,
    4,
    5,
    5,
    5,
    0,
    5,
    2,
    3,
    2,
    5,
    2,
    5,
    0,
    5,
    2,
    1,
    4,
    3,
    0,
    5,
    3,
    4,
    1,
    0,
    3,
    0,
    3,
    5,
    5,
    4,
    2,
    1,
    4,
    1,
    5,
    4,
    5,
    2,
    0,
    3,
    3,
    0,
]


def test_new_12w_from_d6(m5stickv, mocker):
    from krux.pages.new_mnemonic.dice_rolls import DiceEntropy, D6_12W_MIN_ROLLS
    from krux.input import BUTTON_ENTER, BUTTON_PAGE, BUTTON_PAGE_PREV

    BTN_SEQUENCE = (
        # 1 press to proceed to 12 words
        [BUTTON_ENTER]
        +
        # 1 press to proceed msg
        [BUTTON_ENTER]
        +
        # 1 presses per roll
        [BUTTON_ENTER for _ in range(D6_12W_MIN_ROLLS)]
        +
        # 1 press prev and 1 press on btn Go
        [BUTTON_PAGE_PREV, BUTTON_ENTER]
        + [
            BUTTON_ENTER,  # proceed with poor entropy,
            BUTTON_PAGE,  # move to Generate Words, while seeing rolls
            BUTTON_ENTER,  # generate words
            BUTTON_ENTER,  # 1 press to confirm SHA
        ]
    )
    MNEMONIC = "diet glad hat rural panther lawsuit act drop gallery urge where fit"

    ctx = create_ctx(mocker, BTN_SEQUENCE)
    dice_entropy = DiceEntropy(ctx)
    entropy = dice_entropy.new_key()
    words = bip39.mnemonic_from_bytes(entropy)

    assert ctx.input.wait_for_button.call_count == len(BTN_SEQUENCE)
    assert words == MNEMONIC


def test_new_24w_from_d6(m5stickv, mocker):
    from krux.pages.new_mnemonic.dice_rolls import DiceEntropy, D6_24W_MIN_ROLLS
    from krux.input import BUTTON_ENTER, BUTTON_PAGE, BUTTON_PAGE_PREV

    BTN_SEQUENCE = (
        # 1 press change to 24 words and 1 press to proceed
        [BUTTON_PAGE, BUTTON_ENTER]
        +
        # 1 press to proceed msg
        [BUTTON_ENTER]
        +
        # 1 presses per roll
        [BUTTON_ENTER for _ in range(D6_24W_MIN_ROLLS)]
        +
        # 1 press prev and 1 press on btn Go
        [BUTTON_PAGE_PREV, BUTTON_ENTER]
        + [
            BUTTON_ENTER,  # proceed with poor entropy,
            BUTTON_PAGE,  # move to Generate Words, while seeing rolls
            BUTTON_ENTER,  # generate words
            BUTTON_ENTER,  # 1 press to confirm SHA
        ]
    )
    MNEMONIC = "wheel erase puppy pistol chapter accuse carpet drop quote final attend near scrap satisfy limit style crunch person south inspire lunch meadow enact tattoo"

    ctx = create_ctx(mocker, BTN_SEQUENCE)
    dice_entropy = DiceEntropy(ctx)
    entropy = dice_entropy.new_key()
    words = bip39.mnemonic_from_bytes(entropy)

    assert ctx.input.wait_for_button.call_count == len(BTN_SEQUENCE)
    assert words == MNEMONIC


def test_new_12w_from_d6_on_amigo_device(amigo, mocker):
    from krux.pages.new_mnemonic.dice_rolls import DiceEntropy, D6_12W_MIN_ROLLS
    from krux.input import BUTTON_ENTER, BUTTON_PAGE, BUTTON_PAGE_PREV

    BTN_SEQUENCE = (
        # 1 press to proceed to 12 words
        [BUTTON_ENTER]
        +
        # 1 press to proceed msg
        [BUTTON_ENTER]
        +
        # 1 presses per roll
        [BUTTON_ENTER for _ in range(D6_12W_MIN_ROLLS)]
        +
        # 1 press prev and 1 press on btn Go
        [BUTTON_PAGE_PREV, BUTTON_ENTER]
        + [
            BUTTON_ENTER,  # proceed with poor entropy,
            BUTTON_PAGE,  # move to Generate Words, while seeing rolls
            BUTTON_ENTER,  # generate words
            BUTTON_ENTER,  # 1 press to confirm SHA
        ]
    )
    MNEMONIC = "diet glad hat rural panther lawsuit act drop gallery urge where fit"

    ctx = create_ctx(mocker, BTN_SEQUENCE)
    dice_entropy = DiceEntropy(ctx)
    entropy = dice_entropy.new_key()
    words = bip39.mnemonic_from_bytes(entropy)

    assert ctx.input.wait_for_button.call_count == len(BTN_SEQUENCE)
    assert words == MNEMONIC


def test_new_24w_from_d6_on_amigo_device(amigo, mocker):
    from krux.pages.new_mnemonic.dice_rolls import DiceEntropy, D6_24W_MIN_ROLLS
    from krux.input import BUTTON_ENTER, BUTTON_PAGE, BUTTON_PAGE_PREV

    BTN_SEQUENCE = (
        # 1 press change to 24 words and 1 press to proceed
        [BUTTON_PAGE, BUTTON_ENTER]
        +
        # 1 press to proceed msg
        [BUTTON_ENTER]
        +
        # 1 presses per roll
        [BUTTON_ENTER for _ in range(D6_24W_MIN_ROLLS)]
        +
        # 1 press prev and 1 press on btn Go
        [BUTTON_PAGE_PREV, BUTTON_ENTER]
        + [
            BUTTON_ENTER,  # proceed with poor entropy,
            BUTTON_PAGE,  # move to Generate Words, while seeing rolls
            BUTTON_ENTER,  # generate words
            BUTTON_ENTER,  # 1 press to confirm SHA
        ]
    )
    MNEMONIC = "wheel erase puppy pistol chapter accuse carpet drop quote final attend near scrap satisfy limit style crunch person south inspire lunch meadow enact tattoo"

    ctx = create_ctx(mocker, BTN_SEQUENCE)
    dice_entropy = DiceEntropy(
        ctx,
    )
    entropy = dice_entropy.new_key()
    words = bip39.mnemonic_from_bytes(entropy)

    assert ctx.input.wait_for_button.call_count == len(BTN_SEQUENCE)
    assert words == MNEMONIC


def test_cancel_new_12w_from_d6_on_amigo_device(amigo, mocker):
    "Will test the Esc button on the roll screen"
    from krux.pages.new_mnemonic.dice_rolls import DiceEntropy
    from krux.input import BUTTON_ENTER, BUTTON_PAGE_PREV

    BTN_SEQUENCE = (
        # 1 press to proceed to 12 words
        [BUTTON_ENTER]
        +
        # 1 press to proceed msg
        [BUTTON_ENTER]
        +
        # 2 press prev and 1 press on btn Esc
        [BUTTON_PAGE_PREV, BUTTON_PAGE_PREV, BUTTON_ENTER]
        +
        # 1 press to proceed confirm exit msg
        [BUTTON_ENTER]
    )

    ctx = create_ctx(mocker, BTN_SEQUENCE)
    dice_entropy = DiceEntropy(ctx, is_d20=True)
    dice_entropy.new_key()

    assert ctx.input.wait_for_button.call_count == len(BTN_SEQUENCE)


def test_new_12w_from_d20(m5stickv, mocker):
    from krux.pages.new_mnemonic.dice_rolls import DiceEntropy, D20_12W_MIN_ROLLS
    from krux.input import BUTTON_ENTER, BUTTON_PAGE, BUTTON_PAGE_PREV

    BTN_SEQUENCE = (
        # 1 press to proceed to 12 words
        [BUTTON_ENTER]
        +
        # 1 press to proceed msg
        [BUTTON_ENTER]
        +
        # 1 presses per roll
        [BUTTON_ENTER for _ in range(D20_12W_MIN_ROLLS)]
        +
        # 1 press prev and 1 press on btn Go
        [BUTTON_PAGE_PREV, BUTTON_ENTER]
        + [
            BUTTON_ENTER,  # proceed with poor entropy,
            BUTTON_PAGE,  # move to Generate Words, while seeing rolls
            BUTTON_ENTER,  # generate words
            BUTTON_ENTER,  # 1 press to confirm SHA
        ]
    )
    MNEMONIC = (
        "erupt remain ride bleak year cabin orange sure ghost gospel husband oppose"
    )

    ctx = create_ctx(mocker, BTN_SEQUENCE)
    dice_entropy = DiceEntropy(ctx, is_d20=True)
    entropy = dice_entropy.new_key()
    words = bip39.mnemonic_from_bytes(entropy)

    assert ctx.input.wait_for_button.call_count == len(BTN_SEQUENCE)
    assert words == MNEMONIC


def test_new_24w_from_d20(m5stickv, mocker):
    from krux.pages.new_mnemonic.dice_rolls import DiceEntropy, D20_24W_MIN_ROLLS
    from krux.input import BUTTON_ENTER, BUTTON_PAGE, BUTTON_PAGE_PREV

    BTN_SEQUENCE = (
        # 1 press change to 24 words and 1 press to proceed
        [BUTTON_PAGE, BUTTON_ENTER]
        +
        # 1 press to proceed msg
        [BUTTON_ENTER]
        +
        # 1 presses per roll
        [BUTTON_ENTER for _ in range(D20_24W_MIN_ROLLS)]
        +
        # 1 press prev and 1 press on btn Go
        [BUTTON_PAGE_PREV, BUTTON_ENTER]
        + [
            BUTTON_ENTER,  # proceed with poor entropy,
            BUTTON_PAGE,  # move to Generate Words, while seeing rolls
            BUTTON_ENTER,  # generate words
            BUTTON_ENTER,  # 1 press to confirm SHA
        ]
    )
    MNEMONIC = "fun island vivid slide cable pyramid device tuition only essence thought gain silk jealous eternal anger response virus couple faculty ozone test key vocal"

    ctx = create_ctx(mocker, BTN_SEQUENCE)
    dice_entropy = DiceEntropy(ctx, is_d20=True)
    entropy = dice_entropy.new_key()
    words = bip39.mnemonic_from_bytes(entropy)

    assert ctx.input.wait_for_button.call_count == len(BTN_SEQUENCE)
    assert words == MNEMONIC


def test_cancel_new_12w_from_d20(m5stickv, mocker):
    "Will test the Deletion button and the minimum roll on the roll screen"
    from krux.pages.new_mnemonic.dice_rolls import DiceEntropy, D20_12W_MIN_ROLLS
    from krux.input import BUTTON_ENTER, BUTTON_PAGE, BUTTON_PAGE_PREV

    BTN_SEQUENCE = (
        # 1 press to proceed to 12 words
        [BUTTON_ENTER]
        +
        # 1 press to proceed msg
        [BUTTON_ENTER]
        +
        # 1 presses per roll
        [BUTTON_ENTER for _ in range(D20_12W_MIN_ROLLS)]
        +
        # 3 press prev and 1 press on btn < (delete last roll)
        [BUTTON_PAGE_PREV, BUTTON_PAGE_PREV, BUTTON_PAGE_PREV, BUTTON_ENTER]
        +
        # 1 press prev and 1 press on btn Go
        [BUTTON_PAGE_PREV, BUTTON_ENTER]
        +
        # 1 press for msg not enough rolls!
        [BUTTON_ENTER]
        +
        # 2 press prev and 1 press on btn Esc
        [BUTTON_PAGE_PREV, BUTTON_PAGE_PREV, BUTTON_ENTER]
        +
        # 1 press to proceed confirm exit msg
        [BUTTON_ENTER]
    )

    ctx = create_ctx(mocker, BTN_SEQUENCE)
    dice_entropy = DiceEntropy(ctx, is_d20=True)
    dice_entropy.new_key()

    assert ctx.input.wait_for_button.call_count == len(BTN_SEQUENCE)


# Test low entropy warning
def test_low_shannon_entropy_warning(amigo, mocker):
    from krux.pages.new_mnemonic.dice_rolls import DiceEntropy, D6_12W_MIN_ROLLS
    from krux.input import BUTTON_ENTER, BUTTON_PAGE, BUTTON_PAGE_PREV, BUTTON_TOUCH

    BTN_SEQUENCE = (
        # 1 press to proceed to 12 words
        [BUTTON_ENTER]
        +
        # 1 press to proceed msg
        [BUTTON_ENTER]
        +
        # 10 number 1 presses
        [BUTTON_TOUCH for _ in range(D6_12W_MIN_ROLLS)]
        +
        # 1 press prev and 1 press on btn Go
        [BUTTON_PAGE_PREV, BUTTON_ENTER]
        + [
            BUTTON_ENTER,  # proceed with poor entropy,
            BUTTON_PAGE,  # move to Generate Words, while seeing rolls
            BUTTON_ENTER,  # generate words
            BUTTON_ENTER,  # 1 press to confirm SHA
        ]
    )

    ctx = create_ctx(mocker, BTN_SEQUENCE, touch_seq=POOR_ROLLS_TOUCH_SEQUENCE)
    dice_entropy = DiceEntropy(ctx)
    dice_entropy.new_key()

    assert ctx.input.wait_for_button.call_count == len(BTN_SEQUENCE)

    # Assert ctx.display.draw_centered_text was called with poor entropy warning"
    call_message = mocker.call("Poor entropy!\nPattern detected!")
    ctx.display.draw_centered_text.assert_has_calls([call_message])


# Test low entropy warning is not shown when Shannon's entropy is good
def test_good_rolls(amigo, mocker):
    from krux.pages.new_mnemonic.dice_rolls import DiceEntropy, D6_12W_MIN_ROLLS
    from krux.input import BUTTON_ENTER, BUTTON_PAGE, BUTTON_PAGE_PREV, BUTTON_TOUCH

    BTN_SEQUENCE = (
        # 1 press to proceed to 12 words
        [BUTTON_ENTER]
        +
        # 1 press to proceed msg
        [BUTTON_ENTER]
        +
        # 10 number 1 presses
        [BUTTON_TOUCH for _ in range(D6_12W_MIN_ROLLS)]
        +
        # 1 press prev and 1 press on btn Go
        [BUTTON_PAGE_PREV, BUTTON_ENTER]
        + [
            # No warning should be shown here
            BUTTON_PAGE,  # move to Generate Words, while seeing rolls
            BUTTON_ENTER,  # generate words
            BUTTON_ENTER,  # 1 press to confirm SHA
        ]
    )

    ctx = create_ctx(mocker, BTN_SEQUENCE, touch_seq=GOOD_ROLLS_SEQUENCE)
    dice_entropy = DiceEntropy(ctx)
    dice_entropy.new_key()

    assert ctx.input.wait_for_button.call_count == len(BTN_SEQUENCE)

    # Assert ctx.display.draw_centered_text was not called with poor entropy warning"
    call_message = mocker.call("Poor entropy detected. More rolls are recommended")
    for args in ctx.display.draw_hcentered_text.call_args_list:
        assert args != call_message


# Test stats for nerds
def test_stats_for_nerds(amigo, mocker):
    from krux.pages.new_mnemonic.dice_rolls import DiceEntropy, D6_12W_MIN_ROLLS
    from krux.input import BUTTON_ENTER, BUTTON_PAGE, BUTTON_PAGE_PREV, BUTTON_TOUCH

    BTN_SEQUENCE = (
        # 1 press to proceed to 12 words
        [BUTTON_ENTER]
        +
        # 1 press to proceed msg
        [BUTTON_ENTER]
        +
        # 10 number 1 presses
        [BUTTON_TOUCH for _ in range(D6_12W_MIN_ROLLS)]
        +
        # 1 press prev and 1 press on btn Go
        [BUTTON_PAGE_PREV, BUTTON_ENTER]
        + [
            BUTTON_ENTER,  # show stats for nerds
            BUTTON_ENTER,  # generate words
            BUTTON_ENTER,  # 1 press to confirm SHA
        ]
    )

    ctx = create_ctx(mocker, BTN_SEQUENCE, touch_seq=GOOD_ROLLS_SEQUENCE)
    dice_entropy = DiceEntropy(ctx)
    mocker.spy(dice_entropy, "stats_for_nerds")
    dice_entropy.new_key()

    assert ctx.input.wait_for_button.call_count == len(BTN_SEQUENCE)

    # Assert stats for nerds was called
    dice_entropy.stats_for_nerds.assert_called_once()
