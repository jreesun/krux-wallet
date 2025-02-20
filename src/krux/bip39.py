# Mnemonic convertion to seed and to/from bytes
# pylint: disable=W0102

import hashlib
from embit.wordlists.bip39 import WORDLIST

WORDINDEX = {word: i for i, word in enumerate(WORDLIST)}


def entropy_checksum(entropy: bytes, checksum_length_bits: int = 4):
    """
    Computes checksum for the given entropy
    """
    h = hashlib.sha256(entropy).digest()
    return int(h[0]) >> (8 - checksum_length_bits)


def k_mnemonic_bytes(mnemonic: str, ignore_checksum: bool = False, wordlist=WORDLIST):
    """
    Verifies the mnemonic checksum and returns it in bytes
    Equivalent to embit.bip39.mnemonic_to_bytes
    """
    words = mnemonic.strip().split()
    if len(words) % 3 != 0 or not 12 <= len(words) <= 24:
        raise ValueError("Invalid recovery phrase")

    accumulator = 0
    try:
        if wordlist is WORDLIST:
            for word in words:
                accumulator = (accumulator << 11) + WORDINDEX[word]
        else:
            for word in words:
                accumulator = (accumulator << 11) + wordlist.index(word)
    except Exception:
        raise ValueError("Word '%s' is not in the dictionary" % word)

    entropy_length_bits = len(words) * 11 // 33 * 32
    checksum_length_bits = len(words) * 11 // 33
    checksum = accumulator & (2**checksum_length_bits - 1)
    accumulator >>= checksum_length_bits
    data = accumulator.to_bytes(entropy_length_bits // 8, "big")
    if ignore_checksum:
        return data

    if checksum != entropy_checksum(data, checksum_length_bits):
        raise ValueError("Checksum verification failed")
    return data


def k_mnemonic_is_valid(mnemonic: str, wordlist=WORDLIST):
    """
    Checks if mnemonic is valid (checksum and words)
    Equivalent to embit.bip39.mnemonic_is_valid
    """
    try:
        k_mnemonic_bytes(mnemonic, wordlist=wordlist)
        return True
    except:
        return False
