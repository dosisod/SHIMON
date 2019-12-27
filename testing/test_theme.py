from flask import Flask, Response
import os

from SHIMON import api

from testing.base import BaseTest

from flask.json import jsonify
class TestTheme(BaseTest):
	@BaseTest.request_context
	def test_theme(self):
		api.unlock.unlock(self.shimon, {"unlock":self.pwd})
		assert api.theme.theme(self.shimon, {"theme": "default"})[1]==202
		assert self.shimon.theme=="default"
		assert api.theme.theme(self.shimon, {"theme": "not a theme"})[1]==400
		assert self.shimon.theme=="default"