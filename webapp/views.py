import hashlib
from webapp import webapp
from flask import render_template, send_from_directory, request, redirect, url_for, make_response, abort, session
from werkzeug.utils import secure_filename
from logging import getLogger
from os import listdir
from os.path import isfile, join, realpath, splitext
from .viewmodel import ViewModel
import config
import os

STATIC_FOLDER = "./webapp/static/"

logger = getLogger(__name__)

@webapp.route("/favicon.ico")
def send_favicon():
    return send_from_directory("static/img", "favicon.ico")

@webapp.route("/screenshot")
def screenshot():

    if config.ATTACH_TO_BROWSER is False:
        return "", 404

    screenshot_bytes = webapp.kiosk.get_screenshot()
    if screenshot_bytes is None:
        return abort(404)

    response = make_response(screenshot_bytes)
    response.headers.set('Content-Type', 'image/png')
    
    return response

@webapp.route("/reboot", methods=["POST"])
def reboot():
    if not authenticated():
        return "Not allowed", 401

    os.system("sudo shutdown -r 1")
    return "", 200

@webapp.route("/shutdown", methods=["POST"])
def shutdown():
    if not authenticated():
        return "Not allowed", 401

    os.system("sudo shutdown -h 1")
    return "", 200

@webapp.route("/about", methods=["GET"])
def about():
    model = build_viewmodel()
    model.title = "About"
    
    return render_template("about.html", model = model)

@webapp.route("/status", methods=["GET"])
def status():
    model = build_viewmodel()
    model.title = "Status"

    if config.ATTACH_TO_BROWSER:
        model.status = webapp.kiosk.get_status()

    return render_template("status.html", model = model)

@webapp.route("/settings", methods=["GET"])
def settings():
    if not authenticated():
        return redirect(url_for("login"))

    users = webapp.users

    model = build_viewmodel()
    model.title = "Settings"
    model.users = [{ "index": ix, "user": user } for (ix, user) in enumerate(users.users) ]  

    return render_template("settings.html", model = model)

def build_index():
    repository = webapp.repository

    model = build_viewmodel()
    model.items = [{ "index": ix, "item": item, "url": item.build_relative_url() } for (ix, item) in enumerate(repository.items) ]  
    model.item_count = len(model.items)

    return render_template("index.html", model = model)

@webapp.route("/", methods=["GET"])
def index():
    return build_index()

@webapp.route("/login", methods=["GET", "POST"])
def login():
    if authenticated():
        return redirect(url_for("index"))

    model = build_viewmodel()

    if request.method == "POST":
        u = request.form.get("username")
        pw = request.form.get("pw")

        if signin(str(u), str(pw)):
            return redirect(url_for('index'))
        else:
            model.username = u
            model.message = "Unknown username or bad password."

    return render_template("login.html", model = model)

@webapp.route('/logout')
def logout():
    signout()
    return redirect(url_for('index'))

@webapp.route("/uploader", methods = ["POST"])
def upload_file():
    if not authenticated():
        return redirect(url_for("login"))

    if request.method == "POST":
        uploaded_file = request.files["file"]
        filename = secure_filename(uploaded_file.filename)
        if filename != "":
            file_ext = splitext(filename)[1]
            if file_ext in webapp.config['UPLOAD_EXTENSIONS']:
                filename = join(f"{STATIC_FOLDER}{config.IMAGES_VIRTUAL_FOLDER}", filename)
                uploaded_file.save(filename)

    return redirect(url_for("new_item"))

@webapp.route("/add_url", methods=["POST"])
def add_url():
    if not authenticated():
        return redirect(url_for("login"))

    if request.method == "POST":
        url = request.form.get("url")
        if url is None or url == "":
            return redirect(url_for("index"))
        duration = request.form.get("duration")
        if duration is None or duration.isnumeric() is False:
            duration = 60
        else:
            duration = int(duration)

        repository = webapp.repository
        repository.add(url, "url", duration, False, None)
        repository.save()

    return redirect(url_for("index"))

@webapp.route("/add_image", methods=["POST"])
def add_image():
    if not authenticated():
        return redirect(url_for("login"))

    if request.method == "POST":
        image_name = request.form.get("imagename")
        if image_name is None or image_name == "":
            return redirect(url_for("index"))
        duration = request.form.get("duration")
        if duration is None or duration.isnumeric() is False:
            duration = 60
        else:
            duration = int(duration)
        bgcolor = request.form.get("bgcolor")
        if bgcolor is None or bgcolor == "":
            bgcolor = "#FFFFFF"

        repository = webapp.repository
        repository.add(image_name, "image", duration, False, bgcolor)
        repository.save()

    return redirect(url_for("index"))

@webapp.route("/add_html", methods=["POST"])
def add_html():
    if not authenticated():
        return redirect(url_for("login"))

    if request.method == "POST":
        html_name = request.form.get("htmlname")
        if html_name is None or html_name == "":
            return redirect(url_for("index"))
        duration = request.form.get("duration")
        if duration is None or duration.isnumeric() is False:
            duration = 60
        else:
            duration = int(duration)

        repository = webapp.repository
        repository.add(html_name, "html", duration, False, None)
        repository.save()

    return redirect(url_for("index"))

@webapp.route("/new", methods=["GET"])
def new_item():
    if not authenticated():
        return redirect(url_for("login"))

    model = build_viewmodel()

    staticfolder = f"{STATIC_FOLDER}{config.IMAGES_VIRTUAL_FOLDER}"
    model.available_images = sorted([f for f in listdir(staticfolder) if isfile(join(staticfolder, f)) and isimagefile(f)])
    model.available_htmls = sorted([f for f in listdir(staticfolder) if isfile(join(staticfolder, f)) and ishtmlfile(f)])

    return render_template("new.html", model = model)

@webapp.route("/htmlfile/<filename>")
def htmlfile(filename: str):
    return send_from_directory(f"static/{config.IMAGES_VIRTUAL_FOLDER}", filename)

@webapp.route("/image_centered/<image>/<bgcolor>")
def image_centered(image: str, bgcolor: str):
    model = build_viewmodel()

    model.background_color = bgcolor
    model.image_name = config.IMAGES_VIRTUAL_FOLDER + image

    return render_template("image_centered.html", model = model)

@webapp.route("/image_fullscreen/<image>/<bgcolor>")
def image_fs(image: str, bgcolor: str):
    model = build_viewmodel()

    model.background_color = bgcolor
    model.image_name = config.IMAGES_VIRTUAL_FOLDER + image

    return render_template("image_full_screen.html", model = model)

@webapp.route("/item_delete", methods=["POST"])
def item_delete():
    if not authenticated():
        return None
    data = request.json
    index = data["index"]
    repository = webapp.repository
    repository.delete_by_index(index)
    return build_index()

@webapp.route("/item_up", methods=["POST"])
def item_up():
    if not authenticated():
        return None
    data = request.json
    index = data["index"]
    repository = webapp.repository
    repository.moveup_by_index(index)
    return build_index()

@webapp.route("/item_down", methods=["POST"])
def item_down():
    if not authenticated():
        return None
    data = request.json
    index = data["index"]
    repository = webapp.repository
    repository.movedown_by_index(index)
    return build_index()

@webapp.route("/item_activate", methods=["POST"])
def item_activate():
    if not authenticated():
        return None
    data = request.json
    index = data["index"]
    webapp.kiosk.activate_by_index(index)
    return "", 200

def ishtmlfile(filename):
    validextension = [".html", ".htm"]
    ext = filename[filename.rfind("."):]
    return ext in validextension

def isimagefile(filename):
    validextension = [".png", ".jpeg", ".jpg", ".gif"]
    ext = filename[filename.rfind("."):]
    return ext in validextension

def build_viewmodel():
    model = ViewModel()
    model.authenticated = authenticated()
    model.username = authenticated_user() if authenticated_user() is not None else ""
    return model

def signin(username: str, password: str) -> bool:
    if username in config.USERS:
        hash = hashlib.sha256(password.encode("utf-8")).hexdigest()
        if config.USERS[username] == hash:
            session["username"] = username
            session["authenticated"] = True
            return True

    return False

def signout():
    session.pop("username", None)
    session.pop("authenticated", None)

def authenticated() -> bool:
    return ("authenticated" in session) and (session["authenticated"] == True)

def authenticated_user() -> str:
    return None if not authenticated() else session["username"]
