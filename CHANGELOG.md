# Changelog 25.02.0 - February 2025

### Taproot and WSH Miniscript support

- Provides an indented visualization of Miniscript for easier inspection.
- Includes policy and cosigner verification.
- Supports custom derivations.
- Detects unspendable internal keys in Taproot.
- Contains several UI and settings modifications.

### More Intuitive Tamper Check
The Tamper Check Flash Hash now appears immediately after the Tamper Check code is created, clarifying its purpose and expected output.

### More Camera Modes
A zoomed camera mode is available for all cameras, and an anti-glare mode has been added to the GC0328 camera.

### Display Customization Options
Display orientation on Yahboom and WonderMV devices can now be flipped.

### SD Card PSBT Signing Preserves All Fields
When signing via SD cards, all fields in a PSBT—including signatures from other keys—are preserved. This facilitates workflows across multiple devices and locations by allowing a single PSBT file to be sequentially signed by different devices.

### Other Bug Fixes and Optimizations
- Stored mnemonics are now sorted alphabetically.
- Flash Map drawing errors have been corrected.
- Address scanning for Blue Wallet has been fixed following its export format change.
- The use of “h” to indicate hardened derivation path nodes has been standardized.
- A faster algorithm for double mnemonic calculation has been introduced.
- PSBT change detection has been made more restrictive.


# Changelog 24.11.1 - November 2024

### Security Fix
This release addresses a vulnerability affecting AES-CBC encrypted mnemonics stored on flash storage, SD cards, and QR codes. Due to an implementation error, the Initialization Vector (IV) in our CBC encryption, which used camera-generated entropy, was not being correctly utilized, which meant it did not provide the intended additional entropy.

# Changelog 24.11.0 - November 2024

### Tamper Check Flash Hash and Tamper Check Code (Experimental)
The *Tamper Check Flash Hash* (TC Flash Hash) feature verifies the integrity of the device's flash memory by generating a unique tamper indicator that relies on hash properties. After setting up a *Tamper Check Code* (TC Code), this check can be performed at every boot or manually via `Tools -> Flash Tools`. The TC Code is a key component, required to execute the verification and detect unauthorized changes to the device's memory. Users can also fill unused memory blocks with camera-generated entropy to further mitigate tampering attempts.

### Flash Map
*Flash Map* is an auxiliary tool that allows users to visualize the regions of the device's memory that are empty. This helps users verify the results of actions such as:

- Wiping the device's memory
- Erasing the user's area
- Saving settings and encrypted mnemonics
- Filling empty blocks with camera-generated entropy

### Japanese Translation
Japanese translation has been added.

### BIP85: Allow Export Base64 Passwords
In  addition to BIP39 Mnemonics, users can now derive Base64 passwords from their keys. These passwords, which can be used in standard logins, can be noted down, saved to an SD card, or exported as a QR code.

### Vulnerability Fix: Block Import of Python Modules from SD Card
A feature of MicroPython, commonly used for general-purpose development, is the ability to run Python code directly from an SD card. However, with the recent implementation of tamper detection tools, this behavior is now considered a vulnerability. It was discovered that MicroPython would prioritize importing `.pyc` (Python frozen modules) from an SD card before checking the internal flash, which could be exploited to run unintended code from the SD card. To address this, a block has been implemented in MicroPython to prevent running any code from the SD card, enhancing the overall security of the device.

### Add Compatibility to Partial Text Mnemonic QR Codes
Partial Text Mnemonic QR Codes, like Coldcard's backups, where mnemonics words are cropped and contain only the first 3 or 4 letters, are now auto-completed and loaded.

### Multi-keypad Position Indicator
An indicator has been added to the bottom of keypads to help users identify the keypad index while swiping between them.

### WonderMV Simulator
Computer simulator for WonderMV device has been added.

### Krux Ethos
Guidelines have been created to assist with decision-making regarding the Krux project's interactions with contributors, users, and businesses that may create products or services related to Krux.

### Minor Bugfixes and Refactors
Several code improvements for better reliability and efficiency.

# Changelog 24.09.1 - September 26, 2024

### Fix Camera Orientation on Cube
Fix for the camera, that was being started upside-down on Maix Cube devices 


# Changelog 24.09.0 - September 25, 2024

### New Device Support: WonderMV
Manufactured by HiWonder, the WonderMV is similar to Yahboom K210 Module, with a few differences, including a metal enclosure, USB-C port, and screen backlight control.

### Added Support for East Asian Languages - Korean and Simplified Chinese
After implementing low-level support for different glyph form factors, we were finally able to introduce the long-awaited Korean language translation. Simplified Chinese support followed shortly thereafter.

### Faster PSBT Scanning
Reduced the time required to scan larger PSBTs by optimizing processing speed.

### Improved QR Code Scanning
Enhanced scan success rates in challenging conditions, such as reduced focus or scanning from greater distances.

### UI Standardization
The positions of "Yes" and "No" in prompts have been inverted to standardize the UI. Affirmative actions, such as "Yes," "Go," and "Proceed," will now be positioned on the right, while "No," "Esc," and "Back" will be on the left.

### Enhanced Scanning Progress Bars
QR code progress bars now provide more detailed information. For UR PSBTs, the progress bar indicates when a valid frame is captured, while for BBQR, it displays the index or position of the last successfully scanned frame.

### Mnemoniocs Editor - Loading Mnemonics
When manually loading an existing mnemonic, you can now correct typos and mistakes during the review stage by simply tapping or navigating to the incorrect words. The checksum word will be highlighted in red if the entered mnemonic is invalid to help detect eventual problems.

### Mnemonics Editor - New Mnemonic
When generating new mnemonics through dice rolls or camera images, you can now modify the entropy by changing some of the mnemonic words. The final word will dynamically adjust to always produce a valid checksum.

### Support for Scanning Various Binary Grid Formats
In addition to TinySeed, the camera can now scan and load mnemonics from equivalent formats, such as OneKey KeyTag, or even generic binary grids, like spreadsheets with colored, squared cells.

### Message Signing Using SD cards
Recently released in Sparrow, the SD card message signing workflow is now supported.

### Generate Double Mnemonics from Camera
When generating a new mnemonic using the camera, users can now choose to create a "Double Mnemonic," in addition to the standard 12 and 24-word options. This feature generates a 24-word mnemonic that, when split in half, forms two valid 12-word mnemonics.

### Increased Valid Touch Surface
To improve touch accuracy, especially on small touchscreens, the touch surface area of buttons has been increased to make better use of the available screen space.

### Add Account Descriptor Type Support 
Krux now accepts urtype.Account type QR code descriptors.

### Enhanced File Exploring
File explorer now better differentiate files from folders.

### Camera Adjustments for Yahboom and WonderMV
Sensitivity and exposure adjustments were made to the GC2145 sensor, enhancing the scanning success rate for Yahboom and WonderMV devices.

### About Shows Board Type
Ensure you flashed the correct firmware for your device consulting the "About" menu item.

### Simplified Translations
Messages and terms were simplified to reduce firmware size and maintenance.

### Bugfix - Signing Messages with ":" Character
Fixed an issue where signing messages containing the ":" character would result in invalid signatures when signing at addresses.

### Bugfix - Import of Base64 Encoded PSBTs from SD Card
Fixed an issue where base64 encoded PSBTs imported from an SD card were not correctly detected and parsed.

### Translation Removed: Polish
Polish translation was removed due to the lack of maintainers and known users.

### Code Refactor and Optimizations
Several optimizations to increase performance and code quality.

# Changelog 24.07.0 - July 15, 2024

### Maix Cube Support
The Maix Cube now has its first official release. This affordable and compact cube-shaped device, equipped with a built-in battery, is an excellent choice for those seeking a discreet option.

### Frozen Code - Speed and Security Improvement
Krux now runs cross-compiled (frozen) Python code instead of real-time compiled code. The Python real-time compiler and REPL have been disabled.

### More Single-sig Script Types Support
Beyond Native Segwit, users can now load Legacy, Nested Segwit, and Taproot script type wallets.

### Accounts Support
Users can now use custom account derivation indexes.

### Wallet Customization Options
New workflow to load wallets, faster for default settings and with more options when custom settings are needed. Wallet's network, script type, single/multisig, and account can be changed during and after loading a wallet.

### BIP85 Support
Generate, export, and load BIP85 child mnemonics.

### Wallet Sans Key
Krux now has a tool to load a trusted wallet descriptor to view addresses without the need for private keys.

### Add BBQr Support
Scan and export PSBTs and wallet descriptors in the compact and efficient BBQr format.

### Update Embit
Embit updated to 0.8.

### Auto Shutdown - Security and Battery Saving Feature
The device will automatically shut down at a configurable time if left on.

### Hide Mnemonics - Security Feature
Disable backup tools and hide private key data when a wallet is loaded.

### PSBT Path Mismatch
Detect and warn the user if the PSBT path differs from the loaded wallet's path. This is useful for users who use multiple script types with the same key, ensuring they use the correct account when sending transactions.

### Show Multisig PSBT Policy When Descriptor is Not Loaded
Ensure you are signing for the correct multisig setup by inspecting PSBT's fingerprints if the wallet descriptor is not loaded. If the descriptor is loaded, verification is done by Krux.

### Status Bar Shows Loaded Fingerprint
The loaded key's fingerprint is now shown in the status bar.

### Fee Percentage of Transaction
Show the transaction's fee as a proportion of the transaction cost, warning if it is greater than 10%.

### Sats/vB
PSBT now displays an accurate estimation of the transaction’s feerate.

### Brightness Control for Maix Cube and M5stickV
Adjust backlight intensity for better viewing and scanning from your Cube or M5stickV.

### Fast Forward for Buttons
Hold the NEXT or PREVIOUS buttons when navigating among letters while typing text to fast forward or backward.

### Add Display Settings for Maix Amigo
Add more display settings for Amigo to allow different display models to work properly.

### Faster Address Scanning and Exploring
The time to scan or display wallet addresses is now less than half compared to the previous version.

### Sign PSBTs Without Fingerprints
Krux will now sign PSBTs even if a fingerprint is not properly set on the coordinator. Krux will still warn the user to set it correctly or use Krux-exported public keys to set their coordinators.

### Dice Rolls Pattern Detection
Krux warns the user if it suspects there are patterns within the actual rolls

### Optimized SD Card Signing
Better suited for large transactions, SD card signing is now more RAM efficient, allowing transactions with +100 inputs to be signed in less than a minute.

### Stand Alone Verifiable Signed PSBTs
As required in BIP174, signed PSBT QR codes and SD card files now contain all the required data to verify the signatures without needing the original, unsigned PSBT.

### Camera Optimizations for Yahboom (ver:1.1) With GC2145 Camera
Recent Yahboom K210 devices (ver:1.1) come with the GC2145 camera instead of the OV2640 (ver:1.0). Optimizations and features, such as anti-glare, have been added for the new camera.

### Yahboom and Cube Devices Added to Simulator
Simulator can now run as M5stickV, Amigo, Dock, Yahboom, and Cube.

### Files sorted in SD file explorer
The SD file explorer now sorts files in ascending order, showing directories first.

### Receive or change address now starts with the index 0
Address explorer now shows receive and change address starting at index 0 instead of number 1.

### Other Small Fixes and Code Optimizations
Bugfixes, optimizations and code refactoring.

# Changelog 24.03.0 - March 12, 2024

## Changes

### Wipe Device
Option on tools to wipe the device, permanently removing settings and stored encrypted mnemonics by erasing every single bit of user's flash space.

### Better Deletion of Mnemonics Stored on SD card
When deleting an encrypted mnemonic from an SD card, Krux will now overwrite the memory area making it impossible to recover the previously stored data.

### Save and Load Wallet Output Descriptor from SD card
Create or load from a wallet output descriptor file on an SD card. The backup file format is compatible with most coordinators.

### Sign Messages at a Derived Bitcoin address
Sign messages from Sparrow and Specter, via QR code, also attesting a Bitcoin address belongs to you.

### Reproducible Builds
To enhance the reproducibility of firmware builds, random variables such as file write timestamps have been removed from the build process. As a result, builds from developers' computers, those built within GitHub Actions from published code, and those you compile locally are more likely to be identical and have the same hash checksum as the official and beta releases. This change ensures greater consistency and traceability across all builds.

### Add Entropy Quality Estimation for Mnemonic Creation.
Entropy quality estimators, like Shannon's entropy, were added to mnemonic generation through dice rolls and camera snapshot.

### IRQ Interfaces
Button and touch presses are now detected by the application through IO interrupts. Meaning inputs events will be registered and handled even if they happened when other tasks were being executed by the processor, resulting in a better UX.

### Restore Default Settings
Option to restore the device's settings to its factory state.

### Optimized Settings Storage
Device's storage is now used more efficiently, data is stored less frequently, only in case a setting is changed from defaults.

### Amigo's Power Manager Enhancements
The power management behavior for the Amigo device has been standardized. Previously, some devices would not wake up from shutdown or sleep mode. Now, these devices will fully shut down when the shutdown option is selected from the menu, and they will always power on when the power button is pressed for 1 second.

### GUI Enhancements
Icons, information text boxes, and rounded shapes are now present at the GUI.

### Mnemonic Numbers
To match the input options, export mnemonics as decimal, hexadecimal, or octal numbers. When loading from numbers, a new numbers confirmation screen was added.

### Optimized QR codes
QR codes rendering is faster and uses less RAM.

### Export QR Codes as Images to SD Card
Some QR codes can be exported as images to SD card.

### Screensaver
Optional screensaver to reduce pixels' burn-in and grab the attention of the user when the device is left powered on.

### Addresses Exploring
More receive and change addresses per page are shown on bigger screens.

### Update Embit to version 0.7
Use the latest Embit release.

### Maix Dock Simulator
Now Krux PC simulator can also run in Maix Dock mode, mimicking appearance and characteristics of the most DIY Krux device.

### New Compatible Device - Yahboom
The Yahboom Aimotion K210 module, a compact touchscreen device, now has its first official firmware release.

### Join Amigo IPS and Amigo TFT firmwares
Users will be able to flash a single firmware and change display settings if their device was shipped with a display different from standard TFT.

### Other Small Fixes and Code Optimizations
Many other small fixes and optimizations under the hood.

# Version 23.09.1 - November 18, 2023
This release contain bugfixes:

Encrypted Mnemonic QR codes would fail to decrypt if PBKDF2 iterations settings was changed to non multiple of 10,000.

QR code transcription helpers that highlight regions could crash on edges of some QR code sizes.

Address navigation "previous" menu option wouldn't show correct number.

# Version 23.09.0 - September 12, 2023
After a long year, new features are finally coming out of beta and making their way into a stable release. Also @jreesun appointed @odudex as the new lead maintainer of the project.

## Changes

### Battery Indicator
Check battery status of M5stickV or Maix Amigo on top right of the screen.

### New Mnemonic From Camera
Use camera as a source of entropy to quickly create a mnemonic.

### Tiny Seed - Export, Print, Punch, Manually Load or Scan
Import and export a binary representation of your mnemonic, in a format popularized by Tiny Seed metal plates. BIP39 mnemonic words number, ranging from 1 to 2048 are punched in binary format on a rectangular grid.
Krux will automatically convert a mnemonic to Tiny Seed format allowing to print or transcript it. You can also load a tiny seed toggling word bits on screen, or make use of machine vision capabilities of K210 chip to directly scan a Tiny Seed mnemonic backup stored on metal or paper.

### Stackbit - Import and Export
Without needing tools, guides or dictionaries, import and export another metal plate backup format, where each of the four digits of the word's number is a sum of marked (punched) numbers 1,2,4 and 8.

### Enter Mnemonic as Word Numbers - Hex and Octal formats
Also available in some metal plate backup formats, you could load your mnemonic words from its decimal BIP39 word number (1-2048), now you can also load from its hexadecimal(0x1-0x800) or octal(01-04000) word number.

### Encryption and Storage
Conveniently store your mnemonics on device's internal flash memory or removable SD card, protecting them with encryption. It is now possible to export encrypted QR codes too.

### Addresses
Beyond verifying your wallet's receive addresses, you can now also list, export and print receive and change addresses.

### SD Card Hot plugging
SD cards can now be inserted and removed at any time, making it easier to use it for signing transactions, messages and storing encrypted mnemonics.

### Transcript Tools for QR codes
Different visualization modes which make it easier to transcript QR codes.

### Transaction Details
When signing a transaction, more information is presented, ensuring that the user sees all details before signing.

### Tools
#### Check SD Card
Check if the SD card is detected and explore its content.

#### Delete Mnemonic
Delete any stored encrypted mnemonic, on device's internal flash memory or SD card.

#### Print Test QR
Quickly print a test QR code to check and optimize your printer setup.

#### Create QR Code
Enter a text input to create, print or transcript a QR code that can be later used as an encryption key or as a passphrase.

### Themes
Choose your color theme according to your preference.

### Thermal Printing and CNC
More mnemonic export formats and tools to create and print generic QR codes to be used as passphrases or encryption keys. You can also export QR codes to gcode files and save them in SD cards, allowing you to machine them GRBL compatible CNCs without the need of computers and CAD tools.

### More Settings
#### Persist
Choose where you want to store your settings, on internal flash memory or SD card.

#### Touchscreen
If your device has touchscreen you can change the touch detection threshold.

### Languages
Dutch translations were added.

### UI Tweaks
Small changes to optimize user experience.

### Under the Hood
Small bugfixes, optimizations and code refactoring, targeting better compatibility with coordinator softwares, faster boot and better RAM management.


# Version 22.08.2 - September 13, 2022

This patch release reverts the zpub QR code format, once again including key origin derivation info which is necessary for BlueWallet to use when preparing PSBTs for signing with single-key wallets.

It is recommended to update to this version if you are using a single-key "Imported Watch-only" wallet with BlueWallet and are seeing a "cannot sign" error message when trying to send an outgoing transaction. If so, please do the following:

1. Upgrade Krux to this new release
2. Delete the affected wallet in BlueWallet (funds are safu as long as you have your mnemonic)
3. Create a new wallet in BlueWallet by importing from the new zpub QR code that Krux now displays.
4. Open the wallet in BlueWallet and pull down to fetch the old wallet's transaction history.
5. Create a new outgoing transaction and scan the QR code with Krux.
6. Krux should display the tx information and allow you to sign.
7. Display the signed QR back to BlueWallet.
8. Broadcast!

# Version 22.08.1 - August 11, 2022

This release is to fix a bug that would have prevented Amigos from performing airgapped upgrades to the next release.

# Version 22.08.0 - August 10, 2022

This latest version of Krux is brought to you by @odudex, who tirelessly worked for months to get Krux working on three new devices: the Maix Amigo, Maix Bit, and Maix Dock. Thank you for all your hard work! 

Many other improvements to Krux were made along the way which will be listed below. 

Enjoy!

## Installing
For instructions on how to install this release, please follow the *Getting Started* guide on [https://selfcustody.github.io/krux/](https://selfcustody.github.io/krux/).

To perform an airgapped upgrade (with a microSD card) from a previous signed release, please follow the directions here: [https://selfcustody.github.io/krux/getting-started/installing/#upgrade-via-microsd-card](https://selfcustody.github.io/krux/getting-started/installing/#upgrade-via-microsd-card)

## Changes
### ¡Three Amigos!
Krux now supports three new devices: Maix Amigo, Maix Bit, and Maix Dock. The Amigo is an all-in-one device with a touchscreen display, while the Dock and Bit are more DIY-focused kits where some assembly is required.
 
### New touchscreen UI + UX enhancements
Along with being usable on multiple devices now, Krux also has native touchscreen support and many refinements to its UI to make better use of the screen space it has. More work has gone into improving UX including the ability to escape out of the mnemonic loading or creation screens at any point.

### Built-in translations + Portuguese
Krux now includes translations in the firmware due to using a more space-efficient font format. With this change, the rendering issues with Vietnamese characters have also been fixed. A new Portuguese translation has been added.

### Amigo support added to Krux Simulator
The Krux Simulator, which lets you simulate on your PC what it would be like to run Krux on a device, was updated to support the Amigo. There is also now a PC option if you want to run Krux "natively" on your PC (**NOTE**: This is a toy for fun and is *not recommended* for real usage).

### CompactSeedQR support
Support for scanning SeedSigner’s newer "CompactSeedQR" QR codes

### BIP39 passphrases
Support has been added for BIP39 passphrases. After loading a mnemonic, you will be asked if you want to "Add a passphrase?" to it.

### Export signed PSBTs to microSD
You can now save a signed PSBT to microSD which should help users having trouble getting their webcams to read the tiny QR codes on the M5StickV. Furthermore, Krux supports loading a PSBT from microSD as well if you want to forgo QR codes entirely.

### Better mnemonic generation
The flow for entering rolls has been streamlined to allow more rapid input, with your string of rolls now being visible along the top of the screen as you go. We also introduced a change to how the D6 roll string is built, no longer including "-" between rolls prior to hashing to have consistency with ColdCard and SeedSigner. 

Note: We continue to use a "-" separator between D20 rolls to avoid reducing state space due to collisions (e.g., rolling 1-17 and 11-7 would result in the same 117 string without a separator, and would thus have the same hash)

### Back button and rotary encoders
All devices, even the M5StickV, support moving backward in the UI now. The left-side power button on the M5StickV no longer does one-press resets and instead acts as a third input button. Note: You can still shutdown the device by holding it down for 5 seconds.

Support for using a rotary encoder as the previous and next buttons has also been added. Check out @odudex’s open source case design with instructions on how to use one with the Dock:
[https://github.com/odudex/DockEncoderCase](https://github.com/odudex/DockEncoderCase)

Just to note, he also has a case design for the Bit:

[https://github.com/odudex/MaixBitCase](https://github.com/odudex/MaixBitCase)

### Updated website + i18n future
The Github Pages site has been updated with new documentation and screenshots for the Amigo.

A new internationalization (i18n) framework has been added by @qlrd that will allow the website to be easily translated to other languages so we can eventually have documentation for every language that Krux supports!

@qlrd is also working on a graphical installer we hope to start making use of in the future when it’s ready. Keep tabs on it here: [https://github.com/qlrd/krux-installer](https://github.com/qlrd/krux-installer)

# Version 22.03.0 - March 31, 2022
Finally, after much TODO, the first official release of Krux is out!

Krux will be following a calendar version release schedule similar to Ubuntu, hence the first release is version (20)22.03.0. If any glaring security issues or important bugfixes come up, they will make their way into point releases such as 22.03.1, 22.03.2, etc. All new work will go toward major releases which will get a new year and month combo.

Thank you to everyone who contributed their time and effort toward this release. It's been very cool to see people take an interest in the project! Also, a special thank you is due to @stepansnigirev for creating the embit library that Krux leans so heavily on.

## Installing
For instructions on how to install this release, please follow the Getting Started guide on [https://selfcustody.github.io/krux/](https://selfcustody.github.io/krux/).
