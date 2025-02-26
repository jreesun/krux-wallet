[![created at](https://img.shields.io/github/created-at/selfcustody/krux)](https://github.com/selfcustody/krux/commit/bb8e2d63e031417111ff7cb2b8877c10e19410be)
[![downloads](https://img.shields.io/github/downloads/selfcustody/krux/total)](https://github.com/selfcustody/krux/releases)
[![downloads (latest release)](https://img.shields.io/github/downloads/selfcustody/krux/latest/total)](https://github.com/selfcustody/krux/releases)
[![contributors](https://img.shields.io/github/contributors-anon/selfcustody/krux)](https://github.com/selfcustody/krux/graphs/contributors)
[![commit activity](https://img.shields.io/github/commit-activity/y/selfcustody/krux)](https://github.com/selfcustody/krux/commits)
[![codecov](https://codecov.io/gh/selfcustody/krux/branch/main/graph/badge.svg?token=XU80PT6Q9V)](https://codecov.io/gh/selfcustody/krux)
[![calver](https://img.shields.io/badge/calver-YY.0M.MICRO-22bfda.svg)](https://calver.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/selfcustody/krux/blob/main/LICENSE.md)

<p align="center">
<img src="docs/img/maixpy_yahboom/logo-312.png" alt="yahboom" style="width: 11%;">
<img src="docs/img/maixpy_amigo/logo-300.png"  alt="maixpy amigo" style="width: 16%;">
<img src="docs/img/maixpy_dock/logo-302.png" alt="maixpy dock" style="width: 15%;">
<img src="docs/img/maixpy_wonder_mv/logo-304.png" alt="wonder mv" style="width: 11%;">
<img src="docs/img/maixpy_m5stickv/logo-250.png" alt="m5stickv" style="width: 6%;">
<img src="docs/img/maixpy_cube/logo-400.png" alt="maixpy cube" style="width: 10%;">
</p>

Krux is an open-source firmware facilitating the creation of Bitcoin signing devices from readily available components, such as Kendryte K210 devices. It transforms these devices into airgapped tools capable of handling transactions for both single and multisignature wallets, supporting offline signing via QR code or SD card, thus empowering users to securely self-custody their Bitcoin.

---
## Disclaimer
**WARNING**: *This software has not yet been formally audited by a third party. Use at your own risk!*

---

# Getting Started
Detailed instructions for installing and running Krux can now be found in our [official documentation](https://selfcustody.github.io/krux/).


The instructions below are intended for programmers or developers who want to contribute to the project.

## Download our firmware releases
[<img src="docs/img/badge_github.png" alt="github releases page" width="186">](https://github.com/selfcustody/krux/releases)

# Development
## Fetch the code
This will download the source code of Krux as well as the code of all its dependencies inside a new folder called `krux`:
```bash
git clone --recurse-submodules https://github.com/selfcustody/krux
```

Note: When you wish to pull updates (to all submodules, their submodules, ...) to this repo, use:
```bash
git pull origin main && git submodule update --init --recursive
```

## Krux (script) (Linux or WSL)
The [krux](krux) bash script contains commands for common development tasks. It assumes a Linux host, you will need to have [Docker Desktop or Docker Engine](https://docs.docker.com/desktop/) (don't forget to add your user to the docker group `sudo usermod -aG docker $USER`), `openssl`, and `wget` installed at a minimum for the commands to work as expected. It works on Windows using WSL. The channel Crypto Guide from Youtube made a step-by-step video - [Krux DIY Bitcoin Signer: Build From Source & Verify (With Windows + WSL2 + Docker)](https://www.youtube.com/watch?v=Vmr_TFy2TfQ)

To build and flash the firmware:
```bash
# build firmware for Maix Amigo
./krux build maixpy_amigo

# flash the firmware to Maix Amigo
./krux flash maixpy_amigo
```

The first time, the build can take around an hour or so to complete. Subsequent builds should take only a few minutes. If all goes well, you should see a new `build` folder containing `firmware.bin` and `kboot.kfpkg` files when the build completes.

## Install Krux and dev tools
Krux uses [Poetry](https://python-poetry.org/) as Python packaging and dependency management. This cmd installs development dependencies like [embit](https://github.com/diybitcoinhardware/embit), [ur](https://github.com/selfcustody/foundation-ur-py) and [urtypes](https://github.com/selfcustody/urtypes), and tools to run [tests](https://docs.pytest.org), review code with [pylint](https://pypi.org/project/pylint/), format code with [black](https://github.com/psf/black) and a lib to help handle i18n translations.
```bash
pip install poetry
poetry install
```

If you have a problem installing Poetry on Linux OS:
```bash
# we considered the name of the venv .krux
python -m venv .krux
source .krux/bin/activate
```
The result will be something like:
```bash
(.krux) username:~/directory name$ 
```
Now you can run normaly the pip of the poetry:
```bash
pip install poetry
poetry install
```

Note: when changing the dependencies in `pyptoject.toml` you need to generate a new `poetry.lock` file using the cmd: `poetry lock --no-update`.

## Format code
```bash
poetry run poe format
```

## Review code
```bash
poetry run poe lint
```

## Run tests with coverage
```bash
poetry run poe test
```

Note: The coverage report will be created at the `htmlcov` folder `file:///path/to/krux/htmlcov/index.html`. 

For more verbose output (e.g., to see the output of print statements):
```bash
poetry run poe test-verbose
```

To run just a specific test from a specific file:
```bash
poetry run pytest --cache-clear ./tests/pages/test_login.py -k 'test_load_key_from_hexadecimal'
```

## Use the Python interpreter (REPL)
This is useful for rapid development of non-visual code:
```bash
poetry run python
```
```
Python 3.9.1
Type "help", "copyright", "credits" or "license" for more information.
>>> from krux.key import Key
>>> Key("olympic term tissue route sense program under choose bean emerge velvet absurd", False).xpub()
'tpubDCDuqu5HtBX2aD7wxvnHcj1DgFN1UVgzLkA1Ms4Va4P7TpJ3jDknkPLwWT2SqrKXNNAtJBCPcbJ8Tcpm6nLxgFapCZyhKgqwcEGv1BVpD7s'
>>>
```

## Run the device simulator
This is useful for rapid code development that utilizes UI/UX. It is also good for newcomers to try Krux before purchasing a device. However, the simulator does not behave exactly as the HW device and may not have all features implemented (e.g. scanning via camera a TinySeed currently only works on the HW device).

Before executing, make sure you have installed the poetry extras:
```bash
# This cmd will uninstall other extras
poetry install --extras simulator

# To install all extras, use:
poetry install --all-extras
```

Run the simulator:
```bash
# Run simulator with the touch device Amigo, then use mouse to navigate
poetry run poe simulator

# Run simulator with SD enabled (folder `simulator/sd`) on the small button-only device M5stickV, then use keyboard (arrow keys UP or DOWN and ENTER)
poetry run poe simulator-m5stickv --sd

# Run simulator on the device dock, then use keyboard (arrow keys UP or DOWN and ENTER)
poetry run poe simulator-dock

# Run simulator with the touch device yahboom, then use mouse to navigate
poetry run poe simulator-yahboom

# Run simulator on the device cube, then use keyboard (arrow keys UP or DOWN and ENTER)
poetry run poe simulator-cube

# Run simulator with the touch device wonderMV, then use mouse to navigate
poetry run poe simulator-wonder-mv
```

Note: With emulated SD card it is possible to store settings, encrypted mnemonics, also drop and sign PSBTs. After some time running, the simulator may become slow. If that happens, just close and open again!

```bash
# ImportError: Unable to find zbar shared library
sudo apt install python3-zbar

# ImportError: libGL.so.1: cannot open shared object file: No such file or directory
sudo apt install libgl1

# `pygame.error: No available video device`
# You are trying to run the simulator on an OS without a GUI (some kind of terminal only or WSL). Try one with GUI!

# Depending on the OS, it may be necessary to install zbar-tools too:
sudo apt install zbar-tools
```

### Simulator sequences execution

This is useful for taking screenshots of device screens to use in documentation:
```bash
# Run all sequences of commands on all devices and in all locales (languages) [Linux OS]
cd simulator
./generate-all-screenshots.sh

# Run a specific sequence for a specific device's with SD enabled (folder `simulator/sd`)
poetry run poe simulator --sequence sequences/about.txt --sd

# Sequence screenshots are scaled to fit in docs. Use --no-screenshot-scale to get full size
poetry run poe simulator --sequence sequences/home-options.txt --no-screenshot-scale
```

## Live debug a device (Linux)
It is not possible to drop into a live Python REPL anymore as we disabled the `MICROPY_ENABLE_COMPILER` flag in `firmware\MaixPy\components\micropython\port\include\mpconfigport.h`. If you enable it again it will be possible to drop into a live Python REPL by issuing an interrupt with Ctrl-C:

If you've made a fresh build and flashed it to your device, you can connect to the device over serial connection with:
```bash
screen /dev/tty.usbserial-device-name 115200
```

If successful, the device should restart and you should see:
```bash
K210 bootloader by LoBo v.1.4.1

* Find applications in MAIN parameters
0: '       firmware', @ 0x00080000, size=XXX, app_size=XXX, App ok, ACTIVE
* Loading app from flash at 0x00080000 (XXX B)
* Starting at 0x80000000 ...


[MAIXPY] Pll0:freq:XXX
[MAIXPY] Pll1:freq:XXX
[MAIXPY] Pll2:freq:XXX
[MAIXPY] cpu:freq:XXX
[MAIXPY] kpu:freq:XXX
[MAIXPY] Flash:0xef:0x17
[MaixPy] gc heap=0x8029f430-0x8036f430(851968)
init i2c:2 freq:XXX
[MAIXPY]: find ov7740
[MAIXPY]: find ov sensor
```
Some devices like Amigo have two serial ports, check the second one if you don't read data from first.

To leave `screen` serial monitor press `Ctrl+a`, followed by `k`, then confirm with `y`.

## Live debug a device using MaixPy IDE (Mac or Windows)
Use [MaixPy IDE](https://dl.sipeed.com/shareURL/MAIX/MaixPy/ide/v0.2.5) to debug the devices. Click on `Tools > Open Terminal > New Terminal > Connect to serial port > Select a COM port available` (if didn't work, try another COM port). We have removed some support for MaixPy IDE (due to size constraints), but the debug works.

## WDT watchdog
Krux makes use of MaixPy's [WDT watchdog module](https://wiki.sipeed.com/soft/maixpy/en/api_reference/machine/wdt.html), you can see it [here](src/krux/wdt.py). This will reset the device if not fed for some time. To stop the watchdog, when connected through the terminal, run the following (starting from v24.07.0 this is no loger possible because the Python real-time compiler and REPL were disabled):
```python
# Run this everytime you want to stop the watchdog

from krux.wdt import wdt
wdt.stop()
```

Now, with watchdog disabled, you can use debug the device normally. Also remember to disable the `Settings > Security > Shutdown Time` setting it to `0` to no more automatic resets, and if you added any print statements to the code, they should appear whenever your code is reached.

## Create new translations - i18n
The project has lots of translations [here](i18n/translations), if you add new english messages in code using `t()` function, you will need to:

```bash
# Clean unused translations:
poetry run poe i18n clean

# Create a new translation file in JSON:
poetry run poe i18n new tr-TR

# Use Google translate to create missing translations, copy them to respective files, review phrases and commas.
poetry run poe i18n fill

# Create missing translations for a single language. Ex: Brazilian Portuguese
poetry run poe i18n fill pt-BR

# Make sure all files have this new translated message:
poetry run poe i18n validate

# Format translation files properly:
poetry run poe i18n prettify

# Create the compiled table for krux translations.py
poetry run poe i18n bake
```

## Fonts
Learn about how to setup fonts [here](firmware/font/README.md)

## Colors
Use [this script](firmware/scripts/rgbconv.py) to generate device compatible colors from RGB values (usefull for color themes).

## Documentation
Before change documentation, and run the mkdocs server, make sure you have installed the poetry extras:

```bash
# This cmd will uninstall other extras
poetry install --extras docs

# To install all extras, use:
poetry install --all-extras
```

To change lateral and upper menus on documentation, see `mkdocs.yml` file on `nav` section. To create or edit translations (TODO: need help!), read [here](i18n/README.md).

Create the documentation site locally - `http://127.0.0.1:8000/krux/`:
```bash
poetry run poe docs
```

# Inspired by these similar projects
- https://github.com/SeedSigner/seedsigner for Raspberry Pi (Zero)
- https://github.com/diybitcoinhardware/f469-disco for the F469-Discovery board

# Powered by
- [embit](https://embit.rocks/), a Bitcoin library for Python 3 and Micropython
- [MaixPy](https://github.com/sipeed/MaixPy), MicroPython for K210 RISC-V
- [MicroPython](https://github.com/micropython/micropython), a lean and efficient Python implementation for microcontrollers and constrained systems
- [Kboot](https://github.com/loboris/Kboot) and [ktool](https://github.com/loboris/ktool)

# Contributing
Issues and pull requests welcome! Let's make this as good as it can be.

Feel free to start a [new discussion](https://github.com/selfcustody/krux/discussions) or an [issue](https://github.com/selfcustody/krux/issues) for work. When making your pull request, explain what it solves, ideally each PR should focus on solving one issue (exceptions can be made if the work is related or tightly coupled).

**Note for PR's**: Checkout and branch off of the `develop` branch, please also make sure to explicitly target `develop`; `main` is the default branch for the latest version and also for downloading and installing Krux from source.

# Support
For technical support installing or using Krux, you can join our [Telegram chat](https://t.me/SC_Krux). Follow us on [X (Twitter)](https://x.com/selfcustodykrux) or send a message to the [Bitcoin Forum](https://bitcointalk.org/index.php?topic=5489022.0). Also check out the [DIYbitcoin chat](https://t.me/diybitcoin) on Telegram, a broader community of tinkerers, builders and hackers!

Please do not use issues for support requests. If necessary, you can use our [Discussions](https://github.com/selfcustody/krux/discussions) to post your question here on GitHub.
