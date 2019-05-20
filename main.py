from werkzeug.exceptions import HTTPException
from flask_restful import Resource, Api
from waitress import serve
from flask import Flask

from shimon import Shimon

app=Flask(__name__, static_url_path="")
shimon=Shimon()

@app.route("/error/<int:ex>")
@app.errorhandler(Exception)
def error(ex):
	return shimon.error(ex)

@app.route("/")
def index():
	return shimon.index()

@app.route("/settings")
def settings():
	return shimon.settings()

@app.route("/msg/<uuid>")
def msg(uuid):
	return shimon.msg(uuid)

@app.route("/login")
def login():
	return shimon.login()

@app.route("/api/", methods=["POST"])
def api():
	return shimon.api()

if __name__=="__main__":
	serve(app, host="0.0.0.0", port=1717, threads=6)