from werkzeug.exceptions import HTTPException
from flask import Flask, Response

from SHIMON.shimon import Shimon

from typing import Union
from SHIMON.__init__ import HttpResponse

class App:
	IP="127.0.0.1"
	PORT=1717

	app=Flask(__name__, static_url_path="")
	shimon=Shimon()

	def __init__(self) -> None:
		@self.app.route("/error/<int:ex>")
		@self.app.errorhandler(Exception)
		def error(ex: Union[int, Exception]) -> HttpResponse:
			return self.shimon.error(ex)

		#using @user syntax the msg page will be rendered
		#if nothing is added, then the index will be rendered as normal
		@self.app.route("/")
		@self.app.route("/@<uuid>")
		def index(uuid: str="") -> HttpResponse:
			if uuid:
				return self.shimon.msg(uuid)

			return self.shimon.index()

		@self.app.route("/settings")
		def settings() -> HttpResponse:
			return self.shimon.settings()

		@self.app.route("/account")
		def account() -> HttpResponse:
			return self.shimon.account()

		@self.app.route("/add")
		def add() -> HttpResponse:
			return self.shimon.add()

		@self.app.route("/login")
		def login() -> HttpResponse:
			return self.shimon.login()

		@self.app.route("/api/", methods=["POST"])
		def api() -> HttpResponse:
			return self.shimon.api()