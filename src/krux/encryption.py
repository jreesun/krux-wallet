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

try:
    import ujson as json
except ImportError:
    import json
import hashlib
import ucryptolib
from .baseconv import base_encode, base_decode
from .sd_card import SDHandler
from .krux_settings import Settings, PBKDF2_HMAC_ECB, PBKDF2_HMAC_CBC, FLASH_PATH
from embit.wordlists.bip39 import WORDLIST


MNEMONICS_FILE = "seeds.json"
FLASH_PATH = "/" + FLASH_PATH + "/"

VERSION_MODE = {
    "AES-ECB": ucryptolib.MODE_ECB,
    "AES-CBC": ucryptolib.MODE_CBC,
    PBKDF2_HMAC_ECB: ucryptolib.MODE_ECB,
    PBKDF2_HMAC_CBC: ucryptolib.MODE_CBC,
}

VERSION_NUMBER = {
    "AES-ECB": PBKDF2_HMAC_ECB,
    "AES-CBC": PBKDF2_HMAC_CBC,
}

AES_BLOCK_SIZE = 16
QR_CODE_ITER_MULTIPLE = 10000


class AESCipher:
    """Helper for AES encrypt/decrypt"""

    def __init__(self, key, salt, iterations):
        self.key = hashlib.pbkdf2_hmac(
            "sha256", key.encode(), salt.encode(), iterations
        )

    def encrypt(self, raw, mode=ucryptolib.MODE_ECB, i_vector=None):
        """Encrypt using AES-ECB or AES-CBC and return the value encoded as base64"""
        data_bytes = raw.encode("latin-1") if isinstance(raw, str) else raw
        if i_vector:
            encryptor = ucryptolib.aes(self.key, mode, i_vector)
        else:
            encryptor = ucryptolib.aes(self.key, mode)
        encrypted = encryptor.encrypt(
            data_bytes + b"\x00" * ((16 - (len(data_bytes) % 16)) % 16)
        )
        if i_vector:
            encrypted = i_vector + encrypted
        return base_encode(encrypted, 64)

    def decrypt(self, encrypted, mode, i_vector=None):
        """Decrypt bytes and return the value decoded as string"""
        if i_vector:
            decryptor = ucryptolib.aes(self.key, mode, i_vector)
        else:
            decryptor = ucryptolib.aes(self.key, mode)
        load = decryptor.decrypt(encrypted).decode("utf-8")
        return load.replace("\x00", "")

    def decrypt_bytes(self, encrypted, mode, i_vector=None):
        """Decrypt and return value as bytes"""
        if i_vector:
            decryptor = ucryptolib.aes(self.key, mode, i_vector)
        else:
            decryptor = ucryptolib.aes(self.key, mode)
        return decryptor.decrypt(encrypted)


class MnemonicStorage:
    """Handler of stored encrypted seeds"""

    def __init__(self) -> None:
        self.stored = {}
        self.stored_sd = {}
        try:
            with SDHandler() as sd:
                self.stored_sd = json.loads(sd.read(MNEMONICS_FILE))
        except:
            pass
        try:
            with open(FLASH_PATH + MNEMONICS_FILE, "r") as f:
                self.stored = json.loads(f.read())
        except:
            pass

    def list_mnemonics(self, sd_card=False):
        """List all seeds stored on a file"""
        mnemonic_ids = []
        source = self.stored_sd if sd_card else self.stored
        for mnemonic_id in source:
            mnemonic_ids.append(mnemonic_id)
        return mnemonic_ids

    def decrypt(self, key, mnemonic_id, sd_card=False):
        """Decrypt a selected encrypted mnemonic from a file"""
        try:
            if sd_card:
                encrypted_data = self.stored_sd.get(mnemonic_id)["data"]
                iterations = self.stored_sd.get(mnemonic_id)["key_iterations"]
                version = self.stored_sd.get(mnemonic_id)["version"]
            else:
                encrypted_data = self.stored.get(mnemonic_id)["data"]
                iterations = self.stored.get(mnemonic_id)["key_iterations"]
                version = self.stored.get(mnemonic_id)["version"]
        except:
            return None
        data = base_decode(encrypted_data, 64)
        mode = VERSION_MODE[version]
        if mode == ucryptolib.MODE_ECB:
            encrypted_mnemonic = data
            i_vector = None
        else:
            encrypted_mnemonic = data[AES_BLOCK_SIZE:]
            i_vector = data[:AES_BLOCK_SIZE]
        decryptor = AESCipher(key, mnemonic_id, iterations)
        words = decryptor.decrypt(encrypted_mnemonic, mode, i_vector)
        return words

    def store_encrypted(self, key, mnemonic_id, mnemonic, sd_card=False, i_vector=None):
        """Saves the encrypted mnemonic on a file, returns True if successful"""
        encryptor = AESCipher(key, mnemonic_id, Settings().encryption.pbkdf2_iterations)
        mode = VERSION_MODE[Settings().encryption.version]
        encrypted = encryptor.encrypt(mnemonic, mode, i_vector).decode("utf-8")
        mnemonics = {}
        if sd_card:
            # load current MNEMONICS_FILE
            try:
                with SDHandler() as sd:
                    contents = sd.read(MNEMONICS_FILE)
                    orig_len = len(contents)
                    mnemonics = json.loads(contents)
            except:
                orig_len = 0

            # save the new MNEMONICS_FILE
            try:
                with SDHandler() as sd:
                    mnemonics[mnemonic_id] = {}
                    mnemonics[mnemonic_id]["version"] = VERSION_NUMBER[
                        Settings().encryption.version
                    ]
                    mnemonics[mnemonic_id][
                        "key_iterations"
                    ] = Settings().encryption.pbkdf2_iterations
                    mnemonics[mnemonic_id]["data"] = encrypted
                    contents = json.dumps(mnemonics)
                    # pad contents to orig_len to avoid abandoned bytes on sdcard
                    if len(contents) < orig_len:
                        contents += " " * (orig_len - len(contents))
                    sd.write(MNEMONICS_FILE, contents)
            except:
                return False
        else:
            try:
                # load current MNEMONICS_FILE
                with open(FLASH_PATH + MNEMONICS_FILE, "r") as f:
                    mnemonics = json.loads(f.read())
            except:
                pass
            try:
                # save the new MNEMONICS_FILE
                with open(FLASH_PATH + MNEMONICS_FILE, "w") as f:
                    mnemonics[mnemonic_id] = {}
                    mnemonics[mnemonic_id]["version"] = VERSION_NUMBER[
                        Settings().encryption.version
                    ]
                    mnemonics[mnemonic_id][
                        "key_iterations"
                    ] = Settings().encryption.pbkdf2_iterations
                    mnemonics[mnemonic_id]["data"] = encrypted
                    f.write(json.dumps(mnemonics))
            except:
                return False
        return True

    def del_mnemonic(self, mnemonic_id, sd_card=False):
        """Remove an entry from encrypted mnemonics file"""
        if sd_card:
            self.stored_sd.pop(mnemonic_id)
            with SDHandler() as sd:
                orig_len = len(sd.read(MNEMONICS_FILE))
                contents = json.dumps(self.stored_sd)
                # pad contents to orig_len to avoid abandoned bytes on sdcard
                if len(contents) < orig_len:
                    contents += " " * (orig_len - len(contents))
                sd.write(MNEMONICS_FILE, contents)
        else:
            self.stored.pop(mnemonic_id)
            with open(FLASH_PATH + MNEMONICS_FILE, "w") as f:
                f.write(json.dumps(self.stored))


class EncryptedQRCode:
    """Creates and decrypts encrypted mnemonic QR codes"""

    def __init__(self) -> None:
        self.mnemonic_id = None
        self.version = VERSION_NUMBER[Settings().encryption.version]
        self.iterations = Settings().encryption.pbkdf2_iterations
        self.encrypted_data = None

    def create(self, key, mnemonic_id, mnemonic, i_vector=None):
        """Joins necessary data and creates encrypted mnemonic QR codes"""
        name_lenght = len(mnemonic_id.encode())
        version = VERSION_NUMBER[Settings().encryption.version]
        ten_k_iterations = Settings().encryption.pbkdf2_iterations

        # Divide iterations by a Multiple(10,000) to save space
        ten_k_iterations //= QR_CODE_ITER_MULTIPLE

        # Add public data bytes
        qr_code_data = name_lenght.to_bytes(1, "big")
        qr_code_data += mnemonic_id.encode()
        qr_code_data += version.to_bytes(1, "big")
        qr_code_data += ten_k_iterations.to_bytes(3, "big")

        # Restore the iterations value assuring is a multiple of 10,000
        ten_k_iterations *= QR_CODE_ITER_MULTIPLE

        # Encrypted data
        encryptor = AESCipher(key, mnemonic_id, ten_k_iterations)
        mode = VERSION_MODE[Settings().encryption.version]
        words = mnemonic.split(" ")
        checksum_bits = 8 if len(words) == 24 else 4
        indexes = [WORDLIST.index(word) for word in words]
        bitstring = "".join(["{:0>11}".format(bin(index)[2:]) for index in indexes])[
            :-checksum_bits
        ]
        bytes_to_encrypt = int(bitstring, 2).to_bytes((len(bitstring) + 7) // 8, "big")
        bytes_to_encrypt += hashlib.sha256(bytes_to_encrypt).digest()[:16]
        base64_encrypted = encryptor.encrypt(bytes_to_encrypt, mode, i_vector)
        bytes_encrypted = base_decode(base64_encrypted, 64)

        # Add encrypted data bytes
        qr_code_data += bytes_encrypted

        return qr_code_data

    def public_data(self, data):
        """Parse and returns encrypted mnemonic QR codes public data"""
        mnemonic_info = "Encrypted QR Code:\n"
        try:
            id_lenght = int.from_bytes(data[:1], "big")
            self.mnemonic_id = data[1 : id_lenght + 1].decode("utf-8")
            mnemonic_info += "ID: " + self.mnemonic_id + "\n"
            self.version = int.from_bytes(data[id_lenght + 1 : id_lenght + 2], "big")
            version_name = [k for k, v in VERSION_NUMBER.items() if v == self.version][
                0
            ]
            mnemonic_info += "Version: " + version_name + "\n"
            self.iterations = int.from_bytes(data[id_lenght + 2 : id_lenght + 5], "big")
            self.iterations *= 10000
            mnemonic_info += "Key iter.: " + str(self.iterations)
        except:
            return None
        extra_bytes = id_lenght + 5  # 1(id lenght byte) + 1(version) + 3(iterations)
        if self.version == 1:
            extra_bytes += 16  # Initial Vector size
        extra_bytes += 16  # Encrypted QR checksum is always 16 bytes
        len_mnemonic_bytes = len(data) - extra_bytes
        if len_mnemonic_bytes not in (16, 32):
            return None
        self.encrypted_data = data[id_lenght + 5 :]
        return mnemonic_info

    def decrypt(self, key):
        """Decrypts encrypted mnemonic QR codes"""
        mode = VERSION_MODE[self.version]
        if mode == ucryptolib.MODE_ECB:
            encrypted_mnemonic_data = self.encrypted_data
            i_vector = None
        else:
            encrypted_mnemonic_data = self.encrypted_data[AES_BLOCK_SIZE:]
            i_vector = self.encrypted_data[:AES_BLOCK_SIZE]
        decryptor = AESCipher(key, self.mnemonic_id, self.iterations)
        decrypted_data = decryptor.decrypt_bytes(
            encrypted_mnemonic_data, mode, i_vector
        )
        mnemonic_data = decrypted_data[:-AES_BLOCK_SIZE]
        checksum = decrypted_data[-AES_BLOCK_SIZE:]
        # Data validation:
        if hashlib.sha256(mnemonic_data).digest()[:16] != checksum:
            return None
        return mnemonic_data
