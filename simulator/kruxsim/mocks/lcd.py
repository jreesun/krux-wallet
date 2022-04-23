import sys
import os
from unittest import mock
import pygame as pg
import cv2
from kruxsim import events
from kruxsim.mocks.board import BOARD_CONFIG

COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_RED = (255, 0, 0)
COLOR_BLUE = (0, 0, 255)
COLOR_DARKGREY = (237, 237, 220)
COLOR_LIGHTBLACK = (10, 10, 20)

WIDTH = BOARD_CONFIG["lcd"]["width"]
HEIGHT = BOARD_CONFIG["lcd"]["height"]

FONT = pg.font.Font(
    os.path.join("assets", "Terminess (TTF) Nerd Font Complete Mono.ttf"), 16
)

screen = None
portrait = True


def clear():
    def run():
        if screen:
            screen.fill(COLOR_BLACK)

    pg.event.post(pg.event.Event(events.LCD_CLEAR_EVENT, {"f": run}))


def init(*args, **kwargs):
    pass


def register(addr, val):
    pass


def display(img):
    def run():
        frame = img.get_frame()
        frame = cv2.resize(
            frame,
            (screen.get_width(), screen.get_height()),
            interpolation=cv2.INTER_AREA,
        )
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = frame.swapaxes(0, 1)
        pg.surfarray.blit_array(screen, frame)

    pg.event.post(pg.event.Event(events.LCD_DISPLAY_EVENT, {"f": run}))


def rotation(r):
    global screen
    global portrait

    def run():
        global screen
        global portrait
        if r == BOARD_CONFIG["krux"]["display"]["orientation"][0]:
            portrait = True
            screen = pg.Surface((HEIGHT, WIDTH))
        else:
            portrait = False
            screen = pg.Surface((WIDTH, HEIGHT))

    pg.event.post(pg.event.Event(events.LCD_ROTATION_EVENT, {"f": run}))


def width():
    return HEIGHT if portrait else WIDTH


def height():
    return WIDTH if portrait else HEIGHT


def draw_string(x, y, s, color, bgcolor=COLOR_BLACK):
    def run():
        text = FONT.render(s, True, color, bgcolor)
        screen.blit(text, (x, y))

    pg.event.post(pg.event.Event(events.LCD_DRAW_STRING_EVENT, {"f": run}))


def draw_qr_code(offset_y, code_str, max_width, dark_color, light_color):
    def run():
        starting_size = 0
        while code_str[starting_size] != "\n":
            starting_size += 1
        scale = max_width // starting_size
        qr_width = starting_size * scale
        offset_x = (max_width - qr_width) // 2
        for og_y in range(starting_size):
            for i in range(scale):
                y = og_y * scale + i
                for og_x in range(starting_size):
                    for j in range(scale):
                        x = og_x * scale + j
                        og_yx_index = og_y * (starting_size + 1) + og_x
                        screen.set_at(
                            (offset_x + x, offset_y + y),
                            COLOR_BLACK
                            if code_str[og_yx_index] == "1"
                            else COLOR_WHITE,
                        )

    pg.event.post(pg.event.Event(events.LCD_DRAW_QR_CODE_EVENT, {"f": run}))


def fill_rectangle(x, y, width, height, color):
    def run():
        pg.draw.rect(screen, color, (x, y, width, height))

    pg.event.post(pg.event.Event(events.LCD_FILL_RECTANGLE_EVENT, {"f": run}))


if "lcd" not in sys.modules:
    sys.modules["lcd"] = mock.MagicMock(
        init=init,
        register=register,
        display=display,
        clear=clear,
        rotation=rotation,
        width=width,
        height=height,
        draw_string=draw_string,
        draw_qr_code=draw_qr_code,
        fill_rectangle=fill_rectangle,
        WHITE=COLOR_WHITE,
        BLACK=COLOR_BLACK,
        LIGHTBLACK=COLOR_LIGHTBLACK,
        DARKGREY=COLOR_DARKGREY,
        RED=COLOR_RED,
    )
