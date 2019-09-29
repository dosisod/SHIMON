from werkzeug.exceptions import HTTPException
from flask_restful import Resource, Api
from flask import Flask, Response
from waitress import serve

from shimon import Shimon

from typing import Union

Page=Union[Response, str] #can be a flask response or raw html response
Json=Response #json returned from api_error is still a Response, alias it to make sense

IP="127.0.0.1"
PORT=1717

app=Flask(__name__, static_url_path="")
shimon=Shimon()

@app.route("/error/<int:ex>")
@app.errorhandler(Exception)
def error(ex: Union[int, Exception]) -> Page:
	return shimon.error(ex)

@app.route("/")
def index() -> Page:
	return shimon.index()

@app.route("/settings")
def settings() -> Page:
	return shimon.settings()

@app.route("/account")
def account() -> Page:
	return shimon.account()

@app.route("/msg/<uuid>")
def msg(uuid: str) -> Page:
	return shimon.msg(uuid)

@app.route("/add")
def add() -> Page:
	return shimon.add()

@app.route("/login")
def login() -> Page:
	return shimon.login()

@app.route("/api/", methods=["POST"])
def api() -> Union[Page, Json]:
	return shimon.api()

if __name__=="__main__":
	print("starting SHIMON v"+shimon.VERSION+" -> github.com/dosisod/SHIMON")
	print("")

	try:
		serve(app, host=IP, port=PORT, threads=6)

	except OSError:
		print("Could not bind to port "+str(PORT))
		print("Is SHIMON already running? if not, check port "+str(PORT)+" availability")