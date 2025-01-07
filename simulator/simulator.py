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
import os
import sys
import argparse
import threading
import pygame as pg
from kruxsim import devices, events

exec_folder = 'simulator'
current_dir = os.getcwd()

# check if is executing in exec_folder, if not, try to change to exec_folder
if current_dir[len(current_dir) - len(exec_folder):] not in exec_folder:
    os.chdir(exec_folder)

parser = argparse.ArgumentParser()
parser.add_argument(
    "--device",
    type=str,
    default=devices.PC,
    required=False,
)
parser.add_argument(
    "--sequence",
    type=str,
    default="",
    required=False,
)
parser.add_argument(
    "--printer",
    type=bool,
    default=False,
    required=False,
    action=argparse.BooleanOptionalAction,
)
parser.add_argument(
    "--sd",
    type=bool,
    default=False,
    required=False,
    action=argparse.BooleanOptionalAction,
)
parser.add_argument(
    "--exit-after-sequence",
    type=bool,
    default=True,
    required=False,
    action=argparse.BooleanOptionalAction,
)
parser.add_argument(
    "--screenshot-scale",
    type=bool,
    default=True,
    required=False,
    action=argparse.BooleanOptionalAction,
)

args = parser.parse_args()

pg.init()
pg.freetype.init()

from kruxsim.mocks import board

board.register_device(args.device)

if args.sd:
    from kruxsim.mocks import uopen
    from kruxsim.mocks import uos

from kruxsim.mocks import uos_functions

from kruxsim.mocks import usys
from kruxsim.mocks import utime
from kruxsim.mocks import fpioa_manager
from kruxsim.mocks import Maix
from kruxsim.mocks import flash
from kruxsim.mocks import lcd
from kruxsim.mocks import machine
from kruxsim.mocks import image
from kruxsim.mocks import pmu
from kruxsim.mocks import deflate

if args.printer:
    machine.simulate_printer()

from kruxsim.mocks import secp256k1
from kruxsim.mocks import qrcode
from kruxsim.mocks import sensor
from kruxsim.mocks import shannon
from kruxsim.mocks import ft6x36
from kruxsim.mocks import buttons
from kruxsim.mocks import rotary
from kruxsim.sequence import SequenceExecutor

sequence_executor = None
if args.sequence:
    sequence_executor = SequenceExecutor(args.sequence)

buttons.register_sequence_executor(sequence_executor)
pmu.register_sequence_executor(sequence_executor)
sensor.register_sequence_executor(sequence_executor)
ft6x36.register_sequence_executor(sequence_executor)


def run_krux():
    with open("../src/boot.py", "r", encoding='utf-8') as boot_file:
        exec(boot_file.read())


# mock for SD
if args.sd:
    # create the sd folder if not exists
    from krux.settings import SD_PATH
    if not os.path.exists(SD_PATH):
        os.makedirs(SD_PATH)
    from kruxsim.mocks import sd_card

t = threading.Thread(target=run_krux)
t.daemon = True

screen = pg.display.set_mode(devices.WINDOW_SIZES[args.device], pg.SCALED, 32)
screen.fill(lcd.COLOR_BLACK)
buffer_image = screen.copy().convert()

pg.display.set_caption("Krux Simulator")

device_image = devices.load_image(args.device)

# Scale screenshots for docs
AMIGO_SIZE = (150, 252)
M5STICKV_SIZE = (125, 247)
DOCK_SIZE = (151, 258)
YAHBOOM_SIZE = (156, 220)
CUBE_SIZE = (200, 212)
WONDER_MV_SIZE = (152, 220)

# Handle screenshots scale and alpha bg
# When exporting the mask from GIMP uncheck "Save info about transparent pixels color"
device_screenshot_size = AMIGO_SIZE
mask_img = pg.image.load(
    os.path.join("assets", "maixpy_amigo_mask.png")
    ).convert_alpha()
if (args.device == devices.M5STICKV):
    device_screenshot_size = M5STICKV_SIZE
    mask_img = pg.image.load(
        os.path.join("assets", "maixpy_m5stickv_mask.png")
        ).convert_alpha()
elif (args.device == devices.DOCK):
    device_screenshot_size = DOCK_SIZE
    mask_img = pg.image.load(
        os.path.join("assets", "maixpy_dock_mask.png")
        ).convert_alpha()
elif (args.device == devices.YAHBOOM):
    device_screenshot_size = YAHBOOM_SIZE
    mask_img = pg.image.load(
        os.path.join("assets", "maixpy_yahboom_mask.png")
        ).convert_alpha()
elif (args.device == devices.CUBE):
    device_screenshot_size = CUBE_SIZE
    mask_img = pg.image.load(
        os.path.join("assets", "maixpy_cube_mask.png")
        ).convert_alpha()
elif (args.device == devices.WONDER_MV):
    device_screenshot_size = WONDER_MV_SIZE
    mask_img = pg.image.load(
        os.path.join("assets", "maixpy_wonder_mv_mask.png")
        ).convert_alpha()
    
# Handle screenshots filename suffix when scaled
from krux.krux_settings import Settings
screenshot_suffix = ""
if args.screenshot_scale:
    screenshot_suffix = "-" + str(device_screenshot_size[0]) + "." + Settings().i18n.locale.split("-")[0]


if args.device == devices.PC:
    from kruxsim.mocks.board import BOARD_CONFIG
    BOARD_CONFIG["type"] = "amigo"

t.start()


def shutdown():
    if t.is_alive():
        t.alive = False

    pg.quit()
    sys.exit()


def update_screen():
    if lcd.screen:
        lcd_rect = lcd.screen.get_rect()
        lcd_rect.center = buffer_image.get_rect().center
        buffer_image.blit(lcd.screen, lcd_rect)

    if device_image:
        device_rect = device_image.get_rect()
        device_rect.center = buffer_image.get_rect().center
        buffer_image.blit(device_image, device_rect)

    scaled_image = buffer_image
    scaled_rect = scaled_image.get_rect()
    scaled_rect.center = buffer_image.get_rect().center
    if args.device == devices.M5STICKV:
        scaled_image = pg.transform.smoothscale(
            buffer_image, (screen.get_width() * 0.95, screen.get_height() * 0.85)
        )
        scaled_rect = scaled_image.get_rect()
        scaled_rect.center = buffer_image.get_rect().center
    screen.blit(scaled_image, scaled_rect)

    pg.display.flip()


try:
    clock = pg.time.Clock()
    while True:
        clock.tick(60)

        if sequence_executor:
            if not sequence_executor.commands and args.exit_after_sequence:
                shutdown()
            sequence_executor.execute()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                shutdown()
            elif event.type >= pg.USEREVENT:
                if event.type == events.SCREENSHOT_EVENT:
                    SCREENSHOTS_DIR = "screenshots"
                    if not os.path.exists(SCREENSHOTS_DIR):
                        os.makedirs(SCREENSHOTS_DIR)

                    sub = screen.subsurface(devices.screenshot_rect(args.device)).convert_alpha()
                    sub.blit(mask_img, sub.get_rect(), None, pg.BLEND_RGBA_SUB)
                    if (args.screenshot_scale):
                        sub = pg.transform.smoothscale(sub, device_screenshot_size)
                    pg.image.save(
                        sub, os.path.join(SCREENSHOTS_DIR, event.dict["filename"].replace(".png", screenshot_suffix + ".png"))
                    )
                else:
                    event.dict["f"]()
                    update_screen()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:
                    buttons.buttons_control.enter_event_flag = True
                if event.key == pg.K_DOWN:
                    buttons.buttons_control.page_event_flag = True
                if event.key == pg.K_UP:
                    buttons.buttons_control.page_prev_event_flag = True
            if event.type == pg.MOUSEBUTTONDOWN:
                ft6x36.touch_control.trigger_event()

except KeyboardInterrupt:
    shutdown()
