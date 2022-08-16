# The MIT License (MIT)

# Copyright (c) 2021-2022 Krux contributors

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
import gc
import sensor
import lcd
from .qr import QRPartParser
from .wdt import wdt

OV9650_ID = 0x96
OV2640_ID = 0x2642 # Lenses, vertical flip - Bit
OV5640_ID = 0x5640
OV5642_ID = 0x5642 # Lenses, horizontal flip - Bit
OV7725_ID = 0x77
OV7740_ID = 0x7742 # No lenses, no Flip - M5sitckV, Amigo
OV3660_ID = 0x3660
MT9V034_ID = 0x13
LEPTON_ID = 0x54
GC0328_ID = 0x9d # Dock


class Camera:
    """Camera is a singleton interface for interacting with the device's camera"""

    def __init__(self):
        self.ID = None

    def initialize_sensor(self):
        """Initializes the camera"""
        sensor.reset()
        self.ID = sensor.get_id()
        sensor.set_pixformat(sensor.GRAYSCALE)
        sensor.set_framesize(sensor.QVGA)
        if self.ID == OV5642_ID:
            sensor.set_hmirror(1)
        if self.ID == OV2640_ID:
            sensor.set_vflip(1)
        sensor.skip_frames()

    def capture_qr_code_loop(self, callback):
        """Captures either singular or animated QRs and parses their contents until
        all parts of the message have been captured. The part data are then ordered
        and assembled into one message and returned.
        """
        self.initialize_sensor()
        sensor.run(1)

        parser = QRPartParser()

        prev_parsed_count = 0
        new_part = False
        while True:
            wdt.feed()
            stop = callback(parser.total_count(), parser.parsed_count(), new_part)
            if stop:
                break

            new_part = False

            img = sensor.snapshot()
            if self.ID in (OV2640_ID, OV5642_ID):
                img.lens_corr(1.2)
            if self.ID == OV2640_ID:
                img.rotation_corr(z_rotation=180)
            gc.collect()
            hist = img.get_histogram()
            if "histogram" not in str(type(hist)):
                continue

            lcd.display(img)

            # Convert the image to black and white by using Otsu's thresholding.
            # This is done to account for low light and glare conditions, as well as
            # for imperfections in (printed) QR codes such as spots, blotches, streaks, and
            # fading.
            img.binary([(0, hist.get_threshold().value())], invert=True)
            res = img.find_qrcodes()
            if len(res) > 0:
                data = res[0].payload()

                parser.parse(data)

                if parser.parsed_count() > prev_parsed_count:
                    prev_parsed_count = parser.parsed_count()
                    new_part = True

            if parser.is_complete():
                break

        sensor.run(0)

        if parser.is_complete():
            return (parser.result(), parser.format)
        return (None, None)