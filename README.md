# puppet-octoprintpi

Puppet module for configuring and managing Raspberry Pis running OctoPrint and related software.

## What's Here?

Lorem ipsum.

### Why not OctoPi?

[OctoPi](https://github.com/guysoft/OctoPi) is a wonderful project that makes it super easy to get up and running with OctoPrint on a Raspberry Pi. However, for an organization with half a dozen or more Pis running 3d Printers, and a whole bunch more Pis doing other things, it has a few significant disadvantages:

1. The pace of releases has been pretty slow recently; there were OctoPi releases in January 2021 and February 2023.
2. There's no official upgrade process other than "back everything up, re-image, restore everything".
3. We're already managing a bunch of Pis for other purposes, and from a maintenance and update standpoint, it's easiest to just have them all running the same image.

## Setting Up a New Pi

First, obtain a Raspberry Pi 3B or newer and a MicroSD card of 32GB or larger (preferably 64GB or 128GB).

Note that the following instructions assume you're working on a Linux (or maybe Mac?) computer. Please consult a knowledgeable source if you're using Windows.

1. Download the latest [Raspberry Pi OS 64-bit Lite](https://www.raspberrypi.com/software/operating-systems/) image. At the moment this is the May 3rd, 2023 image with kernel 6.1 and Debian 11, which has a filename of `2023-05-03-raspios-bullseye-arm64-lite.img.xz` (**note** the following instructions will all assume this filename)
1. Extract that image with `xz -d 2023-05-03-raspios-bullseye-arm64-lite.img.xz`
1. Put a SD card in a USB adapter and plug in to your computer. Write the image to it, replacing `/dev/sdX` with the path to the SD card block device: `dd bs=4M if=2023-05-03-raspios-bullseye-arm64-lite.img of=/dev/sdX conv=fsync status=progress`
1. Mount the first (boot) partition from the SD card (e.g. `mount /dev/sdX1 /mnt/temp`) and `cd` to where it's mounted
   1. `touch ssh` to enable SSH at boot
   1. Since Raspberry Pi OS [no longer has a default user](https://www.raspberrypi.com/news/raspberry-pi-bullseye-update-april-2022/), configure the initial user account for the pi. The (random) password should be on a label on the Pi being used (along with its MAC address). Encrypt that password (replacing `PasswordFromLabelOnPi` with the password from the label) with `echo 'PasswordFromLabelOnPi' | openssl passwd -6 -stdin` and write the username (`pi`) and output from that command to a file at `userconf` in the format `pi:<encrypted-password>` where `<encrypted-password>` is the openssl output.
   1. Unmount the partition (`sync; sync; umount /mnt/temp`)
1. On your local computer, create a `wpa_supplicant.conf` file with content for the DM network:
    ```
    ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
    update_config=1
    country=US

    network={
            ssid="DecaturMakers"
            psk="<Our Network Key>"
            key_mgmt=WPA-PSK
    }
    ```
1. Mount the second (root) partition from the SD card (e.g. `mount /dev/sdX2 /mnt/temp`) and `cd` to where it's mounted
   1. `cat <path to>/wpa_supplicant.conf > etc/wpa_supplicant/wpa_supplicant.conf`
   1. `echo octotest > etc/hostname`
   1. `sed -i "/127.0.1.1/s/raspberrypi/octotest/" etc/hosts`
   1. Unmount the partition (`sync; sync; umount /mnt/temp`)
1. Unplug the SD card from your computer and plug it in to the Pi.
1. If this is a new Pi and you don't know its MAC address, plug the Pi's wired Ethernet port into your laptop, power up the pi, and fire up Wireshark. When the Pi starts sending DHCPDISCOVER messages, get its MAC address.
1. If this Pi isn't already set up in the UniFi network controller, set up a fixed IP lease for its MAC address.
1. Wait for the Pi to settle a bit, and then unplug power and then Ethernet. Once the UniFi changes propagate out to the router, plug the Pi in for real.
1. `ssh pi@<IP Address of Pi>` using the password on the label in the enclosure. Assuming you properly set up the files on the boot partition, when the Pi finishes booting up it will be running SSH for remote login and have the default (pi) user configured.
1. Perform a full system update: ``sudo apt update && sudo apt upgrade && sudo reboot`` ; once the reboot is done, log back in via SSH.
1. ``sudo raspi-config``
   1. System Options -> Hostname (set to `sidedoorpi`)
   1. System Options -> Network at Boot -> wait for network at boot
   1. Localisation Options -> Locale (unselect `en_GB.UTF-8 UTF-8` and select `en_US.UTF-8 UTF-8`; set the default locale to `en_US.UTF-8`)
   1. Localisation Options -> Timezone (select America -> New York)
   1. System Options -> Wireless LAN -> select "US" for country then cancel when asked for the SSID.
   1. System Options -> Boot / Auto Login -> Console
   1. Finish, Reboot
1. ``sudo apt install puppet git r10k``
1. ``sudo su -``
   1. ``ssh-keygen`` - just hit Enter for every prompt (no passphrase)
   1. ``cat /root/.ssh/id_rsa.pub``
   1. Add the output of that (the content of ``/root/.ssh/id_rsa.pub``) as a [deploy key on this repository](https://github.com/DecaturMakers/dm-puppet/settings/keys)
   1. ``echo -e "Host github.com\n  StrictHostKeyChecking no\n  UserKnownHostsFile /dev/null\n" >> ~/.ssh/config && chmod 0600 ~/.ssh/config``
   1. ``cd /root && git clone git@github.com:DecaturMakers/dm-puppet.git && cd dm-puppet``
   1. ``./bin/run_r10k_puppet.sh``
   1. At this point you should probably ``reboot`` just to make sure all changes will be active.
1. Enjoy!
