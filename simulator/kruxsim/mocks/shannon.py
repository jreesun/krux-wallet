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

"""Mocks Micropython Shannon's entropy module"""

import sys
import math
from unittest import mock

BYTES_PER_PIXEL = 3


def entropy_img16b(img_bytes):
    """Function to calculate Shannon's entropy.
    Will return average number of bits required to encode each pixel,
    based on the probability distribution of the pixel values, ranging from 0 to 16.
    The entropy value is a theoretical lower bound on the number of bits needed to
    encode the image without loss, under an ideal compression algorithm.
    This means that in the best-case scenario, you can't compress the image to
    fewer bits per pixel than the entropy value without losing information"""

    """
    As on the simulator 24 bits are used to encode each pixel, we need to refactor the
    entropy calculation to take into account the 24 bits(3 bytes) per pixel.
    The function name will be kept the same for compatibility with the original
    """

    # Calculate frequency of each pixel value
    pixel_counts = {}
    for i in range(0, len(img_bytes), BYTES_PER_PIXEL):
        pixel_value = int.from_bytes(img_bytes[i : i + BYTES_PER_PIXEL], "little")
        if pixel_value in pixel_counts:
            pixel_counts[pixel_value] += 1
        else:
            pixel_counts[pixel_value] = 1

    # Total number of pixels (half the number of bytes)
    total_pixels = len(img_bytes) // BYTES_PER_PIXEL

    # Calculate entropy
    entropy = 0
    for count in pixel_counts.values():
        probability = count / total_pixels
        entropy -= probability * (probability and math.log2(probability))

    # To resemble real devices we do a 24 bits/pixel -> 16 bits/pixel compensation (*2/3)
    return entropy * 2 / 3


if "shannon" not in sys.modules:
    sys.modules["shannon"] = mock.MagicMock(
        entropy_img16b=entropy_img16b,
    )
