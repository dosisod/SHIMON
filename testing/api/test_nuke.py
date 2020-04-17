import shutil

from SHIMON.api.nuke import ApiNuke

from testing.http import assertHttpResponse
from testing.base import BaseTest

class TestNuke(BaseTest):
	@classmethod
	def setup_class(self) -> None:
		#make backup of cache file

		shutil.copy2(
			self.shimon.storage.filepath,
			self.shimon.storage.filepath + ".bak"
		)

	@classmethod
	def teardown_class(self) -> None:
		#restore old cache file

		shutil.move(
			self.shimon.storage.filepath + ".bak",
			self.shimon.storage.filepath
		)

	@BaseTest.request_context
	@BaseTest.unlocked
	def test_incorrect_pwd_returns_http_401(self) -> None:
		assertHttpResponse(
			ApiNuke().entry(self.shimon, "not the password", False),
			code=401
		)

	@BaseTest.request_context
	@BaseTest.unlocked
	def test_nuke_procedure(self) -> None:
		# used "key" as it is randomized when creating a fresh session
		old_key=self.shimon.cache["key"]

		assertHttpResponse(
			ApiNuke().entry(self.shimon, self.pwd, False),
			code=200
		)

		assert self.shimon.cache["key"]!=old_key

	@BaseTest.request_context
	def test_non_str_input_returns_http_400(self) -> None:
		not_a_str=123

		assertHttpResponse(
			ApiNuke().entry(self.shimon, not_a_str, False),
			code=400
		)
