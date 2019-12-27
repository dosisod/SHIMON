from flask import Flask, Response
import os

from SHIMON import api

from testing.base import BaseTest

class TestTheme(BaseTest):
	def test_theme(self):
		with self.app_context, self.request_context:
			api.unlock.unlock(self.test_app.shimon, {"unlock":self.pwd})
			assert api.theme.theme(self.test_app.shimon, {"theme": "default"})[1]==202
			assert self.test_app.shimon.theme=="default"
			assert api.theme.theme(self.test_app.shimon, {"theme": "not a theme"})[1]==400
			assert self.test_app.shimon.theme=="default"