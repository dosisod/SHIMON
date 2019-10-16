from flask import Flask, Response

from SHIMON.shimon import Shimon

from SHIMON.storage import unlock, lock, locker
from SHIMON.error import api_error
from flask.json import jsonify

class Test:
	pwd="123"
	ss=Shimon()
	app=Flask(__name__, static_url_path="")

	def test_storage(self):
		assert unlock(self.pwd)!="{}"

	def test_error(self):
		with self.app.app_context():
			assert api_error(200, "test1", True, False)=="test1"
			assert api_error(200, "test2", "true", False)=="test2"
			assert api_error(200, 1337, True, False)==1337
			assert api_error(200, ["test3"], True, False).json==jsonify(["test3"]).json
			assert api_error(200, None, False, True).json==jsonify({"rethrow":""}).json
			assert api_error(200, None, False, False).json==jsonify({"code":200,"msg":""}).json