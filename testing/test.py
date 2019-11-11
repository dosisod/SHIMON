from flask import Flask, Response
from flask.json import jsonify
import os

from SHIMON.storage import unlock, lock, locker
from SHIMON.renderer import render
from SHIMON.error import api_error
from SHIMON.api import api_handle
from SHIMON.shimon import Shimon

class Test:
	pwd="123"
	ss=Shimon()
	app=Flask(__name__, static_url_path="")

	def test_storage(self):
		assert unlock(self.pwd)!="{}"

	def test_error(self):
		with self.app.app_context():
			#test that True and "true" are treated the same
			#assert strings are returned as-is
			assert api_error(200, "test1", True)[0]=="test1"
			assert api_error(200, "test2", "true")[0]=="test2"

			#assert ints are returned as-is
			assert api_error(200, 1337, True)[0]==1337

			#assert lists are jsonified before returning
			assert api_error(200, ["test3"], True)[0].json==jsonify(["test3"]).json

			#assert that rethrow will return blank rethrow json
			assert api_error(200, None, False, True)[0].json==jsonify({"rethrow":""}).json

			#assert that an unreturnable type will be set to "" before sending back
			assert api_error(200, None, False)[0].json==jsonify({"code":200,"msg":""}).json