from datetime import timedelta
from flask import Flask
import logging

logger = logging.getLogger(__name__)

repository = None
kiosk = None

class CustomFlask(Flask):
    jinja_options = Flask.jinja_options.copy()
    jinja_options.update(dict(
        variable_start_string='%%',  # Default is '{{', I'm changing this because Vue.js uses '{{' / '}}'
        variable_end_string='%%',
    ))

webapp = CustomFlask(__name__)
webapp.secret_key = "RTR10Rtnttrrwrttri76#"
webapp.config["SECRET_KEY"] = "RTR10Rtnttrrwrttri76#"

webapp.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 * 5
webapp.config['UPLOAD_EXTENSIONS'] = [".jpg", ".png", ".gif"]

webapp.permanent_session_lifetime = timedelta(days = 2)

from webapp import views
#from webapp import api

logger.info("App __init__")

