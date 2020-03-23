from flask import abort, redirect, render_template, request

from . import app
from .db import DBInterface
from .exceptions import NoSuchUrlIdError


db_interface = DBInterface()

@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return response

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/shorten", methods=["POST"])
def shorten():
    try:
        url = request.form["url"]
    except KeyError:
        abort(400)
    else:
        url_id = db_interface.shorten_url(url)
        return render_template("shorten.html", short_url_prefix=request.host_url, url=url, url_id=url_id)

@app.route("/<url_id>", methods=["GET"])
def get_url(url_id):
    if url_id == "shorten":
        abort(405)
    
    try:
        url = db_interface.get_url_by_id(url_id)
    except NoSuchUrlIdError:
        abort(404)
    else:
        return redirect(url)