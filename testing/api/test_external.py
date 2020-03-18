from SHIMON.api.external import api_friends, api_recent, api_allfor, sha256hex

from testing.base import BaseTest

from typing import Dict, List

class TestApiFriends(BaseTest):
	@BaseTest.request_context
	@BaseTest.unlocked
	def test_hash_is_not_added_to_cache(self) -> None:
		for friend in self.shimon.cache["friends"]:
			assert "hash" not in friend

		api_friends(self.shimon)

		for friend in self.shimon.cache["friends"]:
			assert "hash" not in friend

class TestApiRecent(BaseTest):
	@BaseTest.request_context
	@BaseTest.unlocked
	def test_returned_data_is_valid(self) -> None:
		raw=api_recent(self.shimon)

		for recent in raw:
			assert "id" in recent
			assert recent["id"]
			assert "hash" in recent
			assert recent["hash"]

			assert "msgs" in recent
			assert "sending" in recent["msgs"][0]
			assert recent["msgs"][0]["sending"]!=None
			assert "msg" in recent["msgs"][0]

class TestApiAllfor(BaseTest):
	user: Dict[str, str]

	@classmethod
	@BaseTest.request_context
	@BaseTest.unlocked
	def setup_class(self) -> None:
		self.user=self.shimon.cache["friends"][0]

	@BaseTest.request_context
	@BaseTest.unlocked
	def test_invalid_user_returns_False(self) -> None:
		assert api_allfor(self.shimon, "not a valid user")==False

	@BaseTest.request_context
	@BaseTest.unlocked
	def test_redraw_disabled_returns_empty_array(self) -> None:
		self.shimon.redraw=False
		assert api_allfor(self.shimon, self.user["id"])==[]

	@BaseTest.request_context
	@BaseTest.unlocked
	def test_redraw_enabled_returns_user_data(self) -> None:
		self.shimon.redraw=True
		raw=api_allfor(self.shimon, self.user["id"])

		assert raw
		assert not isinstance(raw, List)

		assert "id" in raw
		assert raw["id"]

		assert "msgs" in raw
		assert raw["msgs"] or raw["msgs"]==[]

		assert "hash" in raw
		assert raw["hash"]

	@BaseTest.request_context
	@BaseTest.unlocked
	def test_redraw_is_disabled_after_running(self) -> None:
		self.shimon.redraw=True
		api_allfor(self.shimon, self.user["id"])
		assert self.shimon.redraw==False

class TestSha256hex(BaseTest):
	def test_bytes_and_strings_return_equal_data(self) -> None:
		assert sha256hex("123")==sha256hex(b"123")

	def test_sha256_against_known_hash(self) -> None:
		assert sha256hex("123")=="a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3"
