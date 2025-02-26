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
import sys
import re
import bdftohex
import hexfill
import hexmerge
import hextokff

FONT14 = "ter-u14n"
FONT16 = "ter-u16n"
FONT24 = "ter-u24b"
WIDE14 = "FusionPixel-14"
WIDE16 = "unifont-16"
WIDE24 = "NotoSansCJK-24"


def open_bdf_save_kff(filename, width, height):
    """Open a bdf font filename and save the corresponding kff file based on the filename"""

    filename_kff = "tiny"
    if filename == FONT16:
        filename_kff = "small"
    elif filename == FONT24:
        filename_kff = "medium"
    elif filename == WIDE14:
        filename_kff = "tiny_wide"
    elif filename == WIDE16:
        filename_kff = "small_wide"
    elif filename == WIDE24:
        filename_kff = "medium_wide"

    # Create hexfile based on bdf
    font_hex = "\n".join(bdftohex.bdftohex(filename + ".bdf")) + "\n"
    with open(filename + ".hex", "w", encoding="utf-8", newline="\n") as save_file:
        save_file.write(font_hex)

    # Fill the hexfile with missing empty glyphs
    font_hex_filled = "".join(hexfill.hexfill(filename + ".hex", width, height)).strip()
    with open(filename + ".hex", "w", encoding="utf-8", newline="\n") as save_file:
        save_file.write(font_hex_filled)

    # Merges the hexfile empty glyphs with the its corresponding contents
    # (can be used with multiple files)
    font_hex_merged = "\n".join(hexmerge.hexmerge(filename + ".hex")) + "\n"
    with open(filename + ".hex", "w", encoding="utf-8", newline="\n") as save_file:
        save_file.write(font_hex_merged)

    # Creates the Krux font file, to be used on each project
    # font.c file: ../MaixPy/projects/<device_name>/compile/
    # overrides/components/micropython/port/src/omv/img/font.c
    # in order to replace the contents of the unicode[] variable
    #  in the font.c
    wide_glyphs = None
    if filename in (WIDE14, WIDE16, WIDE24):
        wide_glyphs = ["ko-KR", "zh-CN", "ja-JP"]
    font_kff = hextokff.hextokff(filename + ".hex", width, height, wide_glyphs)
    with open(filename_kff + ".kff", "w", encoding="utf-8", newline="\n") as save_file:
        save_file.write(font_kff)

    # Deletes the temporary hexfile
    os.remove(filename + ".hex")


def save_new_fontc(font_name, overwrite=False):
    """If overwrite=True them overwrite the content of the font.c file
    on each project, based on the font_name passed otherwise save
    a new font.c file"""

    filename_kff = "tiny"
    device_name = "m5stickv"
    if font_name == FONT16:
        filename_kff = "small"
        device_name = "dock"
    elif font_name == FONT24:
        filename_kff = "medium"
        device_name = "amigo"
    elif font_name == WIDE14:
        filename_kff = "tiny_wide"
    elif font_name == WIDE16:
        filename_kff = "small_wide"
        device_name = "dock"
    elif font_name == WIDE24:
        filename_kff = "medium_wide"
        device_name = "amigo"

    maixpy_path_start = "../MaixPy/projects/maixpy_"
    maixpy_path_end = (
        "/compile/overrides/components/micropython/port/src/omv/img/font.c"
    )

    with open(filename_kff + ".kff", "r", encoding="utf-8") as read_file:
        content_kff = read_file.read()

    if font_name in (WIDE14, WIDE16, WIDE24):
        re_escape_str = "static uint8_t unicode_wide[] = {\n"
        content_kff = re_escape_str + content_kff + "\n};"
    else:
        re_escape_str = "static uint8_t unicode[] = {\n"
        content_kff = re_escape_str + content_kff + "\n};"

    filename = maixpy_path_start + device_name + maixpy_path_end
    with open(filename, "r", encoding="utf-8") as font_file:
        lines = font_file.read()
        unicode_str = re.sub(
            re.escape(re_escape_str)
            + r"((0[xX][\da-fA-F]{2},)\n?)*0[xX][\da-fA-F]{2}\n};",
            content_kff,
            lines,
        )

    if overwrite:
        with open(filename, "w", encoding="utf-8", newline="\n") as save_file:
            save_file.write(unicode_str)

        # Also replace for bit, yahboom, wonder_mv, and yahboom_devkit
        if font_name in (FONT16, WIDE16):
            for project in ["bit", "yahboom", "wonder_mv", "yahboom_devkit"]:
                filename = maixpy_path_start + project + maixpy_path_end
                with open(filename, "w", encoding="utf-8", newline="\n") as save_file:
                    save_file.write(unicode_str)

        # Also replace for Cube
        if font_name in (FONT14, WIDE14):
            filename = maixpy_path_start + "cube" + maixpy_path_end
            with open(filename, "w", encoding="utf-8", newline="\n") as save_file:
                save_file.write(unicode_str)
    else:
        with open(
            filename_kff + "_font.c", "w", encoding="utf-8", newline="\n"
        ) as save_file:
            save_file.write(unicode_str)

    # Deletes the temporary kff file
    os.remove(filename_kff + ".kff")


if __name__ == "__main__":

    replace = len(sys.argv) > 1 and sys.argv[1] == "True"

    # generate kff files
    open_bdf_save_kff(FONT14, 8, 14)
    open_bdf_save_kff(FONT16, 8, 16)
    open_bdf_save_kff(FONT24, 12, 24)
    open_bdf_save_kff(WIDE14, 14, 14)
    open_bdf_save_kff(WIDE16, 16, 16)
    open_bdf_save_kff(WIDE24, 24, 24)

    # generate new font.c files (delete kff files)
    save_new_fontc(FONT14, replace)
    save_new_fontc(FONT16, replace)
    save_new_fontc(FONT24, replace)
    save_new_fontc(WIDE14, replace)
    save_new_fontc(WIDE16, replace)
    save_new_fontc(WIDE24, replace)
