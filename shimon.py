from flask import Flask, request, render_template
from werkzeug.exceptions import HTTPException
from flask_restful import Resource, Api
from flask.json import jsonify
from waitress import serve

from security import check_local
from storage import unlock
from api import api_handle

app=Flask(__name__, static_url_path="")

@app.errorhandler(Exception)
def error(ex):
	err=500
	if isinstance(ex, HTTPException):
		err=ex.code
	return render_template("error.html", error=err)

@app.route("/")
def index():
	check_local()
	return render_template("index.html")

@app.route("/login")
def login():
	check_local()
	return render_template("login.html")

@app.route("/api/", methods=["GET"])
def auth():
	check_local()

	data=request.args.to_dict()
	return api_handle(data)

if __name__=="__main__":
	serve(app, host="0.0.0.0", port=1717)