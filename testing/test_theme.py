from flask import Flask, Response
import os

from SHIMON import api

from testing.base import BaseTest

from flask.json import jsonify
class TestTheme(BaseTest):
	@classmethod
	@BaseTest.request_context
	def setup_class(self):
		api.unlock.unlock(self.shimon, {"unlock":self.pwd})

	@BaseTest.request_context
	def test_valid_theme_returns_http_202(self):
		self.reset()
		assert api.theme.theme(self.shimon, {"theme": "default"})[1]==202

	@BaseTest.request_context
	def test_valid_theme_sets_new_theme(self):
		self.reset()
		api.theme.theme(self.shimon, {"theme": "solarized dark"})
		assert self.shimon.theme=="solarized dark"

	@BaseTest.request_context
	def test_invalid_theme_returns_http_400(self):
		assert api.theme.theme(self.shimon, {"theme": "not a theme"})[1]==400

	@BaseTest.request_context
	def test_invalid_theme_keeps_last_theme(self):
		self.reset()
		api.theme.theme(self.shimon, {"theme": "not a theme"})
		assert self.shimon.theme=="default"

	def reset(self):
		self.shimon.theme="default"