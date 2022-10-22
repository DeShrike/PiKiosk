from datetime import timedelta
from flask import Flask
import logging

logger = logging.getLogger(__name__)

class CustomFlask(Flask):
    jinja_options = Flask.jinja_options.copy()
    jinja_options.update(dict(
        variable_start_string='%%',  # Default is '{{', I'm changing this because Vue.js uses '{{' / '}}'
        variable_end_string='%%',
    ))


app = CustomFlask(__name__)
app.secret_key = "RTR10Rtnttrrwrttri76#"
app.config["SECRET_KEY"] = "RTR10Rtnttrrwrttri76#"
app.permanent_session_lifetime = timedelta(days = 2)

from app import views
from app import api

logger.info("App __init__")

