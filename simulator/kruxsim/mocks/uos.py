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

old_listdir = os.listdir
old_remove = os.remove
old_chdir = os.chdir


def new_listdir(path, *args, **kwargs):
    if path.startswith("/sd"):
        path = path.lstrip("/")
    elif path.startswith("/flash"):
        path = path.replace("/flash", "sd")
    return old_listdir(path, *args, **kwargs)


def new_remove(path, *args, **kwargs):
    if path.startswith("/sd"):
        path = path.lstrip("/")
    elif path.startswith("/flash"):
        return
    return old_remove(path, *args, **kwargs)

# Avoid Krux code to change simulator execution dir
def new_chdir(path):
    return


setattr(os, "listdir", new_listdir)
setattr(os, "remove", new_remove)
setattr(os, "chdir", new_chdir)
