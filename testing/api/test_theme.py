from flask import Flask, Response

from SHIMON.api.unlock import unlock
from SHIMON.renderer import jsonify
from SHIMON.api.theme import theme

from testing.base import BaseTest

class TestTheme(BaseTest):
	@classmethod
	@BaseTest.request_context
	def setup_class(self):
		unlock(self.shimon, {"unlock": self.pwd})

	@BaseTest.request_context
	def test_valid_theme_returns_http_202(self):
		self.reset()
		assert theme(self.shimon, {"theme": "default"})[1]==202

	@BaseTest.request_context
	def test_valid_theme_sets_new_theme(self):
		self.reset()
		theme(self.shimon, {"theme": "solarized dark"})
		assert self.shimon.cache["theme"]=="solarized dark"
		assert self.shimon.theme=="solarized dark"

	@BaseTest.request_context
	def test_invalid_theme_returns_http_400(self):
		assert theme(self.shimon, {"theme": "not a theme"})[1]==400

	@BaseTest.request_context
	def test_invalid_theme_keeps_last_theme(self):
		self.reset()
		theme(self.shimon, {"theme": "not a theme"})

		assert self.shimon.theme=="default"
		assert self.shimon.cache["theme"]=="default"

	def reset(self):
		self.shimon.cache_mapper["theme"]="default"