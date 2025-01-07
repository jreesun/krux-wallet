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
import pygame as pg
from krux.krux_settings import Settings, PrinterSettings

simulating_printer = False


def simulate_printer():
    global simulating_printer
    simulating_printer = True
    Settings().hardware.printer.driver = "thermal/adafruit"


def reset():
    pg.event.post(pg.event.Event(pg.QUIT))


class UART:
    UART1 = 0
    UART2 = 1
    UART3 = 2
    UART4 = 3
    UARTHS = 4

    def __init__(self, pin, baudrate):
        pass

    def read(self, num_bytes):
        if simulating_printer:
            module, cls = PrinterSettings.PRINTERS[Settings().hardware.printer.driver]
            if module == "thermal" and cls == "AdafruitPrinter":
                return chr(0b00000000)
        return None

    def readline(self):
        if simulating_printer:
            module, cls = PrinterSettings.PRINTERS[Settings().hardware.printer.driver]
            if module == "cnc" and cls == "FilePrinter":
                return "ok\n".encode()
        return None

    def write(self, data):
        pass


class SDCard:
    def remount():
        pass

def unique_id():
    return b'\xbc\x8d{%\x8e^\xc5Q\xb3N\x07f\x9f\xde\xbbG7\xddFK^\xdc\xdb\xbc\xb4E\x14A~3\x91\x12'


if "machine" not in sys.modules:
    sys.modules["machine"] = mock.MagicMock(
        reset=reset, UART=mock.MagicMock(wraps=UART), SDCard=SDCard, unique_id=unique_id
    )
