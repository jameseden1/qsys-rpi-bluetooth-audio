# Raspberry Pi Bluetooth Audio Receiver

## Setup instructions

### Setup Raspberry Pi OS

1. Flash an SD card with the latest Raspberry Pi OS Lite

2. Connect the Raspberry Pi to HDMI, keyboard, ethernet and power. (Ethernet connection should have access to the internet, and DHCP)

3. Login using username `pi`, password `raspberry`

4. Enable SSH
    * Run `sudo raspi-config`
    * Navigate to `Interfacing Options` > `SSH`
    * Select `Yes`

5. Connect via SSH

    Find the IP address using `ifconfig` and connect via Putty

6. Configure keyboard

    * Run `sudo raspi-config`
    * Navigate to `Locatisation Options` > `Change Keyboard Layout` 
    * Select the current option
    * Select `Other`
    * Select `English (US)`
    * Select `English (US)`
    * Select `The default for the keyboard layout`
    * Select `No compose key`

7. Copy the `rpi` repository over to the home directory of the Pi via SFTP (eg CyberDuck)

8. Run `cd ~/rpi`
    s
9. Run `sudo python3 setup-1.py` and follow the prompts. Wait until it reboots

10. Run `cd ~/rpi`

11. Run `sudo bash setup-2.sh`

Everything is now setup and running

### Optional network setup

Set a static IP address for the eth0 interface

1. sudo nano /etc/dhcpcd.conf
2. Enter the below lines at the bottom of the file (replacing values where necessary)

    ```
        interface eth0
        static ip_address=10.42.62.181/24
        static routers=10.42.62.1
        static domain_name_servers=10.42.62.1
    ```
3. Once you're done, type Ctrl + C, then Y, then Enter to save
