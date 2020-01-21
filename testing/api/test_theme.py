from flask import Flask, Response

from SHIMON.api.unlock import unlock
from SHIMON.renderer import jsonify
from SHIMON.api.theme import theme

from testing.base import BaseTest

class TestTheme(BaseTest):
	@BaseTest.request_context
	def test_valid_theme_returns_http_202(self):
		self.reset()
		assert self.theme("default")[1]==202

	@BaseTest.request_context
	def test_valid_theme_sets_new_theme(self):
		self.reset()
		self.theme("solarized dark")

		assert self.shimon.cache["theme"]=="solarized dark"
		assert self.shimon.theme=="solarized dark"

	@BaseTest.request_context
	def test_invalid_theme_returns_http_400(self):
		assert self.theme("not a theme")[1]==400

	@BaseTest.request_context
	def test_invalid_theme_keeps_last_theme(self):
		self.reset()
		self.theme("not a theme")

		assert self.shimon.theme=="default"
		assert self.shimon.cache["theme"]=="default"

	@BaseTest.request_context
	def test_file_traversal_returns_http_400(self):
		self.reset()

		assert self.theme("../default")[1]==400

	def reset(self):
		self.shimon.cache_mapper["theme"]="default"

	def theme(self, obj):
		return theme(self.shimon, obj, True)