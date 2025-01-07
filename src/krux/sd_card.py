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
import os
from machine import SDCard
from .settings import SD_PATH

SIGNED_FILE_SUFFIX = "-signed"
PSBT_FILE_EXTENSION = ".psbt"
B64_FILE_EXTENSION = ".txt"
DESCRIPTOR_FILE_EXTENSION = ".txt"
JSON_FILE_EXTENSION = ".json"
SIGNATURE_FILE_EXTENSION = ".sig"
PUBKEY_FILE_EXTENSION = ".pub"
BMP_IMAGE_EXTENSION = ".bmp"
PBM_IMAGE_EXTENSION = ".pbm"
MPY_FILE_EXTENSION = ".mpy"


class SDHandler:
    """A simple handler to work with files on SDCard"""

    PATH_STR = "/" + SD_PATH + "/%s"

    def __init__(self):
        pass

    def __enter__(self):
        # try to remount the SDCard, can take up to 500ms
        SDCard.remount()

        # this will raise an exception if not found (SD not mount)
        os.listdir(SDHandler.PATH_STR % ".")

        # if the code reaches here, no exception was raised
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def write_binary(self, filename, data):
        """Writes the data in binary format into the filename, truncating the file first"""
        with open(SDHandler.PATH_STR % filename, "wb") as file:
            file.write(data)

    def write(self, filename, data):
        """Writes the data into the filename, truncating the file first"""
        with open(SDHandler.PATH_STR % filename, "w") as file:
            file.write(data)

    def read_binary(self, filename):
        """Reads the filename in binary format and returns the data"""
        with open(SDHandler.PATH_STR % filename, "rb") as file:
            return file.read()

    def read(self, filename):
        """Reads the filename and returns the data"""
        with open(SDHandler.PATH_STR % filename, "r") as file:
            return file.read()

    def delete(self, filename):
        """Deletes the filename"""
        os.remove(SDHandler.PATH_STR % filename)

    @staticmethod
    def dir_exists(filename):
        """Checks if the file exists and is a directory"""
        try:
            return (os.stat(filename)[0] & 0x4000) != 0
        except OSError:
            return False

    @staticmethod
    def file_exists(filename):
        """Checks if the file exists and is a file"""
        try:
            return (os.stat(filename)[0] & 0x4000) == 0
        except OSError:
            return False
