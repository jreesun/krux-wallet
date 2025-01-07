# Tamper Detection Mechanism (Experimental)
Krux's tamper detection tool combines cryptographic hashes, a *Tamper Check Code (TC Code)*, and camera-generated entropy to create a tamper indicator that is unique to each device, represented by a memorable image and two sets of two words.

Before we get into details, let's start with some limitations and necessary prerequisites to allow the feature to work.

## Krux Security Model - Good Practices and Limitations

To secure your Krux device, always verify firmware authenticity before installation, particularly when flashing via USB.

### Firmware Verification Methods

- **Using OpenSSL Command-Line Tool:** Follow [from pre-built official release](../installing/from-pre-built-release.md/#verify-the-files) instructions to verify the firmware's signature manually. This method provides a high level of assurance but requires familiarity with command-line operations.

- **Using Krux-Installer:** Our [Krux-Installer GUI](../installing/from-gui/index.md) can facilitate this process by downloading our firmware from Github and verifying its signature. It also guides you through manual verification if desired. Just don't forget to verify the integrity of the Krux-Installer as well.


### Recommendations

- **Build from Source:** Consider building the firmware [from source code](../installing/from-source.md) and verifying its [reproducibility](../installing/from-source.md/#reproducibility) for maximum assurance.

- **Use SD Card for Updates:** After the initial flash through USB, perform subsequent [updates via the SD card](../features/sd-card-update.md). This keeps your device air-gapped and allows the existing firmware to verify the new one before installation.

Note: The effectiveness of *TC Flash Hash* tamper detection feature relies on running legitimate, uncompromised firmware and safely protecting your *TC Code*.

### Setting Up Tamper Detection
To help ensure the integrity of your device’s firmware, you can set up tamper detection tools, called *Tamper Check (TC) Flash Hash* and a *Tamper Check (TC) Code*. The *TC Code* must be at least six characters long, and for best security, should include a mix of letters, numbers, and special characters. You can create or change your *TC Code* by going to `Settings -> Security -> Tamper Check Code`.

Ensure that your *TC Code* remains confidential and challenging to guess, as its security directly influences the effectiveness of your tamper detection.

Once configured, your *TC Code* will be required to run *TC Flash Hash*. You can run TC Flash Hash at any time by navigating to `Tools -> Flash Tools -> TC Flash Hash`. Alternatively, enable automatic checks on every boot by selecting `Settings -> Security -> TC Flash Hash at Boot`.

When you enable the *TC Flash Hash at Boot* feature, the device will require you to enter your TC Code at each startup, ensuring routine integrity checks. This also prevents device usage unless the correct code is entered.

*TC Flash Hash* produces a unique visual and verbal signature (an image and two sets of words) that helps you instantly recognize unauthorized changes. See below for details on how it works and what to expect from its output.

### How Krux Tamper Detection Works

## Tamper Check Code (TC Code)
Before being stored in the device’s flash, the *TC Code* is hashed together with the K210 chip’s unique ID and stretched using PBKDF2. This ensures the *TC Code* is not retrievable via a flash dump and can only be brute-forced outside the device if the attacker also has access to the device’s unique ID (UID). By allowing letters, special characters, and running 100k iterations of PBKDF2, brute-forcing the *TC Code* from dumped data becomes more time-consuming and resource-intensive.

### Enhancing Tamper Detection
After setting the *TC Code*, you are prompted to fill empty flash memory blocks with random entropy from the camera. This process ensures that attackers cannot exploit unused memory space.

## Tamper Check Flash Hash (TC Flash Hash) - A Tamper Detection Tool

The *TC Flash Hash* tool enables you to verify if the device's internal flash memory content has been altered. This tool generates a unique image and two sets of two tamper detection words based on a hash of your *TC Code*, the device's UID, and its internal flash content. The flash memory is divided into two regions:

- **Firmware Region:** The area only filled with firmware code. It generates the memorable image and the first set of two words.

- **User's Region:** The area used to stored encrypted mnemonics, settings and TC Code. It generates the last set of two words.

<div style="text-align: center;">
    <img src="../../../img/maixpy_amigo/tc-flash-hash-150.png" alt="TC Flash Hash amigo">
    <img src="../../../img/maixpy_m5stickv/tc-flash-hash-125.png" alt="TC Flash Hash m5stickv">
</div>

*Example: The red symbol and words 'debate lunar' represent the firmware region, while 'renew great' user's region.*

Any change in the flash content results in a different image and words:

- **Firmware Changes:** Alterations in the firmware region, including the bootloader, change the image and the first set of two words.

- **User's Data Changes:** Changes in the user's region, such as new settings or stored mnemonics, change the last set of two words.

- ***TC Code* Changes:** Replacing the *TC Code* alters the image and all sets of words.

### Filling Empty Flash Memory Blocks

Use this to enhance tamper detection. Krux performs a memory sweep while capturing a live feed from the camera. Whenever an empty block is found in the flash memory, it uses the data from the image to fill these empty spaces with rich, random entropy. It estimates the image's entropy by evaluating its color variance waiting until a minimum threshold is met. 

### Ensuring Tamper Detection

The *TC Flash Hash* function securely hashes the combination of the *TC Code*, device's UID, and flash memory contents. The hash properties ensure that without knowing these three elements, an attacker will not be able to reproduce the *TC Flash Hash* results.

## Executing *TC Flash Hash*

After setting a *TC Code* user can use the *TC Flash Hash* feature, available in `Tools -> Flash Tools -> TC Flash Hash`.

By navigating to `Settings -> Security -> TC Flash Hash at Boot`, users can set Krux to always require *TC Flash Hash* verification after device is turned on. If a wrong *TC Code* is typed at boot, the device will turn off. Nothing else will happen if the wrong *TC Code* is entered multiple times. As *TC Code* verification data is stored in the user's region of memory, the requirement to type at boot is disabled if the user [erases user's data](../features/tools.md/#erase-users-data) or [wipe device](../installing/from-gui/usage.md/#wipe-device). Flashing an older firmware version, prior to *TC Flash Hash* support, will also disable this feature.

## Potential Attack Scenarios and Their Mitigation
### Challenge for an Attacker

An attacker faces major challenges in replacing the firmware:

- **Lack of Original Flash Data:** Without the exact original flash content, attackers cannot reproduce the correct hash.

- **Sequential Hash Dependency:** The hash function processes data sequentially (*TC Code*, device's UID, and flash memory contents), preventing the attacker from injecting or rearranging data to produce the same hash.

- **One-Way Hash Functions:** Cryptographic hash functions like SHA-256 are one-way, making it infeasible to reverse-engineer or manipulate the hash without the original inputs.

### Why Tampered Firmware Cannot Bypass Verification

- **Cannot Reconstruct the Hash:** Without the original flash data, attackers cannot generate the correct hash, even if they know the device's UID and the *TC Code* (after the user enters it).

- **Hash Sensitivity:** Any alteration in the flash content changes the hash output, which will be evident through a different image and words.

- **Entropy Filling:** Filling empty flash blocks with camera-generated entropy leaves no space for malicious code and any changes to these blocks will alter the hash.

### Possible Attack Strategies and Failures

- **Precomputing Hashes:** The attacker cannot precompute the correct hash without the *TC Code*, device's UID, and exact contents of the flash memory.

- **Storing Hashes:** Storing `hash(flash_content)` is ineffective because the overall hash depends on the sequential combination of *TC Code*, device's UID, and the flash data.

- **Inserting Malicious Code:** Attempting to insert code into empty spaces fails because after the entropy filling process, the hash verification will detect any changes.

- **Using an SD Card to Store a Copy of Original Flash Content:** An attacker could extract an exact copy of the flash contents to an SD card and subsequently install malicious firmware. This firmware could read the device's UID and the *TC Code* (after the user enters it), then hash the content of the SD card instead of the flash memory. Although this would make the verification process slower, it introduces a potential security risk. To mitigate this vulnerability, it is advisable to avoid performing verifications while an SD card is inserted. 

## Conclusion

The *TC Flash Hash* tool significantly enhances security by making it infeasible for attackers to tamper with firmware without being detected. By combining *TC Code* hashing, filling empty memory with random entropy, and verification of the the unique image and set of words, Krux allows the detection of any tamper attempts.

Note: The strength of this defense strategy depends on maintaining a strong, confidential *TC Code*, removing the SD card before running *TC Flash Hash* and following usual security and privacy practices.
