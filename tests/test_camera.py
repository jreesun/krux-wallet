import pytest


def test_init(mocker, m5stickv):
    from krux.camera import Camera

    c = Camera()
    c.initialize_sensor()

    assert isinstance(c, Camera)


def test_initialize_sensors(mocker, multiple_devices):
    import board
    import krux
    from krux.camera import Camera, OV7740_ID, OV2640_ID, GC0328_ID, GC2145_ID

    SENSORS_LIST = [
        (OV7740_ID, "config_ov_7740"),
        (OV2640_ID, "config_ov_2640"),
        (GC0328_ID, None),
        (GC2145_ID, "config_gc_2145"),
    ]

    for sensor_id, config_method in SENSORS_LIST:
        mocker.patch("krux.camera.sensor.get_id", lambda: sensor_id)
        c = Camera()
        if config_method:
            mocker.spy(c, config_method)
        c.initialize_sensor()
        if config_method:
            getattr(c, config_method).assert_called()

        if board.config["type"] == "cube" or c.cam_id == OV2640_ID:
            krux.camera.sensor.set_vflip.assert_called_with(1)
        else:
            krux.camera.sensor.set_vflip.assert_not_called()
        krux.camera.sensor.set_vflip.reset_mock()

        if board.config["type"] == "cube":
            krux.camera.sensor.set_hmirror.assert_called_with(1)
        else:
            krux.camera.sensor.set_hmirror.assert_not_called()

    krux.camera.sensor.reset.assert_called()
    krux.camera.sensor.set_pixformat.assert_called()
    assert (
        krux.camera.sensor.set_pixformat.call_args.args[0]._extract_mock_name()
        == "mock.RGB565"
    )
    krux.camera.sensor.set_framesize.assert_called()
    assert (
        krux.camera.sensor.set_framesize.call_args.args[0]._extract_mock_name()
        == "mock.QVGA"
    )


def test_fail_to_initialize_sensor(mocker, m5stickv):
    from krux.camera import Camera

    # Mock sensor.reset to raise an exception
    mocker.patch("sensor.reset", side_effect=Exception)
    c = Camera()
    with pytest.raises(Exception):
        c.initialize_sensor()
    assert c.mode == None


def test_initialize_run_no_sensor(mocker, m5stickv):
    from krux.camera import Camera

    mocker.patch("sensor.reset", side_effect=Exception)
    c = Camera()
    try:
        # Fails to initialize at boot
        c.initialize_sensor()
    except:
        pass
    with pytest.raises(ValueError, match="No camera found"):
        c.initialize_run()
    assert c.mode == None


def test_initialize_run(mocker, m5stickv):
    from krux.camera import Camera, QR_SCAN_MODE

    c = Camera()
    c.initialize_run()
    assert c.mode == QR_SCAN_MODE
    assert c.cam_id is not None


def test_initialize_run_from_binary_grid_mode(mocker, m5stickv):  # GrayScale mode
    from krux.camera import Camera, BINARY_GRID_MODE

    c = Camera()
    c.initialize_run(mode=BINARY_GRID_MODE)
    assert c.mode == BINARY_GRID_MODE
    assert c.cam_id is not None


def test_initialize_run_with_anti_glair_enabled(mocker, m5stickv):
    from krux.camera import Camera, ANTI_GLARE_MODE

    c = Camera()
    c.initialize_sensor(mode=ANTI_GLARE_MODE)
    assert c.mode == ANTI_GLARE_MODE
    assert c.cam_id is not None


def test_toggle_antiglare(mocker, m5stickv):
    import krux
    from krux.camera import (
        Camera,
        OV7740_ID,
        OV2640_ID,
        GC0328_ID,
        GC2145_ID,
        QR_SCAN_MODE,
        ANTI_GLARE_MODE,
        ZOOMED_MODE,
    )

    SENSORS_LIST = [OV7740_ID, OV2640_ID, GC0328_ID, GC2145_ID]

    for sensor_id in SENSORS_LIST:
        mocker.patch("krux.camera.sensor.get_id", lambda: sensor_id)
        c = Camera()
        mocker.spy(c, "has_antiglare")
        c.initialize_sensor()
        if c.has_antiglare():
            assert c.mode == QR_SCAN_MODE
            c.toggle_camera_mode()
            assert c.mode == ANTI_GLARE_MODE
            c.toggle_camera_mode()
            assert c.mode == ZOOMED_MODE
            c.toggle_camera_mode()
            assert c.mode == QR_SCAN_MODE
