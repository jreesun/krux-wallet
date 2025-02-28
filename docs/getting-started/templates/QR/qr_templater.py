# The MIT License (MIT)

# Copyright (c) 2024-2024 Krux contributors

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

"""
Generate a QR Code template for manual transcription as an SVG and PNG.
Includes:
  - Finder patterns (orientation stones) + 1-module white separator around them
  - Timing patterns (excluding overlap with finders)
  - Alignment patterns
  - 2-module-thick Quiet Zone around the code
  - Optionally (if "draw_dots=True"), places a 2x2 px gray square
    at the center of each data module.
  - Optionally (if "draw_lines=True"), draws lines between data modules.
  - Optionally (if "draw_regions=True"), draws lines to separate the regions every 5 or 7 modules.

Usage:
  python qr_v4_template.py all      # generate 3 models for each version
  python qr_v4_template.py v3 dots  # Version 3-29x29 QR with gray guide dots
  python qr_v4_template.py v4 lines # Version 4-33x33 QR with lines between modules
  python qr_v4_template.py v2 dots regions  # Version 2-25x25 QR with lines to separate modules
                                            # and thiecker lines to separate regions
"""

import sys
import cairosvg
import os

def create_qr_code_v4_template_svg(
    version=1,
    module_size=10,
    quiet_zone=2,
    file_name="qr.svg",
    draw_dots=False,
    draw_lines=False,
    draw_regions=False
):
    """
    Create an SVG file containing the static (function) patterns for a QR code of the specified version.

    :param version:     QR code version (1 to 5)
    :param module_size: Size (in px) of each QR "module"
    :param quiet_zone:  Number of modules of white margin around the code
    :param file_name:   Output SVG file name
    :param draw_dots:   Whether to draw 2x2 px gray squares in data modules
    :param draw_lines:  Whether to draw lines between data modules
    :param draw_regions: Whether to draw lines to separate the regions every 5 modules
    """

    if version not in range(1, 6):
        raise ValueError("Version must be between 1 and 5")

    # ------------------------------------------------------------
    # 1. Basic dimensions:
    #    - Version 1 => code_modules = 21
    #    - Version 2 => code_modules = 25
    #    - Version 3 => code_modules = 29
    #    - Version 4 => code_modules = 33
    #    - Version 5 => code_modules = 37
    #    - total_modules = code_modules + 2 * quiet_zone
    # ------------------------------------------------------------
    code_modules = 17 + 4 * version
    total_modules = code_modules + 2 * quiet_zone

    # We'll maintain TWO 2D arrays of booleans (size total_modules × total_modules):
    # - qr_matrix[r][c]: whether the final module is black (True) or white (False)
    # - function_matrix[r][c]: whether the module is a function pattern (True) or data area (False)
    #
    # By default, everything is white (False) and everything is data (False).
    qr_matrix = [[False for _ in range(total_modules)] 
                 for _ in range(total_modules)]
    function_matrix = [[False for _ in range(total_modules)]
                       for _ in range(total_modules)]

    # Helper: mark a cell as part of a function pattern (optionally black).
    def set_module_as_function(r, c, black=False):
        r += quiet_zone
        c += quiet_zone
        if 0 <= r < total_modules and 0 <= c < total_modules:
            function_matrix[r][c] = True
            if black:
                qr_matrix[r][c] = True
    # ------------------------------------------------------------
    # 2. Place a 7×7 Finder Pattern + 1-module all-white separator around it.
    #    For corners: (0,0), (0,code_modules-7), (code_modules-7,0).
    # ------------------------------------------------------------
    def place_finder_pattern(r0, c0):
        # Mark the 8×8 region (including the 1-module ring) as function=white.
        for rr in range(r0 - 1, r0 + 8):
            for cc in range(c0 - 1, c0 + 8):
                if 0 <= rr < code_modules and 0 <= cc < code_modules:
                    set_module_as_function(rr, cc)

        # Now draw the 7×7 black squares (finder)
        for rr in range(7):
            for cc in range(7):
                R = r0 + rr
                C = c0 + cc
                if (0 <= R < code_modules) and (0 <= C < code_modules):
                    black = True if rr in [0, 6] or cc in [0, 6] else False
                    set_module_as_function(R, C, black)

        # Inner 3×3 black
        for rr in range(2, 5):
            for cc in range(2, 5):
                set_module_as_function(r0 + rr, c0 + cc, black=True)

    # Place the three finder patterns
    place_finder_pattern(0, 0)                  # top-left
    place_finder_pattern(0, code_modules - 7)   # top-right
    place_finder_pattern(code_modules - 7, 0)   # bottom-left

    # ------------------------------------------------------------
    # 3. Timing patterns (row=6, col=7..code_modules-8) and (col=6, row=7..code_modules-8)
    #    black if index is even, else white (but marked function).
    # ------------------------------------------------------------
    for col in range(7, code_modules - 7):
        # row=6, col
        black = True if col % 2 == 0 else False
        set_module_as_function(6, col, black)

    for row in range(7, code_modules - 7):
        # row, col=6
        black = True if row % 2 == 0 else False
        set_module_as_function(row, 6, black)

    # ------------------------------------------------------------
    # 4. Alignment Patterns for Versions 2 to 5
    #    Skip corners if they overlap the 7×7 finder blocks.
    # ------------------------------------------------------------
    def place_alignment_pattern(r_center, c_center):
        r0 = r_center - 2
        c0 = c_center - 2
        for rr in range(5):
            for cc in range(5):
                R = r0 + rr
                C = c0 + cc
                # Outer border => black
                black = True if rr in [0, 4] or cc in [0, 4] else False
                set_module_as_function(R, C, black)
        # center dot
        set_module_as_function(r_center, c_center, black=True)

    alignment_centers = {
        2: [6, 18],
        3: [6, 22],
        4: [6, 26],
        5: [6, 30]
    }.get(version, [])

    for r_center in alignment_centers:
        for c_center in alignment_centers:
            # Skip if it overlaps the 7×7 corner
            if (r_center < 7 and c_center < 7):  # top-left
                continue
            if (r_center < 7 and c_center > code_modules - 8):  # top-right
                continue
            if (r_center > code_modules - 8 and c_center < 7):  # bottom-left
                continue
            place_alignment_pattern(r_center, c_center)

    # ------------------------------------------------------------
    # 5. Generate the SVG
    # ------------------------------------------------------------
    svg_width = total_modules * module_size
    svg_height = total_modules * module_size

    svg_parts = []
    svg_parts.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'width="{svg_width}" '
        f'height="{svg_height}" '
        f'viewBox="0 0 {svg_width} {svg_height}">'
    )
    # A white background
    svg_parts.append('<rect width="100%" height="100%" fill="white" />')

    # Draw each cell (big matrix) as black or white
    for row in range(total_modules):
        for col in range(total_modules):
            color = "black" if qr_matrix[row][col] else "white"
            x = col * module_size
            y = row * module_size
            svg_parts.append(
                f'<rect x="{x}" y="{y}" width="{module_size}" height="{module_size}" '
                f'fill="{color}" />'
            )

    # If draw_dots=True, place 2x2 px gray squares in the center of data modules.
    if draw_dots:
        for r_code in range(code_modules):
            for c_code in range(code_modules):
                r_big = r_code + quiet_zone
                c_big = c_code + quiet_zone
                # If not function => data module => place the gray guide
                if not function_matrix[r_big][c_big]:
                    x_center = c_big * module_size + (module_size / 2)
                    y_center = r_big * module_size + (module_size / 2)
                    x_small = x_center - 1
                    y_small = y_center - 1
                    svg_parts.append(
                        f'<rect x="{x_small:.1f}" y="{y_small:.1f}" '
                        f'width="2" height="2" fill="gray" />'
                    )
    
    # If draw_lines=True, draw rectangles with no filling and border width = 0.5
    if draw_lines:
        for r_code in range(code_modules):
            for c_code in range(code_modules):
                r_big = r_code + quiet_zone
                c_big = c_code + quiet_zone
                if not function_matrix[r_big][c_big]:
                    x = c_big * module_size
                    y = r_big * module_size
                    svg_parts.append(
                        f'<rect x="{x:.1f}" y="{y:.1f}" width="{module_size}" height="{module_size}" '
                        f'fill="none" stroke="gray" stroke-width="0.5" />'
                    )

    # If draw_regions=True, draw lines to separate the regions every <region_size> modules
    region_size = 7 if version == 1 else 5
    if draw_regions:
        regions_thickness = 0.5 if not draw_lines else 1
        stroke_color = "gray" if not draw_lines else "black"
        # Draw horizontal legend on top quiet zone row
        for c_code in range(code_modules):
            c_big = c_code + quiet_zone
            if (c_code - 1) % region_size == region_size - 1:
                x = (c_big + region_size // 2) * module_size
                y = 0
                svg_parts.append(
                    f'<text x="{x + 2:.1f}" y="{y + 10:.1f}" font-family="monospace" font-size="10" '
                    f'fill="{stroke_color}">{c_code // region_size + 1}</text>'
                )
        # Draw vertical legend on left quiet zone column
        for r_code in range(code_modules):
            r_big = r_code + quiet_zone
            if (r_code - 1) % region_size == region_size - 1:
                x = 0
                y = (r_big + region_size // 2) * module_size
                svg_parts.append(
                    f'<text x="{x + 2:.1f}" y="{y + 10:.1f}" font-family="monospace" font-size="10" '
                    f'fill="{stroke_color}">{chr(65 + r_code // region_size)}</text>'
                )
        for r_code in range(code_modules):
            for c_code in range(code_modules):
                r_big = r_code + quiet_zone
                c_big = c_code + quiet_zone
                if not function_matrix[r_big][c_big]:
                    if r_code and (r_code - 1) % region_size == region_size - 1:
                        x = c_big * module_size
                        y = r_big * module_size
                        svg_parts.append(
                            f'<line x1="{x:.1f}" y1="{y:.1f}" x2="{x + module_size:.1f}" y2="{y:.1f}" '
                            f'stroke="{stroke_color}" stroke-width="{regions_thickness}" />'
                        )
                    if c_code and (c_code - 1) % region_size == region_size -1:
                        x = c_big * module_size
                        y = r_big * module_size
                        svg_parts.append(
                            f'<line x1="{x:.1f}" y1="{y:.1f}" x2="{x:.1f}" y2="{y + module_size:.1f}" '
                            f'stroke="{stroke_color}" stroke-width="{regions_thickness}" />'
                        )

    svg_parts.append('</svg>')
    svg_content = "\n".join(svg_parts)

    # ------------------------------------------------------------
    # 6. Write the SVG file
    # ------------------------------------------------------------
    with open(file_name, 'w', encoding='utf-8') as f:
        f.write(svg_content)

    msg = f"Created '{file_name}' (Version {version} with {quiet_zone}-module Quiet Zone)"
    if draw_dots:
        msg += " and data dots."
    print(msg + ".")

def export_svg_and_png(draw_dots, draw_lines, draw_regions, version=4):
    """
    Export the SVG and PNG files for the QR code template.
    """
    file_name = "qr"
    file_name += "_v" + str(version)
    if draw_dots:
        file_name += "_dots"
    if draw_lines:
        file_name += "_lines"
    if draw_regions:
        file_name += "_regions"
    file_name += ".svg"

    create_qr_code_v4_template_svg(
        version=version,
        module_size=10,   # px
        quiet_zone=2,     # 2 modules of quiet zone
        file_name=file_name,
        draw_dots=draw_dots,
        draw_lines=draw_lines,
        draw_regions=draw_regions
    )

    # Export a png file, scaled up 10x
    # Create the directory if it doesn't exist
    os.makedirs("pngQRs", exist_ok=True)
    png_file_name = "pngQRs/" + file_name[:-4] + ".png"
    cairosvg.svg2png(url=file_name, write_to=png_file_name, scale=10)

def main():
    """
    Main entry point. If the word "dots" is passed as a command-line arg,
    we enable the 2x2 px gray data module squares.
    """
    # Detect features in sys.argv
    all_models = ("all" in sys.argv)
    if all_models:
        for version in range(1, 6):
            # Model 1
            draw_dots = True
            draw_lines = False
            draw_regions = True
            export_svg_and_png(draw_dots, draw_lines, draw_regions, version)

            # Model 2
            draw_dots = False
            draw_lines = True
            draw_regions = True
            export_svg_and_png(draw_dots, draw_lines, draw_regions, version)

            # Model 2
            draw_dots = True
            draw_lines = True
            draw_regions = True
            export_svg_and_png(draw_dots, draw_lines, draw_regions, version)

    else:

        # Look for an argument with vX (e.g., v4) to specify the version
        version = None
        for arg in sys.argv:
            if arg.startswith("v") and arg[1:].isdigit():
                version = int(arg[1:])
                break
        if version is None:
            print("Please specify a version (e.g., 'v4') to generate the template.")
            return
        
        draw_dots = ("dots" in sys.argv)
        draw_lines = ("lines" in sys.argv)
        draw_regions = ("regions" in sys.argv)
        export_svg_and_png(draw_dots, draw_lines, draw_regions, version)
    
    # Move all the SVG files to the "svgQRs" directory
    os.makedirs("svgQRs", exist_ok=True)
    os.system("mv *.svg svgQRs")

if __name__ == "__main__":
    main()
