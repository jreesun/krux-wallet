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
# pylint: disable=C0301
# pylint: disable=C0103


import sys
import math
import os
import json


BYTE_LEN = 2
DEFAULT_CODEPOINTS = [
    ord(char)
    for char in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 !#$%&'()*+,-./:;<=>?@[\\]^_\"{|}~█₿ ⊚↳«»"
]
TRANSLATIONS_DIR = "../../i18n/translations"

JAPANESE_CODEPOINT_MIN = 0x3000  # defined as WIDEFONT_CODEPOINT_MIN in MaixPy
JAPANESE_CODEPOINT_MAX = 0x30FF
CHINESE_CODEPOINT_MIN = 0x4E00
CHINESE_CODEPOINT_MAX = 0x9FFF
KOREAN_CODEPOINT_MIN = 0xAC00
KOREAN_CODEPOINT_MAX = 0xD7A3
FULLHALFWIDTH_CODEPOINT_MIN = 0xFF00
FULLHALFWIDTH_CODEPOINT_MAX = 0xFFEF  # defined as WIDEFONT_CODEPOINT_MAX in MaixPy


def hextokff(filename=None, width=None, height=None, wide_glyphs=None):
    """Convert a hex formatted bitmap font file to a kff file"""

    if filename is None or width is None or height is None:
        raise ValueError(
            "ERROR: Provide the filename.hex, width and height as arguments"
        )

    width = int(width)
    height = int(height)

    width_bytes = math.ceil(width / 8)

    # Scan the translations folder and build a set of unique codepoints used
    # across all translations
    if not wide_glyphs:
        used_codepoints = set(DEFAULT_CODEPOINTS)
    else:
        used_codepoints = set()
    for translation_file in os.listdir(TRANSLATIONS_DIR):
        current_translation = translation_file[:5]
        if not wide_glyphs or current_translation in wide_glyphs:
            file_path = os.path.join(TRANSLATIONS_DIR, translation_file)

            with open(file_path, "r", encoding="utf-8") as file:
                translations = json.load(file)

            for translation in translations.values():
                for char in translation:
                    # If Japanese, Chinese, or Korean codepoint
                    if (
                        JAPANESE_CODEPOINT_MIN <= ord(char) <= JAPANESE_CODEPOINT_MAX
                        or CHINESE_CODEPOINT_MIN <= ord(char) <= CHINESE_CODEPOINT_MAX
                        or KOREAN_CODEPOINT_MIN <= ord(char) <= KOREAN_CODEPOINT_MAX
                        or FULLHALFWIDTH_CODEPOINT_MIN
                        <= ord(char)
                        <= FULLHALFWIDTH_CODEPOINT_MAX
                    ):
                        # only include if wide_glyphs required by this locale
                        if wide_glyphs and current_translation in wide_glyphs:
                            used_codepoints.add(ord(char))
                    elif wide_glyphs is None:
                        used_codepoints.add(ord(char))

    with open(filename, "r", encoding="utf-8") as input_file:
        # Read in a hex formatted bitmap font file
        lines = input_file.readlines()

        # Output in modified dkz format ("krux font format") where first two bytes
        # of each row are the codepoint
        bitmap = []
        total_codepoints = 0
        for line in lines:
            line = line.rstrip("\n")
            codepoint, glyph = line.split(":")
            if int(codepoint, 16) not in used_codepoints:
                continue

            total_codepoints += 1

            # Prefix with codepoint bytes
            rows = [f"0x{codepoint[:2]},0x{codepoint[2:]}"]

            for x in range(width_bytes):
                row = []
                for y in range(height):
                    glyph_index = y * BYTE_LEN * width_bytes + (x * BYTE_LEN)
                    row.append("0x" + glyph[glyph_index : glyph_index + BYTE_LEN])
                rows.append(",".join(row))
            bitmap.append(",\n".join(rows))

        # Prefix with number of codepoints as two hex bytes
        total_codepoints = f"{total_codepoints:04X}"
        return ",\n".join(
            [f"0x{total_codepoints[:2]},0x{total_codepoints[2:]}"] + bitmap
        )


if __name__ == "__main__":
    if len(sys.argv) > 3:
        print(hextokff(sys.argv[1], sys.argv[2], sys.argv[3]))
    else:
        raise ValueError(
            "ERROR: Provide the filename.hex, width and height as arguments"
        )
