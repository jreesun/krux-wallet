## Introduction

There are many possible security layers one could add to protect a wallet’s private key. Adding a BIP39 passphrase to the mnemonic is the most common method. Encrypting a BIP39 mnemonic has a similar use case as the BIP39 passphrase, but the user experience may differ depending on the implementation. The main difference between BIP39 passphrases and Krux’s encrypted mnemonic implementation is that when users type the wrong key, encrypted mnemonics will return an error instead of loading a different wallet, as BIP39 passphrases do. This difference may be desired or not. The implementation also has the convenience of storing a mnemonic ID together with the stored or QR code encrypted mnemonics. Mnemonic encryption, with its own key, can be used together with BIP39 passphrase as an extra security layer.

We use standard AES encryption modes ECB and CBC:

### AES-ECB

ECB (Electronic Codebook) is a simpler method where encryption data blocks are encrypted individually. This mode is faster and simpler to encrypt, resulting in QR codes with lower density and easier to transcribe. It is generally considered less secure than CBC because it does not provide data chaining, meaning identical plaintext blocks will produce identical ciphertext blocks, making it vulnerable to pattern analysis. However, in Krux's implementation, only one or two binary data blocks are encrypted, so there will be no patterns, and the lack of chaining is not as relevant as it would be for larger files, plain text, or media.

### AES-CBC

CBC (Cipher-block Chaining) is considered more secure. In the first data block, an initialization vector (IV) is used to add random data to the encryption. The encryption of subsequent blocks depends on the data from previous blocks, characterizing chaining. The tradeoff is that the encryption process will take longer because a snapshot will be needed to generate the IV. This IV will be stored together with encrypted data, making encrypted QR codes denser and harder to transcribe.

#### CBC Encryption IV

The Initial Vector (IV) will be generated from a snapshot taken with the camera. The IV is a fixed-size input value used in the first block of the encryption process. It adds randomness to the encryption, ensuring that data encrypted with the same key will produce different ciphertexts each time. The IV is not secret and will be transmitted along with the ciphertext. However, like any nonce, it should not be reused to maintain security.

### PBKDF2 Iterations
When you enter the encryption key, it is not directly used to encrypt your data. In order to protect against brute force attacks, the key is derived multiple times using hashing functions. PBKDF2 (Password-Based Key Derivation Function) iterations refer to the number of derivations that will be performed over your key prior to encrypting/decrypting your mnemonic.


## Encrypted QR Codes Data and Parsing
In search of efficiency and smaller QR codes, all data is converted to bytes and organized like a Bitcoin transaction, with variable and fixed length fields. The following data is present on the QR code:

| ID length (1) | ID (2) | Version (3) | Key Derivations (4) | IV (5) | Encrypted Mnemonic (6) | Validation Block (7) |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 1 Byte | Variable | 1 Byte | 3 Bytes | 16 Bytes <br>(optional) | 16 Bytes (12 words) <br>32 Bytes (24 words) | 16 Bytes |

* **Visible data** (1 to 4):
    * **(1)** Mnemonic ID length (1 Byte).
    * **(2)** Mnemonic ID (variable lenght): Custom ID or wallet fingerprint.
    * **(3)** Version (1 Byte): Version of encryption method, currently two are available:
        - 0: AES-ECB-PBKDF2: Electronic Codebook with PBKDF2 key derivation.
        - 1: AES-CBC-PBKDF2: Cypher Block Chaining with PBKDF2 key derivation.
    * **(4)** Key derivation iterations (3 Bytes): Number of PBKDF2 key derivations times 10,000.
* **Cipher data** (5 to 7):
    * **(5)** IV (16 Bytes-optional): Initial vector for AES-CBC encryption, possibility to be nonce for future 	AES-CTR or other encryption methods.
    * **(6)** Encrypted Mnemonic (16 Bytes - 12 words, 32 Bytes - 24 words): Mnemonic ciphertext.
    * **(7)** Validation block (16 Bytes): Currently using first 16 bytes of sha256 of the mnemonic bytes as checksum, could be used in future to store AES-AEX validation tag.

## Considerations
Storage of encrypted mnemonics on the device or SD cards are meant for convenience only and should not be considered a form of backup. Always make a physical backup of your keys that is independent from electronic devices and test recovering your wallet from this backup before you send funds to it. Flash storage can degrade over time and may be subject to permanent damage, resulting in the loss of stored information.

Remember that the stored encrypted mnemonic is protected by the key you defined to encrypt it. If the defined [key is weak](https://www.hivesystems.com/blog/are-your-passwords-in-the-green), your encrypted mnemonic will **not be protected**. If you have stored a mnemonic with funds in the device's internal flash memory using a [weak key](https://www.hivesystems.com/blog/are-your-passwords-in-the-green), the best way to undo this is to [erase user's data](tools.md/#erase-users-data).