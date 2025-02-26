from ..shared_mocks import mock_context, snapshot_generator, SNAP_SUCCESS, IMAGE_TO_HASH
import hashlib

ENTROPY_MESSAGE_STR = (
    f"Shannon's entropy:\n%s bits/px\n(%s total)\n\nPixels deviation index: %s"
)

ENTROPY_INSUFFICIENT_MESSAGE_STR = "Insufficient entropy!\n\n" + ENTROPY_MESSAGE_STR


def test_cancel_capture(amigo, mocker):
    """Test that the capture method returns None when the user cancels the capture"""
    from krux.pages.capture_entropy import CameraEntropy

    # Mock snapshot to return a successful snapshot
    mocker.patch(
        "krux.camera.sensor.snapshot", new=snapshot_generator(outcome=SNAP_SUCCESS)
    )

    # Create a mock context
    ctx = mock_context(mocker)

    # Mock page_event to return True and other events to return False
    mocker.patch.object(ctx.input, "enter_event", return_value=False)
    mocker.patch.object(ctx.input, "touch_event", return_value=False)
    # run 2 times before cancel button is pressed
    mocker.patch.object(ctx.input, "page_event", side_effect=[False, False, True])
    mocker.patch.object(ctx.input, "page_prev_event", return_value=False)

    # Create an instance of CameraEntropy
    camera_entropy = CameraEntropy(ctx)

    # Mock flash_text to monitor its calls
    camera_entropy.flash_text = mocker.MagicMock()

    # Call the capture method
    result = camera_entropy.capture()

    # Assert that the result is None, indicating cancellation
    assert result is None

    # Assert ctx.flash_text was called with "Capture cancelled"
    camera_entropy.flash_text.assert_called_with("Capture cancelled")


def test_insufficient_variance(amigo, mocker):
    """Test that the capture method returns None when the variance is below the threshold"""
    from krux.pages.capture_entropy import (
        CameraEntropy,
        INSUFFICIENT_VARIANCE_TH,
        INSUFFICIENT_SHANNONS_ENTROPY_TH,
    )
    from krux.themes import RED

    # Mock snapshot to return a successful snapshot
    mocker.patch(
        "krux.camera.sensor.snapshot", new=snapshot_generator(outcome=SNAP_SUCCESS)
    )

    # Create a mock context
    ctx = mock_context(mocker)

    # Mock touch_event to return True and other events to return False
    mocker.patch.object(ctx.input, "enter_event", return_value=False)
    mocker.patch.object(ctx.input, "touch_event", return_value=True)
    mocker.patch.object(ctx.input, "page_event", return_value=False)
    mocker.patch.object(ctx.input, "page_prev_event", return_value=False)

    # Create an instance of CameraEntropy
    camera_entropy = CameraEntropy(ctx)

    # Mock rms value to return a value below the threshold
    variance = INSUFFICIENT_VARIANCE_TH - 1
    camera_entropy.rms_value = mocker.MagicMock(return_value=variance)

    # Mock shannon.entropy_img16b to return a value above the threshold
    shannon_value = INSUFFICIENT_SHANNONS_ENTROPY_TH + 1
    total_shannon = shannon_value * 320 * 240
    mocker.patch("shannon.entropy_img16b", return_value=shannon_value)

    # Call the capture method
    result = camera_entropy.capture()

    # Assert that the result is None
    assert result is None

    # Assert ctx.display.draw_centered_text was called with "Insufficient entropy!"
    call_message = mocker.call(
        ENTROPY_INSUFFICIENT_MESSAGE_STR % (shannon_value, total_shannon, variance), RED
    )

    ctx.display.draw_centered_text.assert_has_calls([call_message])


def test_insufficient_shannons_entropy(amigo, mocker):
    """Test that the capture method returns None when the Shannon's entropy is below the threshold"""
    from krux.pages.capture_entropy import (
        CameraEntropy,
        INSUFFICIENT_VARIANCE_TH,
        INSUFFICIENT_SHANNONS_ENTROPY_TH,
    )
    from krux.themes import RED

    # Mock snapshot to return a successful snapshot
    mocker.patch(
        "krux.camera.sensor.snapshot", new=snapshot_generator(outcome=SNAP_SUCCESS)
    )

    # Create a mock context
    ctx = mock_context(mocker)

    # Mock touch_event to return True and other events to return False
    mocker.patch.object(ctx.input, "enter_event", return_value=False)
    mocker.patch.object(ctx.input, "touch_event", return_value=True)
    mocker.patch.object(ctx.input, "page_event", return_value=False)
    mocker.patch.object(ctx.input, "page_prev_event", return_value=False)

    # Create an instance of CameraEntropy
    camera_entropy = CameraEntropy(ctx)

    # Create an instance of CameraEntropy
    camera_entropy = CameraEntropy(ctx)

    # Mock rms value to return a value above the threshold
    variance = INSUFFICIENT_VARIANCE_TH + 1
    camera_entropy.rms_value = mocker.MagicMock(return_value=variance)

    # Mock shannon.entropy_img16b to return a value below the threshold
    shannon_value = INSUFFICIENT_SHANNONS_ENTROPY_TH - 1
    total_shannon = shannon_value * 320 * 240
    mocker.patch("shannon.entropy_img16b", return_value=shannon_value)

    # Call the capture method
    result = camera_entropy.capture()

    # Assert that the result is None
    assert result is None

    # Assert ctx.display.draw_centered_text was called with "Insufficient entropy!"
    call_message = mocker.call(
        ENTROPY_INSUFFICIENT_MESSAGE_STR % (shannon_value, total_shannon, variance), RED
    )

    ctx.display.draw_centered_text.assert_has_calls([call_message])


def test_poor_variance(amigo, mocker):
    """
    Test that the capture method return a valid hash when the variance is below poor threshold,
    but above the insufficient threshold, and the Shannon's entropy is above the threshold
    """
    from krux.pages.capture_entropy import (
        CameraEntropy,
        POOR_VARIANCE_TH,
        INSUFFICIENT_SHANNONS_ENTROPY_TH,
    )

    # Mock snapshot to return a successful snapshot
    mocker.patch(
        "krux.camera.sensor.snapshot", new=snapshot_generator(outcome=SNAP_SUCCESS)
    )

    # Create a mock context
    ctx = mock_context(mocker)

    # Mock touch_event to return True and other events to return False
    mocker.patch.object(ctx.input, "enter_event", return_value=False)
    mocker.patch.object(ctx.input, "touch_event", return_value=True)
    mocker.patch.object(ctx.input, "page_event", return_value=False)
    mocker.patch.object(ctx.input, "page_prev_event", return_value=False)

    # Create an instance of CameraEntropy
    camera_entropy = CameraEntropy(ctx)

    # Create an instance of CameraEntropy
    camera_entropy = CameraEntropy(ctx)

    # Mock rms value to return a value below the poor threshold, but above insufficient
    variance = POOR_VARIANCE_TH - 1
    camera_entropy.rms_value = mocker.MagicMock(return_value=variance)

    # Mock shannon.entropy_img16b to return a value above the threshold
    shannon_value = INSUFFICIENT_SHANNONS_ENTROPY_TH + 1
    total_shannon = shannon_value * 320 * 240
    mocker.patch("shannon.entropy_img16b", return_value=shannon_value)

    # Call the capture method
    result = camera_entropy.capture()

    # Assert that the result has the a valid hash
    hasher = hashlib.sha256()
    hasher.update(IMAGE_TO_HASH)

    assert result == hasher.digest()

    # Assert ctx.display.draw_centered_text was called with "Insufficient entropy!"
    call_message = mocker.call(
        ENTROPY_MESSAGE_STR % (shannon_value, total_shannon, variance)
    )

    ctx.display.draw_centered_text.assert_has_calls([call_message])


def test_good_variance_good_shannons_entropy(amigo, mocker):
    """
    Test that the capture method return a valid hash when the variance and Shannon's entropy are above
    poor and insufficient thresholds
    """
    from krux.pages.capture_entropy import (
        CameraEntropy,
        POOR_VARIANCE_TH,
        INSUFFICIENT_SHANNONS_ENTROPY_TH,
    )

    # Mock snapshot to return a successful snapshot
    mocker.patch(
        "krux.camera.sensor.snapshot", new=snapshot_generator(outcome=SNAP_SUCCESS)
    )

    # Create a mock context
    ctx = mock_context(mocker)

    # Mock touch_event to return True and other events to return False
    mocker.patch.object(ctx.input, "enter_event", return_value=False)
    mocker.patch.object(ctx.input, "touch_event", return_value=True)
    mocker.patch.object(ctx.input, "page_event", return_value=False)
    mocker.patch.object(ctx.input, "page_prev_event", return_value=False)

    # Create an instance of CameraEntropy
    camera_entropy = CameraEntropy(ctx)

    # Create an instance of CameraEntropy
    camera_entropy = CameraEntropy(ctx)

    # Mock rms value to return a value below the poor threshold, but above insufficient
    variance = POOR_VARIANCE_TH + 1
    camera_entropy.rms_value = mocker.MagicMock(return_value=variance)

    # Mock shannon.entropy_img16b to return a value above the threshold
    shannon_value = INSUFFICIENT_SHANNONS_ENTROPY_TH + 1
    total_shannon = shannon_value * 320 * 240
    mocker.patch("shannon.entropy_img16b", return_value=shannon_value)

    # Call the capture method
    result = camera_entropy.capture()

    # Assert that the result has the a valid hash
    hasher = hashlib.sha256()
    hasher.update(IMAGE_TO_HASH)

    assert result == hasher.digest()

    # Assert ctx.display.draw_centered_text was called with "Insufficient entropy!"
    call_message = mocker.call(
        ENTROPY_MESSAGE_STR % (shannon_value, total_shannon, variance)
    )

    ctx.display.draw_centered_text.assert_has_calls([call_message])
