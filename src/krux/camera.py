# The MIT License (MIT)

# Copyright (c) 2021-2024 Krux contributors

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
# pylint: disable=W0212

import gc
import sensor
import board
from .krux_settings import Settings

OV2640_ID = 0x2642  # Lenses, vertical flip - Bit
OV5642_ID = 0x5642  # Lenses, horizontal flip - Bit
OV7740_ID = 0x7742  # No lenses, no Flip - M5sitckV, Amigo
GC0328_ID = 0x9D  # Dock
GC2145_ID = 0x45  # Yahboom

QR_SCAN_MODE = 0
ANTI_GLARE_MODE = 1
ENTROPY_MODE = 2
BINARY_GRID_MODE = 3
ZOOMED_MODE = 4

OV2640Z_OFFSET_X = 160
OV2640Z_OFFSET_Y = 120
OV2640Z_MAX_X = 400 // 4
OV2640Z_MAX_Y = 360 // 4
OV2640Z_WIDTH = OV2640Z_MAX_X - OV2640Z_OFFSET_X // 4
OV2640Z_HEIGHT = OV2640Z_MAX_Y - OV2640Z_OFFSET_Y // 4

# Luminosity threshold values for each camera and mode
LUM_TH = {
    # flat dictionary using composite keys (camera_id, mode)
    (OV2640_ID, QR_SCAN_MODE): (0x60, 0x70),
    (OV2640_ID, ANTI_GLARE_MODE): (0x20, 0x28),
    (OV2640_ID, ENTROPY_MODE): (0x68, 0x78),
    (OV2640_ID, BINARY_GRID_MODE): (0x44, 0x48),
    (OV2640_ID, ZOOMED_MODE): (0x35, 0x50),
    (OV7740_ID, QR_SCAN_MODE): (0x60, 0x70),
    (OV7740_ID, ANTI_GLARE_MODE): (0x20, 0x28),
    (OV7740_ID, ENTROPY_MODE): (0x68, 0x78),
    (OV7740_ID, BINARY_GRID_MODE): (0x44, 0x48),
    (OV7740_ID, ZOOMED_MODE): (0x35, 0x50),
    (GC2145_ID, QR_SCAN_MODE): (0x30, 0x55),
    (GC2145_ID, ANTI_GLARE_MODE): (0x25, 0x40),
    (GC2145_ID, ENTROPY_MODE): (0x20, 0xF2),
    (GC2145_ID, BINARY_GRID_MODE): (0x30, 0x50),
    (GC2145_ID, ZOOMED_MODE): (0x27, 0x45),
    (GC0328_ID, QR_SCAN_MODE): 0x70,
    (GC0328_ID, ANTI_GLARE_MODE): 0x40,
    (GC0328_ID, ENTROPY_MODE): 0x80,
    (GC0328_ID, BINARY_GRID_MODE): 0x70,
    (GC0328_ID, ZOOMED_MODE): 0x55,
}


class Camera:
    """Camera is a singleton interface for interacting with the device's camera"""

    def __init__(self):
        self.cam_id = None
        self.mode = None
        try:
            self.initialize_sensor(mode=QR_SCAN_MODE)
            sensor.run(0)
        except Exception as e:
            print("Camera not found:", e)

    def initialize_sensor(self, mode=QR_SCAN_MODE):
        """Initializes the camera"""
        sensor.reset(freq=18200000)
        self.cam_id = sensor.get_id()
        if board.config["type"] == "cube" or (
            board.config["type"] in ["yahboom", "wonder_mv"]
            and hasattr(Settings().hardware, "display")
            and getattr(Settings().hardware.display, "flipped_orientation", False)
        ):
            # Rotate camera 180 degrees on Cube
            sensor.set_hmirror(1)
            sensor.set_vflip(1)
        self.mode = mode
        if mode == BINARY_GRID_MODE and self.cam_id != GC2145_ID:
            # Binary grid mode uses grayscale except for GC2145
            sensor.set_pixformat(sensor.GRAYSCALE)
        else:
            sensor.set_pixformat(sensor.RGB565)
        if self.cam_id == OV5642_ID:
            sensor.set_hmirror(1)
        if self.cam_id == OV2640_ID:
            sensor.set_vflip(1)
        if board.config["type"] == "bit":
            # CIF mode will use central pixels and discard darker periphery
            sensor.set_framesize(sensor.CIF)
        else:
            sensor.set_framesize(sensor.QVGA)
        if mode != ENTROPY_MODE:
            if self.cam_id == OV7740_ID:
                self.config_ov_7740()
            if self.cam_id == OV2640_ID:
                self.config_ov_2640()
            if self.cam_id == GC2145_ID:
                self.config_gc_2145()
            self.luminosity_threshold()

    def config_ov_7740(self):
        """Specialized config for OV7740 sensor"""

        # Average-based sensing window definition
        # Ingnore periphery and measure luminance only on central area
        # Regions 1,2,3,4
        sensor.__write_reg(0x56, 0x0)
        # Regions 5,6,7,8
        sensor.__write_reg(0x57, 0b00111100)
        # Regions 9,10,11,12
        sensor.__write_reg(0x58, 0b00111100)
        # Regions 13,14,15,16
        sensor.__write_reg(0x59, 0x0)

    def config_ov_2640(self):
        """Specialized config for OV2640 sensor"""
        # Set register bank 0
        sensor.__write_reg(0xFF, 0x00)
        # Enable AEC
        sensor.__write_reg(0xC2, 0x8C)
        # Set register bank 1
        sensor.__write_reg(0xFF, 0x01)

        # Average-based sensing window definition
        # Ingnore periphery and measure luminance only on central area
        # Regions 1,2,3,4
        sensor.__write_reg(0x5D, 0xFF)
        # Regions 5,6,7,8
        sensor.__write_reg(0x5E, 0b11000011)
        # Regions 9,10,11,12
        sensor.__write_reg(0x5F, 0b11000011)
        # Regions 13,14,15,16
        sensor.__write_reg(0x60, 0xFF)

    def config_gc_2145(self):
        """Specialized config for GC2145 sensor"""
        # Set register bank 1
        sensor.__write_reg(0xFE, 0x01)
        # Center weight mode = 7, default=0x01 (center mode = 0)
        sensor.__write_reg(0x0C, 0x71)

    def has_antiglare(self):
        """Returns whether the camera has anti-glare functionality"""
        return self.cam_id in (OV7740_ID, OV2640_ID, GC2145_ID, GC0328_ID)

    def luminosity_threshold(self):
        """Configures the luminosity thresholds for the camera"""
        config_map = {
            GC0328_ID: self._config_gc0328_lum,
            OV2640_ID: self._config_ovxx40_lum,
            OV7740_ID: self._config_ovxx40_lum,  # Same as OV2640
            GC2145_ID: self._config_gc2145_lum,
        }

        config_func = config_map.get(self.cam_id)
        if config_func:
            config_func()
        sensor.skip_frames()

    def _config_gc0328_lum(self):
        key = (self.cam_id, self.mode)
        target = LUM_TH.get(key, 0x80)  # Default value if key not found
        # Set register bank 1
        sensor.__write_reg(0xFE, 0x01)
        # Expected luminance level, default=0x50
        sensor.__write_reg(0x13, target)

    def _config_ovxx40_lum(self):
        key = (self.cam_id, self.mode)
        thresholds = LUM_TH.get(key, (0, 0))  # Default to (0, 0) if key not found
        low, high = thresholds

        if low < 0x10 or high > 0xF0:
            return

        # luminance high level, default=0x78
        sensor.__write_reg(0x24, high)
        # luminance low level, default=0x68
        sensor.__write_reg(0x25, low)
        vpt_low = (low - 0x10) >> 4
        vpt_high = (high + 0x10) >> 4
        vpt = (vpt_high << 4) | vpt_low
        # VPT - fast convergence zone, default=0xD4
        sensor.__write_reg(0x26, vpt)
        if self.mode in (QR_SCAN_MODE, ANTI_GLARE_MODE):
            # Disable frame integration (bad for animated QR codes)
            sensor.__write_reg(0x15, 0x00)

    def _config_gc2145_lum(self):
        key = (self.cam_id, self.mode)
        thresholds = LUM_TH.get(key, (0, 0))  # Default to (0, 0) if key not found
        low, high = thresholds

        if low < 0x10 or high > 0xF0:
            return

        # Set register bank 1
        sensor.__write_reg(0xFE, 0x01)
        # luminance high level, default=0xF2
        sensor.__write_reg(0x0E, high)
        # luminance low level, default=0x20
        sensor.__write_reg(0x0F, low)
        # Expected luminance level, default=0x50
        sensor.__write_reg(0x13, (low + high) // 2)

    def _gc2145_crop(self):
        sensor.run(0)
        sensor.set_framesize(sensor.VGA)
        sensor.set_windowing((0, 0, 240, 240))
        # Set register bank 0
        sensor.__write_reg(0xFE, 0x00)
        # Crop enable
        sensor.__write_reg(0x90, 0x01)
        # Crop window
        # Registers: X[10:8]=0x93, X[7:0]=0x94, Y[10:8]=0x91, Y[7:0]=0x92
        # X_HEIGHT[10:8]=0x95, X_HEIGHT[7:0]=0x96, Y_WIDTH[10:8]=0x97, Y_WIDTH[7:0]=0x98
        sensor.__write_reg(0x93, 0x01)
        sensor.__write_reg(0x94, 0x00)
        sensor.__write_reg(0x91, 0x00)
        sensor.__write_reg(0x92, 0xC0)
        # 240x240
        sensor.__write_reg(0x95, 0x00)
        sensor.__write_reg(0x96, 0xF0)
        sensor.__write_reg(0x97, 0x00)
        sensor.__write_reg(0x98, 0xF0)

        sensor.run(1)

    def _gc0328_crop(self):
        sensor.run(0)
        sensor.set_framesize(sensor.VGA)
        sensor.set_windowing((0, 0, 240, 240))
        # Setting registers to crop GC0328 are the same as GC2145 but starting from 0x50
        # Set register bank 0
        sensor.__write_reg(0xFE, 0x00)
        # Crop enable
        sensor.__write_reg(0x50, 0x01)
        # Crop window
        # Registers: X[10:8]=0x53, X[7:0]=0x54, Y[10:8]=0x51, Y[7:0]=0x52
        # X_HEIGHT[10:8]=0x55, X_HEIGHT[7:0]=0x56, Y_WIDTH[10:8]=0x57, Y_WIDTH[7:0]=0x58
        sensor.__write_reg(0x53, 0x00)
        sensor.__write_reg(0x54, 0xD0)
        sensor.__write_reg(0x51, 0x00)
        sensor.__write_reg(0x52, 0x90)
        # 240x240
        sensor.__write_reg(0x55, 0x00)
        sensor.__write_reg(0x56, 0xF0)
        sensor.__write_reg(0x57, 0x00)
        sensor.__write_reg(0x58, 0xF0)

        sensor.run(1)

    def _ov2640_crop(self):
        sensor.run(0)
        sensor.set_framesize(sensor.VGA)
        sensor.set_windowing((0, 0, 240, 240))

        # Prepare register list
        win_regs = (
            (0xFF, 0x00),
            (0x51, OV2640Z_MAX_X & 0xFF),
            (0x52, OV2640Z_MAX_Y & 0xFF),
            (0x53, OV2640Z_OFFSET_X & 0xFF),
            (0x54, OV2640Z_OFFSET_Y & 0xFF),
            (
                0x55,
                ((OV2640Z_MAX_Y >> 1) & 0x80)  # bit 7 from (OV2640Z_MAX_Y >> 1)
                | (
                    (OV2640Z_OFFSET_Y >> 4) & 0x70
                )  # bits 6:4 from (OV2640Z_OFFSET_Y >> 4)
                | ((OV2640Z_MAX_X >> 5) & 0x08)  # bit 3 from (OV2640Z_MAX_X >> 5)
                | (
                    (OV2640Z_OFFSET_X >> 8) & 0x07
                ),  # bits 2:0 from (OV2640Z_OFFSET_X >> 8)
            ),
            (0x57, (OV2640Z_MAX_X >> 2) & 0x80),  # bit 7 from (OV2640Z_MAX_X >> 2)
            (0x5A, OV2640Z_WIDTH & 0xFF),
            (0x5B, OV2640Z_HEIGHT & 0xFF),
            (
                0x5C,
                ((OV2640Z_HEIGHT >> 6) & 0x04)  # bit 2 from (h >> 6)
                | ((OV2640Z_WIDTH >> 8) & 0x03),  # bits 1:0 from (w >> 8)
            ),
        )

        # Write each register to the sensor
        for reg, val in win_regs:
            sensor.__write_reg(reg, val)

        sensor.run(1)

    def zoom_mode(self):
        """Zooms in the camera to the center of the image"""
        if self.cam_id == GC2145_ID:
            self._gc2145_crop()
        elif self.cam_id == GC0328_ID:
            self._gc0328_crop()
        elif self.cam_id == OV7740_ID:
            sensor.__write_reg(0xD5, 0x00)
        elif self.cam_id == OV2640_ID:
            self._ov2640_crop()

    def toggle_camera_mode(self):
        """Toggles anti-glare mode and returns the new state"""
        if self.mode == ANTI_GLARE_MODE:
            # Enter zoomed mode
            self.zoom_mode()
            self.mode = ZOOMED_MODE
        elif self.mode == ZOOMED_MODE:
            # Turn off zoomed mode
            if self.cam_id in (GC0328_ID, GC2145_ID, OV2640_ID):
                sensor.run(0)
                sensor.set_framesize(sensor.QVGA)
                sensor.set_windowing((0, 0, 320, 240))
                sensor.run(1)
            elif self.cam_id == OV7740_ID:
                sensor.__write_reg(0xD5, 0x30)
            sensor.skip_frames()
            # Go back to standard mode
            self.mode = QR_SCAN_MODE
        else:
            self.mode = ANTI_GLARE_MODE
        self.luminosity_threshold()
        return self.mode

    def snapshot(self):
        """Helper to take a customized snapshot from sensor"""
        img = sensor.snapshot()
        if board.config["type"] == "bit":
            img.lens_corr(strength=1.1)
            img.rotation_corr(z_rotation=180)
        return img

    def initialize_run(self, mode=QR_SCAN_MODE):
        """Initializes and runs sensor"""
        if self.mode is None:
            raise ValueError("No camera found")
        if self.mode != mode:
            self.initialize_sensor(mode=mode)
        sensor.run(1)

    def stop_sensor(self):
        """Stops capturing from sensor"""
        gc.collect()
        sensor.run(0)
