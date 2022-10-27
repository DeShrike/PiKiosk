from webapp import webapp
from flask import render_template, send_from_directory, request, redirect, url_for, make_response, abort
from werkzeug.utils import secure_filename
from logging import getLogger
from os import listdir
from os.path import isfile, join, realpath, splitext
from .viewmodel import ViewModel
import config

STATIC_FOLDER = "./webapp/static/"

logger = getLogger(__name__)

@webapp.route("/favicon.ico")
def send_favicon():
    return send_from_directory("static/img", "favicon.ico")

@webapp.route("/screenshot")
def screenshot():

    screenshot_bytes = webapp.kiosk.get_screenshot()
    if screenshot_bytes is None:
        return abort(404)

    response = make_response(screenshot_bytes)
    response.headers.set('Content-Type', 'image/png')
    
    return response

@webapp.route("/about", methods=["GET"])
def about():
    model = ViewModel()
    model.title = "About"
    
    return render_template("about.html", model = model)

@webapp.route("/status", methods=["GET"])
def status():
    model = ViewModel()
    model.title = "Status"

    model.status = webapp.kiosk.get_status()

    return render_template("status.html", model = model)

@webapp.route("/", methods=["GET"])
def index():
    repository = webapp.repository
    model = ViewModel()
    model.items = [{ "index": ix, "item": item, "url": item.build_relative_url() } for (ix, item) in enumerate(repository.items) ]  
    model.item_count = len(model.items)

    return render_template("index.html", model = model)

@webapp.route("/uploader", methods = ["POST"])
def upload_file():
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

    #if request.method == "POST":
    #   first_name = request.form.get("fname")

    model = ViewModel()

    return redirect(url_for("index"))

@webapp.route("/act", methods=["POST"])
def do_action():

    if request.method == "POST":
        index = request.form.get("index")
        act = request.form.get("act")

    return redirect(url_for("index"))

@webapp.route("/add_image", methods=["POST"])
def add_image():

    #if request.method == "POST":
    #   first_name = request.form.get("fname")

    model = ViewModel()

    return redirect(url_for("index"))

@webapp.route("/add_html", methods=["POST"])
def add_html():

    #if request.method == "POST":
    #   first_name = request.form.get("fname")

    model = ViewModel()

    return redirect(url_for("index"))

@webapp.route("/new", methods=["GET"])
def new_item():
    model = ViewModel()

    staticfolder = f"{STATIC_FOLDER}{config.IMAGES_VIRTUAL_FOLDER}"
    model.available_images = sorted([f for f in listdir(staticfolder) if isfile(join(staticfolder, f)) and isimagefile(f)])
    model.available_htmls = sorted([f for f in listdir(staticfolder) if isfile(join(staticfolder, f)) and ishtmlfile(f)])

    return render_template("new.html", model = model)

@webapp.route("/htmlfile/<filename>")
def htmlfile(filename: str):
    return send_from_directory(f"static/{config.IMAGES_VIRTUAL_FOLDER}", filename)

@webapp.route("/image_centered/<image>/<bgcolor>")
def image_centered(image: str, bgcolor: str):
    model = ViewModel()

    model.background_color = bgcolor
    model.image_name = config.IMAGES_VIRTUAL_FOLDER + image

    return render_template("image_centered.html", model = model)

@webapp.route("/image_fullscreen/<image>/<bgcolor>")
def image_fs(image: str, bgcolor: str):
    model = ViewModel()

    model.background_color = bgcolor
    model.image_name = config.IMAGES_VIRTUAL_FOLDER + image

    return render_template("image_full_screen.html", model = model)

def ishtmlfile(filename):
    validextension = [".html", ".htm"]
    ext = filename[filename.rfind("."):]
    return ext in validextension

def isimagefile(filename):
    validextension = [".png", ".jpeg", ".jpg", ".gif"]
    ext = filename[filename.rfind("."):]
    return ext in validextension
