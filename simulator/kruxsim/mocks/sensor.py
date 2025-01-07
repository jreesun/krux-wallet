# The MIT License (MIT)

# Copyright (c) 2021-2023 Krux contributors

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
import sys
from unittest import mock
from pyzbar.pyzbar import decode
from cv2 import split, VideoCapture, cvtColor, COLOR_BGR2RGB, COLOR_BGR2LAB
from numpy import std
from PIL import Image
import time

THREAD_DROP_PERIOD = 0.01

sequence_executor = None


def register_sequence_executor(s):
    global sequence_executor
    sequence_executor = s


class MockStatistics:
    """
    Used to mock openMV the statistics object returned by the sensor module
    """

    def __init__(self, img):
        self.img = img  # LAB image
        # Split the LAB image into L, a, and b channels
        lab_l, lab_a, lab_b = split(img)

        # Calculate the standard deviation of each channel
        self.std_L = std(lab_l)
        self.std_a = std(lab_a)
        self.std_b = std(lab_b)

    def l_stdev(self):
        return self.std_L

    def a_stdev(self):
        return self.std_a

    def b_stdev(self):
        return self.std_b

    def median(self):
        return 10


class Mockqrcode:
    def __init__(self, data):
        self.data = data

    def payload(self):
        return self.data


capturer = None


def reset(freq=None, dual_buff=False):
    pass


def run(on):
    global capturer
    if sequence_executor:
        return

    if on:
        capturer = VideoCapture(0)
    else:
        if capturer:
            capturer.release()


def find_qrcodes(img):
    codes = []
    data = decode(img)
    if data:
        codes.append(Mockqrcode(data[0].data.decode()))
    return codes


def snapshot():
    # Temporarily yield execution to allow other threads to run
    time.sleep(THREAD_DROP_PERIOD)
    
    m = mock.MagicMock()
    m.find_qrcodes.return_value = None
    if sequence_executor:
        if sequence_executor.camera_image is not None:
            frame = sequence_executor.camera_image
            frame = cvtColor(frame, COLOR_BGR2RGB)
            img = sequence_executor.camera_image
            rgb_frame = cvtColor(img, COLOR_BGR2RGB)
            lab_frame = cvtColor(rgb_frame, COLOR_BGR2LAB)
            m.get_frame.return_value = frame
            m.find_qrcodes.return_value = find_qrcodes(img)
            m.to_bytes.return_value = frame.tobytes()
            m.get_statistics.return_value = MockStatistics(lab_frame)
            m.width.return_value = frame.shape[1]
            m.height.return_value = frame.shape[0]
            if m.find_qrcodes.return_value:
                # Clear the camera image if a QR code is found
                # Otherwise keep the camera image if it's to create entropy
                sequence_executor.camera_image = None
    else:
        _, frame = capturer.read()
        rgb_frame = cvtColor(frame, COLOR_BGR2RGB)
        lab_frame = cvtColor(rgb_frame, COLOR_BGR2LAB)
        img = Image.fromarray(rgb_frame)

        m.get_frame.return_value = rgb_frame
        m.find_qrcodes.return_value = find_qrcodes(img)
        m.to_bytes.return_value = frame.tobytes()
        m.get_statistics.return_value = MockStatistics(lab_frame)
        m.width.return_value = frame.shape[1]
        m.height.return_value = frame.shape[0]
    return m


if "sensor" not in sys.modules:
    sys.modules["sensor"] = mock.MagicMock(
        reset=reset,
        run=run,
        snapshot=snapshot,
    )
