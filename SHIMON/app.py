from werkzeug.exceptions import HTTPException
from flask_restful import Resource, Api
from flask import Flask, Response

from SHIMON.shimon import Shimon

from typing import Union
from SHIMON.__init__ import Page, Json

class App:
	IP="127.0.0.1"
	PORT=1717

	app=Flask(__name__, static_url_path="")
	shimon=Shimon()

	def __init__(self):
		@self.app.route("/error/<int:ex>")
		@self.app.errorhandler(Exception)
		def error(ex: Union[int, Exception]) -> Page:
			return self.shimon.error(ex)

		@self.app.route("/")
		def index() -> Page:
			return self.shimon.index()

		@self.app.route("/settings")
		def settings() -> Page:
			return self.shimon.settings()

		@self.app.route("/account")
		def account() -> Page:
			return self.shimon.account()

		@self.app.route("/msg/<uuid>")
		def msg(uuid: str) -> Page:
			return self.shimon.msg(uuid)

		@self.app.route("/add")
		def add() -> Page:
			return self.shimon.add()

		@self.app.route("/login")
		def login() -> Page:
			return self.shimon.login()

		@self.app.route("/api/", methods=["POST"])
		def api() -> Union[Page, Json]:
			return self.shimon.api()

"""
if __name__=="__main__":
	a=App()

	print("starting SHIMON v"+a.shimon.VERSION+" -> github.com/dosisod/SHIMON")
	print("")

	try:
		serve(a.app, host=a.IP, port=a.PORT, threads=6)

	except OSError:
		print("Could not bind to port "+str(a.PORT))
		print("Is SHIMON already running? if not, check port "+str(a.PORT)+" availability")
"""