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
import math
from unittest import mock
import pygame as pg
import cv2
from numpy import zeros_like
from kruxsim import events
from kruxsim.mocks.board import BOARD_CONFIG
from krux.krux_settings import Settings

COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)

WIDTH = BOARD_CONFIG["lcd"]["width"]
HEIGHT = BOARD_CONFIG["lcd"]["height"]

JAPANESE_CODEPOINT_MIN = 0x3000
JAPANESE_CODEPOINT_MAX = 0x30FF
CHINESE_CODEPOINT_MIN = 0x4E00
CHINESE_CODEPOINT_MAX = 0x9FFF
KOREAN_CODEPOINT_MIN = 0xAC00
KOREAN_CODEPOINT_MAX = 0xD7A3

screen = None
portrait = True
landscape = False


def rgb565torgb888(color):
    """convert from gggbbbbbrrrrrggg to tuple"""
    MASK5 = 0b11111
    MASK3 = 0b111

    red = (color >> 3) & MASK5
    red *= 255
    red //= 31
    green = color >> 13
    green += (color & MASK3) << 3
    green *= 255
    green //= 63
    blue = (color >> 8) & MASK5
    blue *= 255
    blue //= 31
    return (red, green, blue)


def clear(color):

    def run():
        if screen:
            screen.fill(color)

    color = rgb565torgb888(color)
    pg.event.post(pg.event.Event(events.LCD_CLEAR_EVENT, {"f": run}))


def init(*args, **kwargs):
    pass


def register(addr, val):
    pass


def zoom_out(img, factor=0.6):
    h, w = img.shape[:2]
    new_width = int(w * factor)
    new_height = int(h * factor)
    resized = cv2.resize(img, (new_width, new_height), interpolation=cv2.INTER_AREA)
    canvas = zeros_like(img)
    y, x = (h - new_height) // 2, (w - new_width) // 2
    canvas[y : y + resized.shape[0], x : x + resized.shape[1]] = resized
    return canvas


def display(img, oft=(0, 0), roi=None):

    image_width = 240
    image_height = 320

    # Swap and adjust oft axis
    if portrait:
        oft = (oft[1], oft[0])

    def run():
        try:
            frame = img.get_frame()
            # Fix aspect ration by cutting the image
            if frame.shape[1] / frame.shape[0] > image_width / image_height:
                frame = frame[
                    :,
                    int(
                        (frame.shape[1] - frame.shape[0] * image_width / image_height)
                        / 2
                    ) : int(
                        (frame.shape[1] + frame.shape[0] * image_width / image_height)
                        / 2
                    ),
                ]
            else:
                frame = frame[
                    int(
                        (frame.shape[0] - frame.shape[1] * image_height / image_width)
                        / 2
                    ) : int(
                        (frame.shape[0] + frame.shape[1] * image_height / image_width)
                        / 2
                    ),
                    :,
                ]
            frame = cv2.resize(
                frame,
                (image_width, image_height),
                interpolation=cv2.INTER_AREA,
            )
            # If roi width < 240, zoom out keeping canvas size
            # Case for M5StickV
            if roi and roi[2] < 240:
                frame = zoom_out(frame, 0.6)
            frame = frame.swapaxes(0, 1)
        except Exception as e:
            print(f"Error: {e}")
            return

        # Cut image according to region of interest
        if roi:
            x, y, w, h = roi
            frame = frame[y : y + h, x : x + w]

        # Create a surface for the frame
        frame_surface = pg.surfarray.make_surface(frame)

        # Blit this surface onto the screen at the specified offset
        screen.blit(frame_surface, oft)

    pg.event.post(pg.event.Event(events.LCD_DISPLAY_EVENT, {"f": run}))


def rotation(r):
    global screen
    global portrait
    global landscape

    def run():
        global screen
        global portrait
        global landscape
        if not screen:
            portrait = True
            screen = pg.Surface((HEIGHT, WIDTH)).convert()
        if r == 2 and BOARD_CONFIG["type"] != "cube":
            landscape = True
        else:
            landscape = False

    pg.event.post(pg.event.Event(events.LCD_ROTATION_EVENT, {"f": run}))


def width():
    return HEIGHT if portrait else WIDTH


def height():
    return WIDTH if portrait else HEIGHT


def _is_x_flipped():
    flipped_x = False
    if BOARD_CONFIG["type"] == "amigo":
        flipped_x = Settings().hardware.display.flipped_x_coordinates
    return flipped_x


def string_width_px(string):
    standard_width = BOARD_CONFIG["krux"]["display"]["font"][0]
    wide_width = BOARD_CONFIG["krux"]["display"]["font_wide"][0]
    string_width = 0

    for c in string:
        if (
            JAPANESE_CODEPOINT_MIN <= ord(c) <= JAPANESE_CODEPOINT_MAX
            or CHINESE_CODEPOINT_MIN <= ord(c) <= CHINESE_CODEPOINT_MAX
            or KOREAN_CODEPOINT_MIN <= ord(c) <= KOREAN_CODEPOINT_MAX
        ):
            string_width += wide_width
        else:
            string_width += standard_width

    return string_width


def string_has_wide_glyph(string):
    for c in string:
        if (
            JAPANESE_CODEPOINT_MIN <= ord(c) <= JAPANESE_CODEPOINT_MAX
            or CHINESE_CODEPOINT_MIN <= ord(c) <= CHINESE_CODEPOINT_MAX
            or KOREAN_CODEPOINT_MIN <= ord(c) <= KOREAN_CODEPOINT_MAX
        ):
            return True
    return False


def is_wide(c):
    return (
        JAPANESE_CODEPOINT_MIN <= ord(c) <= JAPANESE_CODEPOINT_MAX
        or CHINESE_CODEPOINT_MIN <= ord(c) <= CHINESE_CODEPOINT_MAX
        or KOREAN_CODEPOINT_MIN <= ord(c) <= KOREAN_CODEPOINT_MAX
    )


def char_width(c):
    if (
        JAPANESE_CODEPOINT_MIN <= ord(c) <= JAPANESE_CODEPOINT_MAX
        or CHINESE_CODEPOINT_MIN <= ord(c) <= CHINESE_CODEPOINT_MAX
        or KOREAN_CODEPOINT_MIN <= ord(c) <= KOREAN_CODEPOINT_MAX
    ):
        return BOARD_CONFIG["krux"]["display"]["font_wide"][0]
    else:
        return BOARD_CONFIG["krux"]["display"]["font"][0]


def draw_string(x, y, s, color, bgcolor=COLOR_BLACK):

    def run():
        from kruxsim import devices

        x_position = x
        if not string_has_wide_glyph(s):
            text, _ = devices.load_font(BOARD_CONFIG["type"])[0].render(
                s, color, bgcolor
            )
            if landscape:
                text = pg.transform.rotate(text, 90)
                screen.blit(
                    text,
                    (
                        height() - text.get_width() - y,
                        x_position,
                    ),
                )
            else:
                x_val = (
                    x_position
                    if BOARD_CONFIG["type"] != "amigo"
                    else width() - text.get_width() - x_position
                )
                screen.blit(
                    text,
                    (
                        x_val,
                        y,
                    ),
                )
        else:
            # draw wide text char by char
            total_with = string_width_px(s)
            for c in s:
                x_val = (
                    x_position
                    if BOARD_CONFIG["type"] != "amigo"
                    else width() - x_position - total_with
                )
                if is_wide(c):
                    text, _ = devices.load_font(BOARD_CONFIG["type"])[1].render(
                        c, color, bgcolor
                    )
                    if landscape:
                        text = pg.transform.rotate(text, 90)
                        screen.blit(
                            text,
                            (
                                height() - text.get_width() - y,
                                x_position,
                            ),
                        )
                    else:
                        screen.blit(
                            text,
                            (
                                x_val,
                                y,
                            ),
                        )
                else:
                    text, _ = devices.load_font(BOARD_CONFIG["type"])[0].render(
                        c, color, bgcolor
                    )
                    if landscape:
                        text = pg.transform.rotate(text, 90)
                        screen.blit(
                            text,
                            (
                                height() - text.get_width() - y,
                                x_position,
                            ),
                        )
                    else:
                        screen.blit(
                            text,
                            (
                                x_val,
                                y,
                            ),
                        )
                x_position += (
                    char_width(c) if BOARD_CONFIG["type"] != "amigo" else -char_width(c)
                )

    color = rgb565torgb888(color)
    bgcolor = rgb565torgb888(bgcolor)
    pg.event.post(pg.event.Event(events.LCD_DRAW_STRING_EVENT, {"f": run}))


def draw_qr_code(offset_y, code_str, max_width, dark_color, light_color, background):

    def run():
        starting_size = 0
        while code_str[starting_size] != "\n":
            starting_size += 1
        scale = max_width // starting_size
        qr_width = starting_size * scale
        offset = (max_width - qr_width) // 2
        for og_y in range(starting_size):
            for i in range(scale):
                y = og_y * scale + i
                for og_x in range(starting_size):
                    for j in range(scale):
                        x = og_x * scale + j
                        og_yx_index = og_y * (starting_size + 1) + og_x
                        screen.set_at(
                            (offset + x, offset + offset_y + y),
                            dark_color if code_str[og_yx_index] == "1" else light_color,
                        )

    dark_color = rgb565torgb888(dark_color)
    light_color = rgb565torgb888(light_color)
    pg.event.post(pg.event.Event(events.LCD_DRAW_QR_CODE_EVENT, {"f": run}))


def draw_qr_code_binary(
    offset_y, code_bin, max_width, dark_color, light_color, background
):

    def run():
        starting_size = int(math.sqrt(len(code_bin) * 8))
        block_size_divisor = starting_size + 2
        # adds 2 to create room for a 1 block border
        scale = max_width // block_size_divisor
        width = starting_size * scale
        border_size = (max_width - width) // 2
        opposite_border_offset = border_size + width - 1
        # Top border
        for rx in range(max_width):
            for ry in range(border_size):
                screen.set_at((rx, ry), light_color)

        # Bottom border
        for rx in range(max_width):
            for ry in range(opposite_border_offset, max_width):
                screen.set_at((rx, ry), light_color)

        # Left border
        for rx in range(border_size):
            for ry in range(border_size, opposite_border_offset):
                screen.set_at((rx, ry), light_color)

        # Right border
        for rx in range(opposite_border_offset, max_width):
            for ry in range(border_size, opposite_border_offset):
                screen.set_at((rx, ry), light_color)
        # QR code rendering
        for og_y in range(starting_size):
            for og_x in range(starting_size):
                og_yx_index = og_y * starting_size + og_x
                color_byte = code_bin[og_yx_index >> 3]
                color_byte &= 1 << (og_yx_index % 8)
                color = dark_color if color_byte else light_color
                for i in range(scale):
                    y = border_size + og_y * scale + i
                    for j in range(scale):
                        x = border_size + og_x * scale + j
                        screen.set_at((x, y), color)

    dark_color = rgb565torgb888(dark_color)
    light_color = rgb565torgb888(light_color)
    pg.event.post(pg.event.Event(events.LCD_DRAW_QR_CODE_EVENT, {"f": run}))


def fill_rectangle(x, y, w, h, color, radius=0):

    def run():
        if radius == 0:
            pg.draw.rect(screen, color, (x, y, w, h))
        else:
            # Draw the center rectangle
            pg.draw.rect(screen, color, (x + radius, y, w - 2 * radius, h))

            # Draw the two side rectangles
            pg.draw.rect(screen, color, (x, y + radius, radius, h - 2 * radius))
            pg.draw.rect(
                screen, color, (x + w - radius, y + radius, radius, h - 2 * radius)
            )

            # Draw the four corner circles
            pg.draw.circle(screen, color, (x + radius, y + radius), radius)
            pg.draw.circle(screen, color, (x + w - radius, y + radius), radius)
            pg.draw.circle(screen, color, (x + radius, y + h - radius), radius)
            pg.draw.circle(screen, color, (x + w - radius, y + h - radius), radius)

    color = rgb565torgb888(color)
    if _is_x_flipped():
        x = width() - w - x
    radius = min(radius, min(w, h) // 2)
    pg.event.post(pg.event.Event(events.LCD_FILL_RECTANGLE_EVENT, {"f": run}))


def draw_circle(x, y, radious, quadrant, color):
    def run():
        if quadrant == 0:
            pg.draw.circle(screen, color, (x, y), radious)

    color = rgb565torgb888(color)
    if _is_x_flipped():
        x = width() - x - 1
    pg.event.post(pg.event.Event(events.LCD_DRAW_CIRCLE_EVENT, {"f": run}))


def draw_line(x_0, y_0, x_1, y_1, color):

    def run():
        start_pos = (x_0, y_0)
        end_pos = (x_1, y_1)

        # Apply inverted coordinates if necessary
        if _is_x_flipped():
            start_pos = (width() - x_1 - 1, y_0)
            end_pos = (width() - x_0 - 1, y_1)

        pg.draw.line(screen, color, start_pos, end_pos, 1)

    color = rgb565torgb888(color)
    pg.event.post(pg.event.Event(events.LCD_DRAW_LINE_EVENT, {"f": run}))


def draw_outline(x, y, w, h, color):
    x += 1  # Adjust for compatibility with previous implementation

    def run():

        pg.draw.rect(
            screen,
            color,
            (
                (width() - w - x - 1 if _is_x_flipped() else x),
                y,
                w + 1,
                h + 1,
            ),
            1,
        )

    x -= 1  # Adjust for compatibility with previous implementation
    color = rgb565torgb888(color)
    pg.event.post(pg.event.Event(events.LCD_DRAW_OUTLINE_EVENT, {"f": run}))


if "lcd" not in sys.modules:
    sys.modules["lcd"] = mock.MagicMock(
        init=init,
        register=register,
        display=display,
        clear=clear,
        rotation=rotation,
        width=width,
        height=height,
        string_width_px=string_width_px,
        draw_string=draw_string,
        draw_qr_code=draw_qr_code,
        draw_qr_code_binary=draw_qr_code_binary,
        fill_rectangle=fill_rectangle,
        draw_circle=draw_circle,
        draw_line=draw_line,
        draw_outline=draw_outline,
        BLACK=COLOR_BLACK,
        WHITE=COLOR_WHITE,
    )
