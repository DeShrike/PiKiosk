# Pi Kiosk

Simple kiosk application for Raspberry Pi.

Includes a web interface to manage the kiosk.

## Dependancies



## Installation

Start with a clean install of Raspberry Pi OS.

Download the *Raspberry Pi OS with desktop* from https://www.raspberrypi.com/software/operating-systems/#raspberry-pi-os-32-bit

Write the image to an SD Card.

After first boot, do all the usual things: expand the filesystem, change the default password, etc...

### Install packages:

```console
sudo apt-get update
sudo apt-get install python3-pip
sudo apt-get install git
pip3 install flask
pip3 install websocket-client
pip3 install requests
```

These should already be installed:

```console
sudo apt-get install xserver-xorg xinit
# sudo dpkg-reconfigure x11-common
sudo apt-get install chromium-browser
```

### Clone this repo:

```console
cd
git clone https://github.com/DeShrike/PiKiosk.git
```



## Setup


## TODO

- More errorhandling
- Security: ask for password
- Use another webserver (Apache or ...)
- Add a setup script
