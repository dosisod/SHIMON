from flask import Flask, request, render_template
from werkzeug.exceptions import HTTPException
from flask_restful import Resource, Api
from flask.json import jsonify
from waitress import serve

from security import check_local
from storage import unlock
from api import api_handle

from shimon import Shimon

app=Flask(__name__, static_url_path="")
shimon=Shimon()

@app.errorhandler(Exception)
def error(ex):
	return shimon.error(ex)

@app.route("/")
def index():
	return shimon.index()

@app.route("/msg")
def msg():
	return shimon.msg()

@app.route("/login")
def login():
	return shimon.login()

@app.route("/api/", methods=["POST"])
def api():
	return shimon.api()

if __name__=="__main__":
	serve(app, host="0.0.0.0", port=1717)