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
import pyqrcode
import re


def encode(data):
    # Uses string encoded qr as it already cleaned up the frames
    # PyQRcode also doesn't offer any binary output

    def is_qr_alphanumeric(string):
        return bool(re.match("^[A-Z0-9 $%*+\-./:]+$", string))

    mode = "binary"
    if isinstance(data, str):
        if data.isnumeric():
            mode = "numeric"
        elif is_qr_alphanumeric(data):
            mode = "alphanumeric"

    try:
        code_str = pyqrcode.create(data, error="L", mode=mode).text(quiet_zone=0)
    except:
        # pre-decode if binary (SeedQR)
        data = data.decode("latin-1")
        code_str = pyqrcode.create(data, error="L", mode="binary").text(quiet_zone=0)
    size = 0
    while code_str[size] != "\n":
        size += 1
    binary_qr = bytearray(b"\x00" * ((size * size + 7) // 8))
    for y in range(size):
        for x in range(size):
            bit_index = y * size + x
            bit_string_index = y * (size + 1) + x
            if code_str[bit_string_index] == "1":
                binary_qr[bit_index >> 3] |= 1 << (bit_index % 8)
    return binary_qr


if "qrcode" not in sys.modules:
    sys.modules["qrcode"] = mock.MagicMock(
        encode=encode,
    )
