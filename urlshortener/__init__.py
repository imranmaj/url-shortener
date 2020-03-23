from gevent import monkey; monkey.patch_all()
##########
import os

from flask import Flask
from gevent.pywsgi import WSGIServer


app = Flask("app")
from . import routes # apply routes

def run():
    server = WSGIServer(("0.0.0.0", int(os.environ.get("PORT", 80))), app)
    server.serve_forever()