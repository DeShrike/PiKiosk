# Configuration settings for Pi Kiosk

# This must match with the value in the kiosk.sh script.
CHROMIUM_DEBUG_PORT = 9222

# The port for the management site.
PORT = 8080

# The address to bind the management site to. Use "0.0.0.0" for all addresses, or specify a specific one.
HOST = "0.0.0.0"

# Set this to False if you want to use the webapp with actually connecting to a browser.
ATTACH_TO_BROWSER = True

# The name of the file containing the items to display on the kiosk. Only edit this file manually if you know what you are doing.
REPOSITORY_FILE = "repository.json"

# The virtual folder for the images. Do not change unless you know what you are doing.
IMAGES_VIRTUAL_FOLDER = "assets/"

# Default username password is admin / admin
# Use adduser.py to create key for a new user, and add it to this dictionary.
USERS = {
    "admin": "8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918"
}
