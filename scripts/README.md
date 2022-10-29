# Install Services

## Chromium Service

### Install the service

```console
sudo cp ~/pikiosk/scripts/pikioskx.service /lib/systemd/system/pikioskx.service
sudo systemctl enable pikioskx.service
```

### Start the service

```console
sudo systemctl start pikioskx.service
```

### Check the service status

```console
sudo systemctl status pikioskx.service
```

### Stop the service

```console
sudo systemctl stop pikioskx.service
```

### Disable the service

```console
sudo systemctl disable pikioskx.service
```

## Webapp Service



https://werkzeug.palletsprojects.com/en/1.0.x/urls/
