from werkzeug.exceptions import HTTPException
from flask import Flask, Response

from SHIMON.shimon import Shimon

from typing import Union
from SHIMON.__init__ import Page, HttpResponse, AnyResponse

class App:
	IP="127.0.0.1"
	PORT=1717

	app=Flask(__name__, static_url_path="")
	shimon=Shimon()

	def __init__(self):
		@self.app.route("/error/<int:ex>") # type: ignore
		@self.app.errorhandler(Exception)
		def error(ex: Union[int, Exception]) -> HttpResponse:
			return self.shimon.error(ex)

		#using @user syntax the msg page will be rendered
		#if nothing is added, then the index will be rendered as normal
		@self.app.route("/") # type: ignore
		@self.app.route("/@<uuid>")
		def index(uuid: str="") -> HttpResponse:
			return self.shimon.index(uuid=uuid)

		@self.app.route("/settings") # type: ignore
		def settings() -> HttpResponse:
			return self.shimon.settings()

		@self.app.route("/account") # type: ignore
		def account() -> HttpResponse:
			return self.shimon.account()

		@self.app.route("/add") # type: ignore
		def add() -> HttpResponse:
			return self.shimon.add()

		@self.app.route("/login") # type: ignore
		def login() -> HttpResponse:
			return self.shimon.login()

		@self.app.route("/api/", methods=["POST"]) # type: ignore
		def api() -> AnyResponse:
			return self.shimon.api()