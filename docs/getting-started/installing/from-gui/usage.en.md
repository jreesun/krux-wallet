This guide will walk through the basic use of the installer. At startup, it can differ in some
operational systems. In the rest, the procedures will be similar.

### Main Menu 
When executing the **Krux-Installer**, you will be presented with a menu of 4 enabled buttons and
two disabled buttons:

<img width="640" src="/krux/img/krux-installer/main.png" alt="Krux-Installer Main Menu" />

* Enabled buttons:
    * `Version`: select a firmware version;
    
    * `Device`: select a supported device for the selected version;
    
    * `Settings`: change some application settings;
    
    * `About`: just show some information about the application.

* Disabled buttons:

    * `Flash firmware`: This button will start the flash firmware procedure;
        
        * It will be enabled when user select **both** version and device;
    
    * `Wipe device`: This button will start the wipe device procedure.
    
        * It will be enabled when user select the device.

### Select version

At startup, the application will setup it to the latest one, `{{latest_krux}}`. But you can select
even a beta release or older versions:
    
<img width="640" src="/krux/img/krux-installer/select_version_menu.png" alt="Krux-Installer Select Version Menu" />

* Click in the button that show the text `Version: {{latest_krux}}`;

* To select a beta release, click on button that show the text `odudex/krux_binaries`;

* To select an older version, click on button that show the text `Old versions`;

#### Beta release

After choose `odudex/krux_binaries`, you'll be warned with a message:

<img width="640" src="/krux/img/krux-installer/warn_beta.png" alt="Krux-Installer warning beta version" />

#### Older versions

* We put this option in case you have any interest in the history of firmware development;

<img width="640" src="/krux/img/krux-installer/select_old_version_menu.png" alt="Krux-Installer Select Old Version Menu" />

* Each version supports one device or the other;

* For example: the version `v22.03.0` has support only for `m5stickv`.
    

### Settings

**Krux-Installer** will give to you some freedom of choices for:

* Krux-Installer settings;

* General settings;

#### Krux-Installer specific settings

Here you can configure some of the specifics of krux firmare, like:

<img width="640" src="/krux/img/krux-installer/app_settings.png" alt="Krux-Installer App settings Menu" />

* Where you'll save downloaded assets;

* The flash baudrate 

* The natural language that will be used in the application ([system locale](https://en.wikipedia.org/wiki/Locale_(computer_software))).

##### Flash baudrate
The flash baudrate is how quickly the firmware will be written to the device.

<img width="640" src="/krux/img/krux-installer/baudrate.png" alt="Krux-Installer baudrate" />

But not any value can be used. The valid ones are: 9600, 19200, 28800, 38400, 57600, 76800, 115200,
230400, 460800, 576000, 921600, 1500000.

##### System locale

At startup, **Krux-Installer** recognize the locale used in your system. If your language isn't supported, it will defaults to `en_US`.

<img width="640" src="/krux/img/krux-installer/locale_menu.png" alt="Krux-Installer locale menu" />


### Select Device

Everytime you select a new version, you'll see that the device button will be
reseted to `Device: select a new one` state. Once a version is selected you can choose a device
on which the firmware will be written.

First, select the device we want to flash. After that the menu will shown three items:

<img width="640" src="/krux/img/krux-installer/select_device.png" alt="Select Device Menu" />

Note that some devices may be disabled if they are not supported by the chosen version

### Flash device

Once you choose the device and version, it enables the "flash device" button. It will start an
**automatic** process of:

* For official firmware's releases:

    * Warning;

    * Download;

    * Verification:
    
    * Unzip the correct firmware;

    * Flash:
        
        * The flash itself via USB;

        * Air-gapped update via SD card;
        

* For beta releases:

    * Download asset;

    * The flash itself;

#### Warning

If you already downloaded assets, you'll be warned about this and will be offered the possibility
to download again or continue without downloading:

<img width="640" src="/krux/img/krux-installer/warn_already_downloaded.png" alt="Krux-Installer already downloaded" />

#### Download

**Krux-Installer** download can download four assets for official releases or one for beta releases.

##### Official releases

* A `zip` file containing all firmwares for each device;

* Download a `zip.sha256.txt` file containing a `zip`'s digital fingerprint;

* Download a `zip.sig` file containing a `zip`'s digital signature;
    
* Download the `selfcustody.pem` file containing a public key certificate, signed by `odudex`;

<img width="640" src="/krux/img/krux-installer/download_assets.png" alt="Krux-Installer downloading assets" />

##### Beta releases

* A `kfpkg` file containing the specific firmware for choosen device;

#### Verification

* Integrity verification compares the computed hash of `zip` against thei provided `zip.sha256.txt`;

* Authenticity verification check if the `zip` file was really signed by `odudex`, using
the `zip.sig` and `selfcustody.pem`.

<img width="640" src="/krux/img/krux-installer/verification.png" alt="Krux-Installer verification process" />


#### Unzip

Now you will be able to select if you do a flash process or need to do an airgap process:

<img width="640" src="/krux/img/krux-installer/unzip.png" alt="Krux-Installer unzip" />

Click on [Flash with](#flash-with) to install via USB or [Air-gapped update with](#air-gapped-update-with) to perform upgrades via an SD card.

#### Flash with

When flash starts, it will warn you to **not disconnect the device until the process is complete**.
You'll be able to see the flash progress:

<img width="640" src="/krux/img/krux-installer/flash.png" alt="Krux-Installer unzip" />
> ⚠️  TIP: You must connect and turn on your device **before click extract and flashing starts!**.

As well a done icon:

<img width="640" src="/krux/img/krux-installer/flash_done.png" alt="Krux-Installer unzip" />

> ⚠️  TIP:
----8<----
flash-krux-logo.en.txt
----8<----

#### Air-gapped update with

Once you've installed the initial firmware on your device via USB, you can perform upgrades via SD card to keep the device airgapped.

<img width="640" src="/krux/img/krux-installer/unzip.png" alt="Krux-Installer unzip" />
> ⚠️ Click on "Air-gapped update with"

Once the `firmware.bin` and `firmware.bin.sig` are extracted, you'll see a warning message.

<img width="640" src="/krux/img/krux-installer/warn_airgap.png" alt="Krux-Installer warn airgap" />

Insert the SD card and click 'Proceed' to allow the installer to detect it.

<img width="640" src="/krux/img/krux-installer/list_drivers.png" alt="Krux-Installer warn airgap" />
> ⚠️ If a single SD card is inserted, the screen will display a large button. If multiple removable drives are detected, both SD cards and other drives will be listed.

Select the desired removable drive to copy both `firmware.bin` and `firmware.bin.sig.` The first is the Krux firmware, and the second is a signature file that verifies the firmware’s integrity and authenticity. 

Now you can compare the firmware's hash computed by installer with  the firmware's hash computed by the device. 

<img width="640" src="/krux/img/krux-installer/airgap_done.png" alt="Krux-Installer warn airgap" />
> ⚠️ Once files are copied, remove the SD card from computer, connect to device and compare the hashes

### Wipe device

This is two step process:

* Warning

* Wipe

#### Warning

Before the wipe starts, it will show to you a message:

<img width="640" src="/krux/img/krux-installer/wipe_warn.png" alt="Wipe Warning" />
> ⚠️  TIP: It's useful when your device is not working or for security reasons.
To use Krux again, you'll need to re-flash the firmware.

#### Wipe

Once the process starts, the screen will appear frozen and a spinner will keep moving.
When it's done, you can scroll down you will see a `check` icon.

<img width="640" src="/krux/img/krux-installer/wipe.png" alt="Wipe Warning" />
> ⚠️  TIP: Do not unplug or poweroff your device or computer. Wait until the process finishes.

## Tips after install

----8<----
tips-after-install.en.txt
----8<----
