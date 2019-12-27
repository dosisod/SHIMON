from flask import Flask, Response
from flask.json import jsonify
import os

from SHIMON import storage
from SHIMON import api

from SHIMON.app import App

class Test:
	pwd="123"

	test_app=App()
	app_context=test_app.app.app_context()
	request_context=test_app.app.test_request_context()

	def test_storage(self):
		assert storage.unlock(self.pwd)!="{}"

	def test_error(self):
		with self.app_context:
			#test that True and "true" are treated the same
			assert api.error.error(200, "test1", True)[0]=="test1"

			#assert strings are returned as-is
			assert api.error.error(200, "test2", "true")[0]=="test2"

			#assert ints are returned as-is
			assert api.error.error(200, 1337, True)[0]==1337

			#assert lists are jsonified before returning
			assert api.error.error(200, ["test3"], True)[0].json==jsonify(["test3"]).json

			#assert that rethrow will return blank rethrow json
			assert api.error.error(200, None, False, True)[0].json==jsonify({"rethrow":""}).json

			#assert that an unreturnable type will be set to "" before sending back
			assert api.error.error(200, None, False)[0].json==jsonify({"code":200,"msg":""}).json

			#assert default error 200 msg is the same as the explicit call
			assert api.error.error_200()[0].json==api.error.error(200, "OK", False)[0].json

			#assert custom error 200 msg is the same as the explicit version
			assert api.error.error_200("test")[0].json==api.error.error(200, "test", False)[0].json

	def test_theme(self):
		with self.app_context, self.request_context:
			api.unlock.unlock(self.test_app.shimon, {"unlock":self.pwd})
			assert api.theme.theme(self.test_app.shimon, {"theme": "default"})[1]==202
			assert self.test_app.shimon.theme=="default"
			assert api.theme.theme(self.test_app.shimon, {"theme": "not a theme"})[1]==400
			assert self.test_app.shimon.theme=="default"