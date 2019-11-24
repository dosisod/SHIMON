from flask import Flask, Response
from flask.json import jsonify
import os

from SHIMON.storage import unlock, lock, locker
from SHIMON.api.handle import handler
from SHIMON.renderer import render
from SHIMON.api.error import error

from SHIMON.app import App

class Test:
	pwd="123"

	app=App()

	def test_storage(self):
		assert unlock(self.pwd)!="{}"

	def test_error(self):
		with self.app.app.app_context():
			#test that True and "true" are treated the same
			#assert strings are returned as-is
			assert error(200, "test1", True)[0]=="test1"
			assert error(200, "test2", "true")[0]=="test2"

			#assert ints are returned as-is
			assert error(200, 1337, True)[0]==1337

			#assert lists are jsonified before returning
			assert error(200, ["test3"], True)[0].json==jsonify(["test3"]).json

			#assert that rethrow will return blank rethrow json
			assert error(200, None, False, True)[0].json==jsonify({"rethrow":""}).json

			#assert that an unreturnable type will be set to "" before sending back
			assert error(200, None, False)[0].json==jsonify({"code":200,"msg":""}).json