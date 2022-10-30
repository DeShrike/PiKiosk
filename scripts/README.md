


# Install Services

## Start Chromium at start

Add these lines to the bottom of your .bashrc file

```
if [ -z $DISPLAY ] && [ $(tty) = /dev/tty1 ]
then
    xinit /home/pi/pikiosk/scripts/pikioskx.sh -- vt$(fgconsole)
fi
```

## Webapp

This service will start main.py

### Install the service

```console
sudo cp ~/pikiosk/scripts/pikiosk.service /lib/systemd/system/pikiosk.service
sudo systemctl enable pikiosk.service
```

### Start the service

```console
sudo systemctl start pikiosk.service
```

### Check the service status

```console
sudo systemctl status pikiosk.service
```

### Stop the service

```console
sudo systemctl stop pikiosk.service
```

### Disable the service

```console
sudo systemctl disable pikiosk.service
```
