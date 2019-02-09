from flask import Flask, request, send_from_directory, render_template
from flask_restful import Resource, Api
from flask.json import jsonify
from waitress import serve

app=Flask(__name__, static_url_path="")

@app.route("/")
def index():
	return render_template("index.html")

@app.route("/api/", methods=["POST"])
def auth():
	data=requests.args.post("id") #for testing
	return jsonify({"msg":"good"})

if __name__=="__main__":
	serve(app, host="0.0.0.0", port=1717)