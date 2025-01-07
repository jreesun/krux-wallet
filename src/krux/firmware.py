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
import io
import os
import binascii
import hashlib
import time
import flash
from embit import ec
from .input import Input, BUTTON_PAGE, BUTTON_PAGE_PREV
from .metadata import SIGNER_PUBKEY
from .display import display
from .krux_settings import t
from .wdt import wdt
from .themes import theme

FLASH_SIZE = 2**24
MAX_FIRMWARE_SIZE = 0x300000

FIRMWARE_SLOT_1 = 0x00080000
FIRMWARE_SLOT_2 = 0x00390000
SPIFFS_ADDR = 0xD00000

MAIN_BOOT_CONFIG_SECTOR_ADDRESS = 0x00004000
BACKUP_BOOT_CONFIG_SECTOR_ADDRESS = 0x00005000

ERASE_BLOCK_SIZE = 0x1000

FLASH_IO_WAIT_TIME = 100


def find_active_firmware(sector):
    """Returns a tuple of the active firmware's configuration"""
    for i in range(8):
        app_entry = sector[i * 32 : i * 32 + 32]
        config_flags = int.from_bytes(app_entry[0:4], "big")
        active = config_flags & 0b1 == 0b1
        if not active:
            continue
        app_address = int.from_bytes(app_entry[4 : 4 + 4], "big")
        app_size = int.from_bytes(app_entry[8 : 8 + 4], "big")
        return app_address, app_size, i
    return None, None, None


def update_boot_config_sector(
    sector, entry_index, new_firmware_address, new_firmware_size
):
    """Updates the boot config sector in flash"""
    updated_sector = bytearray(sector)
    app_entry = updated_sector[entry_index * 32 : entry_index * 32 + 32]
    app_entry[0:4] = (0x5AA5D0C0 | 0b1101).to_bytes(4, "big")
    app_entry[4 : 4 + 4] = new_firmware_address.to_bytes(4, "big")
    app_entry[8 : 8 + 4] = new_firmware_size.to_bytes(4, "big")
    updated_sector[entry_index * 32 : entry_index * 32 + 32] = app_entry
    return bytes(updated_sector)


def write_data(
    pct_cb, address, data, data_size, chunk_size, header=False, sha_suffix=None
):
    """Writes data to the flash, optionally adding header and sha suffix for firmware"""
    buffer = bytearray(chunk_size)
    i = 0
    chunk_read = 0
    total_read = 0
    read_attempts = 0
    while True:
        wdt.feed()
        if sha_suffix is None:
            pct_cb(total_read / data_size)
            if total_read == data_size:
                break
        else:
            pct_cb(total_read / (data_size + len(sha_suffix)))
            if total_read == data_size + len(sha_suffix):
                break

        header_offset = 5 if header and i == 0 else 0
        chunk_size_after_header = chunk_size - header_offset

        num_read = 0
        if sha_suffix is not None and total_read >= data_size:
            sha_index = total_read - data_size
            num_read = len(sha_suffix[sha_index:])
            buffer[:num_read] = sha_suffix[sha_index:]
        else:
            read_bytes = data.read(chunk_size_after_header - chunk_read)
            num_read = len(read_bytes)
            buffer[chunk_read : chunk_read + num_read] = read_bytes
        total_read += num_read

        if not num_read and not chunk_read:
            if read_attempts < 5:
                read_attempts += 1
                continue
            raise ValueError("failed to read")

        chunk_read += num_read
        if num_read and chunk_read < chunk_size_after_header and total_read < data_size:
            continue

        if sha_suffix is not None and total_read >= data_size:
            sha_index = total_read - data_size
            remainder = min(
                chunk_size_after_header - chunk_read, len(sha_suffix[sha_index:])
            )
            buffer[chunk_read : chunk_read + remainder] = sha_suffix[
                sha_index : sha_index + remainder
            ]
            total_read += remainder
            chunk_read += remainder

        for j in range(chunk_size_after_header - chunk_read):
            buffer[chunk_read + j] = 0b0

        cur_address = i * chunk_size + address
        flash.erase(cur_address, chunk_size)
        time.sleep_ms(FLASH_IO_WAIT_TIME)
        if header and i == 0:
            flash.write(cur_address, b"\x00" + data_size.to_bytes(4, "little"))
            time.sleep_ms(FLASH_IO_WAIT_TIME)
        flash.write(cur_address + header_offset, buffer[:chunk_size_after_header])
        time.sleep_ms(FLASH_IO_WAIT_TIME)
        i += 1
        num_read = 0
        chunk_read = 0


def fsize(firmware_filename):
    """Returns the size of the firmware"""
    size = 0
    with open(firmware_filename, "rb", buffering=0) as file:
        while True:
            chunk = file.read(128)
            if not chunk:
                break
            size += len(chunk)
    return size


def sha256(firmware_filename, firmware_size=None):
    """Returns the sha256 hash of the firmware"""
    hasher = hashlib.sha256()
    # If firmware size is supplied, then we want a sha256 of the firmware with its header
    if firmware_size is not None:
        hasher.update(b"\x00" + firmware_size.to_bytes(4, "little"))
    with open(firmware_filename, "rb", buffering=0) as file:
        while True:
            chunk = file.read(128)
            if not chunk:
                break
            hasher.update(chunk)
    return hasher.digest()


def check_signature(pubkey, sig, file_hash):
    """Return if signature of the file_hash is valid for the pubkey"""

    try:
        # Parse, serialize, and reparse to ensure signature is compact prior to verification
        sig = ec.Signature.parse(ec.Signature.parse(sig).serialize())
        if not pubkey.verify(sig, file_hash):
            return False
    except:
        return False

    return True


def get_pubkey():
    """Construct the pubkey based on Krux metadata pubkey string"""

    try:
        return ec.PublicKey.from_string(SIGNER_PUBKEY)
    except:
        return None


def upgrade():
    """Installs new firmware from SD card"""

    firmware_path = ""
    try:
        firmware_filenames = list(
            filter(
                lambda filename: filename.startswith("firmware")
                and filename.endswith(".bin"),
                os.listdir("/sd"),
            )
        )
        firmware_filenames.sort(reverse=True)
        if not firmware_filenames:
            return False
        firmware_path = "/sd/" + firmware_filenames[0]
    except:
        return False

    inp = Input()

    def status_text(text):
        display.clear()
        display.draw_centered_text(text)

    status_text(t("New firmware detected.") + "\n\n" + t("Verifying.."))

    new_size = fsize(firmware_path)
    firmware_hash = sha256(firmware_path)
    firmware_with_header_hash = sha256(firmware_path, new_size)

    status_text(
        t("New firmware detected.")
        + "\n\n"
        + "SHA256:\n"
        + binascii.hexlify(firmware_hash).decode()
        + "\n\n\n\n"
        + t("Install?")
    )
    inp.buttons_active = True
    if inp.wait_for_button() in (BUTTON_PAGE, BUTTON_PAGE_PREV):
        display.clear()
        inp.wait_for_release()  # Wait for button release loading inputs on context
        return False

    if new_size > MAX_FIRMWARE_SIZE:
        display.flash_text(
            "Firmware exceeds max size: %d" % MAX_FIRMWARE_SIZE, theme.error_color
        )
        return False

    pubkey = get_pubkey()
    if pubkey is None:
        display.flash_text("Invalid public key", theme.error_color)
        return False

    sig = None
    try:
        with open(firmware_path + ".sig", "rb") as sig_file:
            sig = sig_file.read()
    except:
        display.flash_text(t("Missing signature file"), theme.error_color)
        return False

    if not check_signature(pubkey, sig, firmware_hash):
        display.flash_text(t("Bad signature"), theme.error_color)
        return False

    boot_config_sector = flash.read(MAIN_BOOT_CONFIG_SECTOR_ADDRESS, 4096)
    address, _, entry_index = find_active_firmware(boot_config_sector)
    if address is None:
        boot_config_sector = flash.read(BACKUP_BOOT_CONFIG_SECTOR_ADDRESS, 4096)
        address, _, entry_index = find_active_firmware(boot_config_sector)
        if address is None:
            display.flash_text("Invalid bootloader", theme.error_color)
            return False

    # Write new firmware to the opposite slot
    new_address = FIRMWARE_SLOT_2 if address == FIRMWARE_SLOT_1 else FIRMWARE_SLOT_1

    try:
        with open(firmware_path, "rb", buffering=0) as firmware_file:
            write_data(
                lambda pct: status_text(
                    t("Processing..") + "1/3" + "\n\n%d%%" % int(pct * 100)
                ),
                new_address,
                firmware_file,
                new_size,
                65536,
                True,
                firmware_with_header_hash,
            )

        write_data(
            lambda pct: status_text(
                t("Processing..") + "2/3" + "\n\n%d%%" % int(pct * 100)
            ),
            BACKUP_BOOT_CONFIG_SECTOR_ADDRESS,
            io.BytesIO(boot_config_sector),
            len(boot_config_sector),
            4096,
        )

        new_boot_config_sector = update_boot_config_sector(
            boot_config_sector, entry_index, new_address, new_size
        )
        write_data(
            lambda pct: status_text(
                t("Processing..") + "3/3" + "\n\n%d%%" % int(pct * 100)
            ),
            MAIN_BOOT_CONFIG_SECTOR_ADDRESS,
            io.BytesIO(new_boot_config_sector),
            len(new_boot_config_sector),
            4096,
        )
    except:
        display.flash_text("Error read/write data", theme.error_color)
        return False

    status_text(
        t("Upgrade complete.") + "\n" + t("Remove firmware files from SD Card?")
    )
    inp.buttons_active = True
    if not inp.wait_for_button() in (BUTTON_PAGE, BUTTON_PAGE_PREV):
        os.remove(firmware_path)
        os.remove(firmware_path + ".sig")

    display.flash_text(t("Shutting down.."))
    return True
