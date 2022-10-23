# Configuration settings for Pi Kiosk

# This must match with the value in the kiosk.sh script.
CHROMIUM_DEBUG_PORT = 9222

# The port for the management site.
PORT = 8080

# The address to bind the management site to. Use "0.0.0.0" for all addresses, or specify a specific one.
HOST = "0.0.0.0"

# The name of the file containing the items to display on the kiosk. Only edit this manually if you knoow what you are doing.
REPOSITORY_FILE = "repository.json"

# The virtual folder for the images. Do not change unless you know what you are doing.
IMAGES_VIRTUAL_FOLDER = "images/"

