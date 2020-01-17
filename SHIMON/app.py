from werkzeug.exceptions import HTTPException
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

		#using @user syntax the msg page will be rendered
		#if nothing is added, then the index will be rendered as normal
		@self.app.route("/")
		@self.app.route("/@<uuid>")
		def index(uuid: str="") -> Page:
			return self.shimon.index(uuid=uuid)

		@self.app.route("/settings")
		def settings() -> Page:
			return self.shimon.settings()

		@self.app.route("/account")
		def account() -> Page:
			return self.shimon.account()

		@self.app.route("/add")
		def add() -> Page:
			return self.shimon.add()

		@self.app.route("/login")
		def login() -> Page:
			return self.shimon.login()

		@self.app.route("/api/", methods=["POST"])
		def api() -> Union[Page, Json]:
			return self.shimon.api()