Krux supports creating 12 and 24-word BIP-39 mnemonic seed phrases. Since generating true entropy is challenging, especially with an embedded device, we recommend outsourcing entropy generation using dice rolls. However, it is also possible to randomly pick words (e.g., SeedPicker) or use the camera as a source of entropy to quickly create a mnemonic.

At the start screen, after selecting New Mnemonic, you will be taken to a second menu where you can choose to create a mnemonic via the camera, words, rolls of a D6 (standard six-sided die), or a D20 (20-sided die).

<img src="../../../img/maixpy_amigo/new-mnemonic-options-300.png" class="amigo">
<img src="../../../img/maixpy_m5stickv/new-mnemonic-options-250.png" class="m5stickv">

## Camera
(Experimental!) Choose between 12, 24 words or double mnemonic, then take a random picture and Krux will generate a mnemonic from the hash of the image bytes.

<img src="../../../img/maixpy_amigo/new-mnemonic-via-snapshot-prompt-300.png" class="amigo">
<img src="../../../img/maixpy_amigo/new-mnemonic-via-snapshot-capturing-300.png" class="amigo">
<img src="../../../img/maixpy_m5stickv/new-mnemonic-via-snapshot-prompt-250.png" class="m5stickv">
<img src="../../../img/maixpy_m5stickv/new-mnemonic-via-snapshot-capturing-250.png" class="m5stickv">

#### Image Entropy Quality Estimation
<img src="../../../img/maixpy_m5stickv/new-mnemonic-via-snapshot-entropy-estimation-250.png" align="right" class="m5stickv">
<img src="../../../img/maixpy_amigo/new-mnemonic-via-snapshot-entropy-estimation-300.png" align="right" class="amigo">

During image capture, entropy quality estimation is displayed to assist you in obtaining a quality image source for your key. After a snapshot is taken, Shannon's entropy and pixel deviation indices are presented. Minimum thresholds are established to prevent the use of poor-quality images with low entropy for key generation. It's important to note that these values serve as indicators or estimations of entropy quality, but they are not absolute entropy values in a cryptographic context.

<div style="clear: both"></div>

#### Double mnemonic
It is the combination of two 12-word mnemonics that also forms a valid 24-word BIP-39 mnemonic. This is achieved by using the first 16 bytes (128 bits) of the image's entropy to generate the first 12-word, then using the next 16 bytes to generate the second 12-word and checking if these two 12-word together forms a valid 24-word, if not, we iterate over the second 12-word incrementing its entropy bytes until the two 12-word forms a valid 24-word.

Double Mnemonic was first defined by Stepan Snigirev in his [Double Mnemonic Generator](https://stepansnigirev.github.io/seed-tools/double_mnemonic.html). It can be used for plausible deniability, or, as Stepan stated, to have fun and confuse everyone.

## Words
Print the BIP39 word list in 3D or on paper, then cut out the words and place them in a bucket. Manually draw 11 or 23 words from the bucket.
For the final word, Krux will assist you in picking a valid 12th or 24th word by adjusting its smart keypad to only allow typing words with a valid checksum. Alternatively, you can leave it empty, and Krux will select a final, valid checksum word for you.

## Dice Rolls
### Via D6
Choose between 12 or 24 words. The entropy in a single roll of a D6 is 2.585 bits ( log<sub>2</sub>(6) ); therefore a minimum of a 50 rolls will be required for 128 bits of entropy, enough to generate a 12-word mnemonic. For 24-word, or an entropy of 256 bits, a minimum of 99 rolls will be required.

<img src="../../../img/maixpy_amigo/new-mnemonic-via-d6-roll-1-300.png" class="amigo">
<img src="../../../img/maixpy_amigo/new-mnemonic-via-d6-last-n-rolls-300.png" class="amigo">
<img src="../../../img/maixpy_m5stickv/new-mnemonic-via-d6-roll-1-250.png" class="m5stickv">
<img src="../../../img/maixpy_m5stickv/new-mnemonic-via-d6-last-n-rolls-250.png" class="m5stickv">

### Via D20
Since a D20 has more possible outcomes, the entropy is increased per roll to 4.322 bits ( log<sub>2</sub>(20) ). This means that only 30 rolls are necessary to create a 12-word mnemonic and 60 rolls for a 24-word mnemonic.

<img src="../../../img/maixpy_amigo/new-mnemonic-via-d20-roll-1-300.png" class="amigo">
<img src="../../../img/maixpy_amigo/new-mnemonic-via-d20-last-n-rolls-300.png" class="amigo">
<img src="../../../img/maixpy_m5stickv/new-mnemonic-via-d20-roll-1-250.png" class="m5stickv">
<img src="../../../img/maixpy_m5stickv/new-mnemonic-via-d20-last-n-rolls-250.png" class="m5stickv">

### Dice Rolls Entropy Quality Estimation
<img src="../../../img/maixpy_m5stickv/new-mnemonic-via-d6-roll-string-250.png" align="right" class="m5stickv">
<img src="../../../img/maixpy_amigo/new-mnemonic-via-d6-roll-string-300.png" align="right" class="amigo">

When you input your dice rolls, you'll see two progress bars filling up. The top progress bar shows how many rolls you've entered compared to the minimum number needed. The bottom progress bar shows the real-time calculated Shannon's entropy compared to the required minimum (128 bits for 12 words and 256 bits for 24 words). When the Shannon's entropy estimation reaches the recommended level, the progress bar will be full, and its frame will change color. If you've met the minimum number of rolls but the entropy estimation is still below the recommended level, a warning will appear, suggesting you add more rolls to increase entropy.
Note: Similar to image entropy quality estimation, dice rolls Shannon's entropy serves as an indicator and should not be considered an absolute measure of cryptographic entropy.

Learn more about [Krux Entropy Quality Estimation](../features/entropy.md).

<div style="clear: both"></div>

### Stats for Nerds
A low Shannon's entropy value could suggest that your dice are biased or that there's a problem with how you're gathering entropy. To investigate further, examine the "Stats for Nerds" section to check the distribution of your rolls and look for any abnormalities.

<img src="../../../img/maixpy_amigo/new-mnemonic-via-d6-roll-nerd-stats-300.png" class="amigo">
<img src="../../../img/maixpy_amigo/new-mnemonic-via-d20-roll-nerd-stats-300.png" class="amigo">
<img src="../../../img/maixpy_m5stickv/new-mnemonic-via-d6-roll-nerd-stats-250.png" class="m5stickv">
<img src="../../../img/maixpy_m5stickv/new-mnemonic-via-d20-roll-nerd-stats-250.png" class="m5stickv">


## Editing a New Mnemonic - Optional
After entering dice rolls, random words, or captured entropy through the camera, you can manually add custom entropy by editing some of the words. Edited words will be highlighted, and the final word will automatically update to ensure a valid checksum. However, proceed with caution, modifying words can negatively impact the natural entropy previously captured.

<img src="../../../img/maixpy_amigo/new-mnemonic-edited-300.png" class="amigo">
<img src="../../../img/maixpy_m5stickv/new-mnemonic-edited-250.png" class="m5stickv">

## How Entropy Capture Works
For dice rolls, Krux keeps track of every roll you enter and displays the cumulative string of outcomes after each roll. 

When you have entered your final roll, Krux will hash this string using [SHA256](https://en.bitcoin.it/wiki/SHA-256) and output the resulting hash to the screen so that you can verify it for yourself.

In case a camera snapshot is used as a source, the image bytes, which contain pixels data in RGB565 format, will be hashed in the same way as the dice rolls.

<img src="../../../img/maixpy_amigo/new-mnemonic-via-snapshot-sha256-300.png" class="amigo">
<img src="../../../img/maixpy_amigo/new-mnemonic-via-d6-roll-sha256-300.png" class="amigo">
<img src="../../../img/maixpy_m5stickv/new-mnemonic-via-snapshot-sha256-250.png" class="m5stickv">
<img src="../../../img/maixpy_m5stickv/new-mnemonic-via-d6-roll-sha256-250.png" class="m5stickv">

Krux then takes this hash, runs [`unhexlify`](https://docs.python.org/3/library/binascii.html#binascii.unhexlify) on it to encode it as bytes, and deterministically converts it into a mnemonic according to the [BIP-39 Reference Implementation](https://github.com/trezor/python-mnemonic/blob/6b7ebdb3624bbcae1a7b3c5485427a5587795120/src/mnemonic/mnemonic.py#L189-L207).

Note: For 12-word mnemonics, only the first half of the SHA256 hash is used (128 bits), while 24-word mnemonics use the full hash (256 bits).

### How to Verify
Don't trust, verify. We encourage you not to trust any claim you cannot verify yourself. Therefore, there are wallets that use compatible algorithms to calculate the entropy derived from dice rolls. You can use the [SeedSigner](https://seedsigner.com/) or [Coldcard](https://coldcard.com/) hardware wallets, or even the [Bitcoiner Guide website](https://bitcoiner.guide/seed/), they share the same logic that Krux uses and will give the same mnemonic for the dice roll method.
