import shutil

from SHIMON.api.nuke import nuke

from testing.util import assertHttpResponse
from testing.base import BaseTest

class TestNuke(BaseTest):
	@classmethod
	def setup_class(self):
		#make backup of cache file

		shutil.copy2(
			self.shimon.storage.filepath,
			self.shimon.storage.filepath + ".bak"
		)

	@classmethod
	def teardown_class(self):
		#restore old cache file

		shutil.move(
			self.shimon.storage.filepath + ".bak",
			self.shimon.storage.filepath
		)

	@BaseTest.request_context
	@BaseTest.unlocked
	def test_incorrect_pwd_returns_http_401(self):
		assertHttpResponse(
			nuke(self.shimon, "not the password", False),
			code=401
		)

	@BaseTest.request_context
	@BaseTest.unlocked
	def test_nuke_procedure(self):
		# used "key" as it is randomized when creating a fresh session
		old_key=self.shimon.cache["key"]

		assertHttpResponse(
			nuke(self.shimon, self.pwd, False),
			code=200
		)

		assert self.shimon.cache["key"]!=old_key
