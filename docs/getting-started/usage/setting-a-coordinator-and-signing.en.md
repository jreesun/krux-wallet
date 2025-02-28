After creating a mnemonic, making a safe backup, and testing to recover your mnemonic, it's time to set up a coordinator.

Krux can work with multiple coordinator wallets. Popular options include:

- [Sparrow Wallet](https://www.sparrowwallet.com/) (desktop)
- [Liana](https://wizardsardine.com/liana/) (desktop)*
- [Specter Desktop](https://specter.solutions/) (desktop)
- [Nunchuk](https://nunchuk.io/) (mobile)
- [BlueWallet](https://bluewallet.io/) (mobile)

**Note: For Liana, the exchange of extended public keys, wallet output descriptors, and PSBTs is performed via copy and paste. On Krux, use SD cards and a standard text editor, or use QR codes via an intermediary application such as [SeedQReader](https://github.com/pythcoiner/SeedQReader).*

## Step 1: Install the Coordinator Wallet

Download and install the appropriate version of your chosen coordinator wallet for your device and operating system.

## Step 2: Create a New Wallet with Krux as a Signer

Depending on the coordinator, the steps to add Krux as a signer may vary slightly:

**Specter and Nunchuk Single-sig:** Add Krux key, then create a wallet that uses it.

**Specter and Nunchuk Multisig:** Add Krux key, add other keys, then create a wallet that uses them.

**Sparrow, Liana and BlueWallet**: Create a wallet (or vault in Blue Wallet) and add keys during setup.

1. Load a mnemonic and wallet in Krux.

<img src="../../../img/maixpy_amigo/load-mnemonic-seq-mnemonic-300.png" class="amigo">
<img src="../../../img/maixpy_amigo/load-mnemonic-seq-overview-300.png" class="amigo">
<img src="../../../img/maixpy_m5stickv/load-mnemonic-seq-mnemonic-250.png" class="m5stickv">
<img src="../../../img/maixpy_m5stickv/load-mnemonic-seq-overview-250.png" class="m5stickv">

2. On your coordinator, when presented with possible signer devices to add, choose Krux if available, otherwise choose "other" or even another QR code compatible signer. As Krux is compatible with many QR code formats, most of available alternatives should work.

3. When prompted by your coordinator to import signer's public key, access the `Extended Public Key` on Krux.

<img src="../../../img/maixpy_amigo/extended-public-key-selected-300.png" class="amigo">
<img src="../../../img/maixpy_m5stickv/extended-public-key-selected-250.png" class="m5stickv">

4. Export an *XPUB* (or *YPUB, ZPUB*, .., based on the script type) as a QR code.

<img src="../../../img/maixpy_amigo/extended-public-key-xpub-qr-menu-selected-300.png" class="amigo">
<img src="../../../img/maixpy_amigo/extended-public-key-wsh-xpub-qr-300.png" class="amigo">
<img src="../../../img/maixpy_m5stickv/extended-public-key-xpub-qr-menu-selected-250.png" class="m5stickv">
<img src="../../../img/maixpy_m5stickv/extended-public-key-wsh-xpub-qr-250.png" class="m5stickv">

5. Scan this QR code with your coordinator.

6. Ensure the coordinator’s wallet attributes (policy type, script type, fingerprint, and derivation) match those in Krux.

Alternatively, you can export the extended public keys as files to an SD card. Instead of displaying them as QR codes, select the `XPUB - Text` option, then choose `Save to SD card`.

<img src="../../../img/maixpy_amigo/extended-public-key-menu-300.png" class="amigo">
<img src="../../../img/maixpy_amigo/extended-public-key-wsh-xpub-text-300.png" class="amigo">
<img src="../../../img/maixpy_m5stickv/extended-public-key-menu-250.png" class="m5stickv">
<img src="../../../img/maixpy_m5stickv/extended-public-key-wsh-xpub-text-250.png" class="m5stickv">

## Step 3: Load and Backup Wallet Descriptor (Multisig Only)

1. In your coordinator, export the wallet descriptor containing information about the wallet and all cosigners:
    - **Sparrow**: "Descriptor"
    - **Liana**: "Wallet Descriptor"
    - **Specter**: "Export Wallet"
    - **Nunchuk**: "Export Wallet Configuration"
    - **BlueWallet**: "Export Coordination Setup"
2. Export the descriptor as a QR code or file.
3. On Krux, go to **Wallet -> Wallet Descriptor** to scan the descriptor QR code or load it via SD card.

<img src="../../../img/maixpy_amigo/wallet-load-prompt-300.png" class="amigo big">
<img src="../../../img/maixpy_amigo/wallet-wsh-load-prompt-300.png" class="amigo big">
<img src="../../../img/maixpy_m5stickv/wallet-load-prompt-250.png" class="m5stickv big">
<img src="../../../img/maixpy_m5stickv/wallet-wsh-load-prompt-250.png" class="m5stickv big">

4. If you access **Wallet -> Wallet Descriptor** again, you will be able to:
    - Check the wallet cosigners.
    - Save the descriptor on an SD card (useful if you initially loaded it from QR codes).

    **Tip**: Having a backup of the wallet descriptor is essential for recovering your wallet.

## Step 4: Verify Addresses

<img src="../../../img/maixpy_m5stickv/list-address-receive-250.png"  align="right" class="m5stickv">
<img src="../../../img/maixpy_amigo/list-address-receive-300.png"  align="right" class="amigo">

For single-sig or multisig (after loading a descriptor):

- Go to `Address` on Krux.

- List `Receive Addresses` and `Change Addresses` or use `Scan Address` to verify if addresses from your coordinator are matched by Krux.

<div style="clear: both"></div>

## Step 5: Funding your Wallet

Once addresses are verified, send a small test amount to your wallet. Test signing and sending a transaction before adding more funds.

## Step 6: Sign PSBTs and Messages

### PSBTs

1. Create a transaction in your coordinator.

2. Export the transaction as a QR code.

3. On Krux, go to **Sign -> PSBT -> Load from camera**.

4. Scan the animated QR code.

5. Verify the transaction details.

6. If correct, press `Sign to QR code`.

7. Scan the signed transaction QR code back into the coordinator to broadcast it.

Alternatively, you can use an SD card:

Save the transaction as a file on an SD card. On Krux, go to **Sign -> PSBT -> Load from SD card** and `Sign to SD card`. Load the signed transaction on the coordinator and broadcast it.

### Messages

<img src="../../../img/maixpy_m5stickv/sign-message-at-address-prompt-250.png" align="right" class="m5stickv">
<img src="../../../img/maixpy_amigo/sign-message-at-address-prompt-300.png" align="right" class="amigo">

Some coordinators, like Sparrow, allow you to sign messages linked to your wallet's addresses. Signing and verifying a message signature attests to the ownership of an address and serves as an additional test for your setup.

<div style="clear: both"></div>