import pytest
from unittest import mock
from unittest.mock import MagicMock
import pyqrcode
import zlib


class MockFile:
    """Custom mock file class that supports read, write, seek, and other file methods"""

    def __init__(self, data=b""):
        self.data = data if isinstance(data, bytes) else data.encode()
        self.previous_data = []
        self.position = 0
        self.write_data = bytearray()
        self.mode = "rb"
        self.file = MagicMock()
        self.file.read.side_effect = self.read
        self.file.write.side_effect = self.write
        self.file.seek.side_effect = self.seek

    def set_mode(self, mode):
        self.mode = mode
        if self.write_data:
            self.previous_data.append(self.write_data)
        if "b" not in mode:
            self.write_data = ""
        else:
            self.write_data = bytearray()

    def seek(self, pos):
        self.position = pos

    def read(self, size=None):
        if size is None:
            size = len(self.data) - self.position
        result = self.data[self.position : self.position + size]
        self.position += size
        if "b" not in self.mode:
            return result.decode()
        return result

    def write(self, content):
        if "b" not in self.mode:
            if isinstance(content, str):
                self.write_data += content
            else:
                raise TypeError("write() argument must be str")
        else:
            if isinstance(content, bytearray) or isinstance(content, bytes):
                self.write_data.extend(content)
            else:
                raise TypeError("A bytes-like object is required, not 'str'")
        return len(content)

    def __enter__(self):
        self.position = 0
        return self.file

    def __exit__(self, *args):
        pass


def mock_open(mock_file):
    def _open(file, mode="r", *args, **kwargs):
        mock_file.set_mode(mode)
        return mock_file

    return _open


class DeflateIO:
    def __init__(self, stream) -> None:
        self.stream = stream
        self.data = stream.read()

    def read(self):
        return zlib.decompress(self.data, wbits=-10)

    def write(self, input_data):
        compressor = zlib.compressobj(wbits=-10)
        compressed_data = compressor.compress(input_data)
        compressed_data += compressor.flush()
        self.stream.seek(0)  # Ensure we overwrite the stream from the beginning
        self.stream.write(compressed_data)
        self.stream.truncate()  # Remove any remaining part of the old data

    def __enter__(self):
        # Return the instance itself when entering the context
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Handle cleanup here if necessary
        pass


def encode_to_string(data):
    try:
        code_str = pyqrcode.create(data, error="L", mode="binary").text()
    except:
        # pre-decode if binary (SeedQR)
        data = data.decode("latin-1")
        code_str = pyqrcode.create(data, error="L", mode="binary").text()
    size = 0
    while code_str[size] != "\n":
        size += 1
    i = 0
    padding = 0
    while code_str[i] != "1":
        if code_str[i] == "\n":
            padding += 1
        i += 1
    code_str = code_str[(padding) * (size + 1) : -(padding) * (size + 1)]
    size -= 2 * padding

    new_code_str = ""
    for i in range(size):
        for j in range(size + 2 * padding + 1):
            if padding <= j < size + padding:
                index = i * (size + 2 * padding + 1) + j
                new_code_str += code_str[index]
        new_code_str += "\n"

    return new_code_str


def encode(data):
    # Uses string encoded qr as it already cleaned up the frames
    # PyQRcode also doesn't offer any binary output

    frame_less_qr = encode_to_string(data)
    size = 0
    while frame_less_qr[size] != "\n":
        size += 1
    binary_qr = bytearray(b"\x00" * ((size * size + 7) // 8))
    for y in range(size):
        for x in range(size):
            bit_index = y * size + x
            bit_string_index = y * (size + 1) + x
            if frame_less_qr[bit_string_index] == "1":
                binary_qr[bit_index >> 3] |= 1 << (bit_index % 8)
    return binary_qr


def get_mock_open(files: dict[str, str]):
    def open_mock(filename, *args, **kwargs):
        for expected_filename, content in files.items():
            if filename == expected_filename:
                if content == "Exception":
                    raise Exception()
                return mock.mock_open(read_data=content).return_value
        raise OSError("(mock) Unable to open {filename}")

    return mock.MagicMock(side_effect=open_mock)


def statvfs(_):
    return (8192, 8192, 1896512, 1338303, 1338303, 0, 0, 0, 0, 255)


class TimeMocker:
    def __init__(self, increment) -> None:
        self.increment = increment
        self.time = 0

    def tick(self):
        self.time += self.increment
        return self.time


class MockPrinter:
    def __init__(self):
        pass

    def qr_data_width(self):
        return 33

    def clear(self):
        pass

    def print_qr_code(self, qr_code):
        pass

    def print_string(self, string):
        pass

    def set_bitmap_mode(self, x_size, y_size, mode):
        pass

    def print_bitmap_line(self, line):
        pass

    def feed(self, amount):
        pass


class MockQRPartParser:
    TOTAL = 10
    FORMAT = 0

    def __init__(self):
        self.count = 0
        self.parts = []
        self.format = MockQRPartParser.FORMAT

    def total_count(self):
        return MockQRPartParser.TOTAL

    def parsed_count(self):
        return len(self.parts)

    def processed_parts_count(self):
        return self.parsed_count()

    def parse(self, part):
        if part not in self.parts:
            self.parts.append(part)

    def is_complete(self):
        return len(self.parts) == self.total_count()

    def result(self):
        return "".join(self.parts)


class Mockhistogram_threshold:
    def value(self):
        return 1


class Mockhistogram:
    def get_threshold(self):
        return Mockhistogram_threshold()


class Mockqrcode:
    def __init__(self, data):
        self.data = data

    def payload(self):
        return self.data


class MockBlob:
    def rect(self):
        return (10, 10, 125, 100)


class MockStats:
    """Mock the luminosity of dots of a TinySeed on which the words
    abandon...(x11) + about mnemonic is punched"""

    def __init__(self) -> None:
        self.counter = 0
        self.word_counter = 1

    def median(self):
        PUNCHED = 0x50
        NON_PUNCHED = 0xA0

        self.counter += 1
        if self.word_counter == 12 and self.counter == 10:
            return PUNCHED
        if self.counter == 12:
            self.counter = 0
            self.word_counter += 1
            if self.word_counter > 12:
                self.word_counter = 0
                return NON_PUNCHED
            return PUNCHED
        return NON_PUNCHED

    def l_stdev(self):
        return 0

    def a_stdev(self):
        return 0

    def b_stdev(self):
        return 0


SNAP_SUCCESS = 0
SNAP_ANIMATED_QR = 1
SNAP_FIND_ANIMATED_SKIPPING = 2
SNAP_REPEAT_QRCODE = 3
DONT_FIND_ANYTHING = 4

IMAGE_TO_HASH = b"\x12" * 1024  # Dummy bytes


def snapshot_generator(outcome=SNAP_SUCCESS, animated_qr=[]):
    count = 0
    qr_frames = animated_qr

    def snapshot():
        nonlocal count
        count += 1
        m = mock.MagicMock()
        if outcome == SNAP_ANIMATED_QR:
            m.find_qrcodes.return_value = [Mockqrcode(qr_frames[count - 1])]
        elif outcome == SNAP_FIND_ANIMATED_SKIPPING:
            # Skips every other frame
            if count % 2 == 0:
                m.find_qrcodes.return_value = []
            else:
                m.find_qrcodes.return_value = [Mockqrcode(qr_frames[(count - 1) // 2])]
        elif outcome == SNAP_REPEAT_QRCODE:
            # Send every frame two times
            m.find_qrcodes.return_value = [Mockqrcode(qr_frames[count // 2])]
        elif outcome == DONT_FIND_ANYTHING:
            m.find_qrcodes.return_value = []
        else:
            m.find_qrcodes.return_value = [Mockqrcode(str(count))]
            m.to_bytes.return_value = IMAGE_TO_HASH
            m.find_blobs.return_value = [MockBlob()]
            m.width.return_value = 320
            m.height.return_value = 240
            m.get_statistics.return_value = MockStats()
        return m

    return snapshot


def board_m5stickv():
    return mock.MagicMock(
        config={
            "type": "m5stickv",
            "lcd": {"height": 135, "width": 240, "invert": 0, "dir": 40, "lcd_type": 3},
            "sdcard": {"sclk": 30, "mosi": 33, "miso": 31, "cs": 32},
            "board_info": {
                "ISP_RX": 4,
                "ISP_TX": 5,
                "WIFI_TX": 39,
                "WIFI_RX": 38,
                "CONNEXT_A": 35,
                "CONNEXT_B": 34,
                "MPU_SDA": 29,
                "MPU_SCL": 28,
                "MPU_INT": 23,
                "SPK_LRCLK": 14,
                "SPK_BCLK": 15,
                "SPK_DIN": 17,
                "SPK_SD": 25,
                "MIC_LRCLK": 10,
                "MIC_DAT": 12,
                "MIC_CLK": 13,
                "LED_W": 7,
                "LED_R": 6,
                "LED_G": 9,
                "LED_B": 8,
                "BUTTON_A": 36,
                "BUTTON_B": 37,
            },
            "krux": {
                "pins": {
                    "BUTTON_A": 36,
                    "BUTTON_B": 37,
                    "LED_W": 7,
                    "UART2_TX": 35,
                    "UART2_RX": 34,
                    "I2C_SCL": 28,
                    "I2C_SDA": 29,
                },
                "display": {
                    "touch": False,
                    "font": [8, 14],
                    "font_wide": [14, 14],
                },
            },
        }
    )


def board_amigo():
    return mock.MagicMock(
        config={
            "type": "amigo",
            "lcd": {"height": 320, "width": 480, "invert": 0, "dir": 40, "lcd_type": 1},
            "sdcard": {"sclk": 11, "mosi": 10, "miso": 6, "cs": 26},
            "board_info": {
                "BOOT_KEY": 23,
                "LED_R": 14,
                "LED_G": 15,
                "LED_B": 17,
                "LED_W": 32,
                "BACK": 23,
                "ENTER": 16,
                "NEXT": 20,
                "WIFI_TX": 6,
                "WIFI_RX": 7,
                "WIFI_EN": 8,
                "I2S0_MCLK": 13,
                "I2S0_SCLK": 21,
                "I2S0_WS": 18,
                "I2S0_IN_D0": 35,
                "I2S0_OUT_D2": 34,
                "I2C_SDA": 27,
                "I2C_SCL": 24,
                "SPI_SCLK": 11,
                "SPI_MOSI": 10,
                "SPI_MISO": 6,
                "SPI_CS": 12,
            },
            "krux": {
                "pins": {
                    "BUTTON_A": 16,
                    "BUTTON_B": 20,
                    "BUTTON_C": 23,
                    "TOUCH_IRQ": 33,
                    "LED_W": 32,
                    "I2C_SDA": 27,
                    "I2C_SCL": 24,
                },
                "display": {
                    "touch": True,
                    "font": [12, 24],
                    "font_wide": [24, 24],
                },
            },
        }
    )


def board_dock():
    return mock.MagicMock(
        config={
            "type": "dock",
            "lcd": {"height": 240, "width": 320, "invert": 0, "lcd_type": 0},
            "sdcard": {"sclk": 27, "mosi": 28, "miso": 26, "cs": 29},
            "board_info": {
                "BOOT_KEY": 16,
                "LED_R": 13,
                "LED_G": 12,
                "LED_B": 14,
                "MIC0_WS": 19,
                "MIC0_DATA": 20,
                "MIC0_BCK": 18,
            },
            "krux": {
                "pins": {"BUTTON_A": 9, "ENCODER": [10, 11]},
                "display": {
                    "touch": False,
                    "font": [8, 16],
                    "font_wide": [16, 16],
                },
            },
        }
    )


def board_cube():
    return mock.MagicMock(
        config={
            "type": "cube",
            "lcd": {"height": 240, "width": 240, "invert": 1, "lcd_type": 0},
            "sdcard": {"sclk": 27, "mosi": 28, "miso": 26, "cs": 29},
            "board_info": {
                "BOOT_KEY": 16,
                "LED_R": 13,
                "LED_G": 12,
                "LED_B": 14,
                "MIC0_WS": 19,
                "MIC0_DATA": 20,
                "MIC0_BCK": 18,
            },
            "krux": {
                "pins": {
                    "BUTTON_A": 10,
                    "BUTTON_B": 16,
                    "BUTTON_C": 11,
                    "I2C_SDA": 27,
                    "I2C_SCL": 24,
                    "BACKLIGHT": 17,
                },
                "display": {
                    "touch": False,
                    "font": [8, 14],
                    "font_wide": [14, 14],
                },
            },
        }
    )


def board_wonder_mv():
    return mock.MagicMock(
        config={
            "type": "wonder_mv",
            "lcd": {
                "dcx": 8,
                "ss": 6,
                "rst": 21,
                "clk": 7,
                "height": 240,
                "width": 320,
                "invert": 1,
                "dir": 96,
                "lcd_type": 0,
            },
            "sensor": {
                "pin_sda": 9,
                "cmos_href": 17,
                "cmos_pclk": 15,
                "cmos_xclk": 14,
                "cmos_pwdn": 13,
                "cmos_vsync": 12,
                "reg_width": 16,
                "i2c_num": 2,
                "pin_clk": 10,
                "cmos_rst": 11,
            },
            "sdcard": {
                "sclk": 29,
                "mosi": 30,
                "miso": 31,
                "cs": 32,
            },
            "board_info": {
                "BOOT_KEY": 16,
                "CONNEXT_A": 28,
                "CONNEXT_B": 27,
                "I2C_SDA": 19,
                "I2C_SCL": 18,
                "SPI_SCLK": 29,
                "SPI_MOSI": 30,
                "SPI_MISO": 31,
                "SPI_CS": 32,
            },
            "krux": {
                "pins": {
                    "BUTTON_A": 26,
                    "BUTTON_B": 47,
                    "LED_W": 25,
                    "TOUCH_IRQ": 41,
                    "I2C_SDA": 19,
                    "I2C_SCL": 18,
                    "BACKLIGHT": 23,
                },
                "display": {"touch": True, "font": [8, 16], "font_wide": [16, 16]},
            },
        }
    )


def mock_context(mocker):
    import board

    if board.config["type"] == "m5stickv":
        return mocker.MagicMock(
            input=mocker.MagicMock(
                touch=None,
                enter_event=mocker.MagicMock(return_value=False),
                page_event=mocker.MagicMock(return_value=False),
                page_prev_event=mocker.MagicMock(return_value=False),
                touch_event=mocker.MagicMock(return_value=False),
            ),
            display=mocker.MagicMock(
                font_width=8,
                font_height=14,
                total_lines=17,  # 240 / 14
                width=mocker.MagicMock(return_value=135),
                height=mocker.MagicMock(return_value=240),
                usable_width=mocker.MagicMock(return_value=(135 - 2 * 10)),
                to_lines=mocker.MagicMock(return_value=[""]),
                max_menu_lines=mocker.MagicMock(return_value=7),
                draw_hcentered_text=mocker.MagicMock(return_value=1),
            ),
        )
    elif board.config["type"] == "dock":
        return mocker.MagicMock(
            input=mocker.MagicMock(
                touch=None,
                enter_event=mocker.MagicMock(return_value=False),
                page_event=mocker.MagicMock(return_value=False),
                page_prev_event=mocker.MagicMock(return_value=False),
                touch_event=mocker.MagicMock(return_value=False),
            ),
            display=mocker.MagicMock(
                font_width=8,
                font_height=16,
                total_lines=20,  # 320 / 16
                width=mocker.MagicMock(return_value=240),
                height=mocker.MagicMock(return_value=320),
                usable_width=mocker.MagicMock(return_value=(240 - 2 * 10)),
                to_lines=mocker.MagicMock(return_value=[""]),
                max_menu_lines=mocker.MagicMock(return_value=9),
                draw_hcentered_text=mocker.MagicMock(return_value=1),
            ),
            light=None,
        )
    elif board.config["type"] == "amigo":
        return mocker.MagicMock(
            input=mocker.MagicMock(
                touch=mocker.MagicMock(),
                enter_event=mocker.MagicMock(return_value=False),
                page_event=mocker.MagicMock(return_value=False),
                page_prev_event=mocker.MagicMock(return_value=False),
                touch_event=mocker.MagicMock(return_value=False),
            ),
            display=mocker.MagicMock(
                font_width=12,
                font_height=24,
                total_lines=20,  # 480 / 24
                width=mocker.MagicMock(return_value=320),
                height=mocker.MagicMock(return_value=480),
                usable_width=mocker.MagicMock(return_value=(320 - 2 * 10)),
                to_lines=mocker.MagicMock(return_value=[""]),
                max_menu_lines=mocker.MagicMock(return_value=9),
                draw_hcentered_text=mocker.MagicMock(return_value=1),
            ),
        )
    elif board.config["type"] == "cube":
        return mocker.MagicMock(
            input=mocker.MagicMock(
                touch=None,
                enter_event=mocker.MagicMock(return_value=False),
                page_event=mocker.MagicMock(return_value=False),
                page_prev_event=mocker.MagicMock(return_value=False),
                touch_event=mocker.MagicMock(return_value=False),
            ),
            display=mocker.MagicMock(
                font_width=8,
                font_height=14,
                total_lines=17,  # 240 / 14
                width=mocker.MagicMock(return_value=240),
                height=mocker.MagicMock(return_value=240),
                usable_width=mocker.MagicMock(return_value=(240 - 2 * 10)),
                to_lines=mocker.MagicMock(return_value=[""]),
                max_menu_lines=mocker.MagicMock(return_value=7),
                draw_hcentered_text=mocker.MagicMock(return_value=1),
            ),
            light=None,
        )
    elif board.config["type"] == "wonder_mv":
        return mocker.MagicMock(
            input=mocker.MagicMock(
                touch=mocker.MagicMock(),
                enter_event=mocker.MagicMock(return_value=False),
                page_event=mocker.MagicMock(return_value=False),
                page_prev_event=mocker.MagicMock(return_value=False),
                touch_event=mocker.MagicMock(return_value=False),
            ),
            display=mocker.MagicMock(
                font_width=8,
                font_height=16,
                total_lines=20,  # 320 / 16
                width=mocker.MagicMock(return_value=240),
                height=mocker.MagicMock(return_value=320),
                usable_width=mocker.MagicMock(return_value=(240 - 2 * 10)),
                to_lines=mocker.MagicMock(return_value=[""]),
                max_menu_lines=mocker.MagicMock(return_value=9),
                draw_hcentered_text=mocker.MagicMock(return_value=1),
            ),
        )
