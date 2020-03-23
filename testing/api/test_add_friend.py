from SHIMON.api.add_friend import add_friend

from testing.base import BaseTest
from testing.util import assertHttpResponse

from typing import Dict
from SHIMON.__init__ import HttpResponse

class TestAddFriend(BaseTest):
	@BaseTest.request_context
	def test_invalid_data_returns_http_400(self) -> None:
		assertHttpResponse(
			self.add_friend("invalid"), # type: ignore
			400
		)

	@BaseTest.request_context
	@BaseTest.allow_local
	@BaseTest.unlocked
	def test_missing_name_param_returns_http_400(self) -> None:
		@BaseTest.use_cookie("session", self.shimon.session.session)
		def run(self: TestAddFriend) -> None:
			assertHttpResponse(
				self.add_friend({"id": "user id"}),
				400
			)

		run(self)

	@BaseTest.request_context
	@BaseTest.allow_local
	@BaseTest.unlocked
	def test_missing_id_param_returns_http_400(self) -> None:
		@BaseTest.use_cookie("session", self.shimon.session.session)
		def run(self: TestAddFriend) -> None:
			assertHttpResponse(
				self.add_friend({"name": "name"}),
				400
			)

		run(self)

	@BaseTest.request_context
	@BaseTest.allow_local
	@BaseTest.unlocked
	def test_adding_existing_friend_returns_http_400(self) -> None:
		user=self.shimon.cache["history"][0]

		@BaseTest.use_cookie("session", self.shimon.session.session)
		def run(self: TestAddFriend) -> None:
			assertHttpResponse(
				self.add_friend({
					"name": "anything",
					"id": user["id"]
				}
			), 400)

		run(self)

	@BaseTest.request_context
	@BaseTest.allow_local
	@BaseTest.unlocked
	def test_adding_new_friend_actually_adds_them(self) -> None:
		self.remove_tmp_friend()

		friends=len(self.shimon.cache["friends"])
		self.add_friend({
			"name": "whatever",
			"id": "testAdd"
		})

		assert len(self.shimon.cache["friends"])==friends + 1

		self.remove_tmp_friend()

	@BaseTest.request_context
	@BaseTest.allow_local
	@BaseTest.unlocked
	def test_adding_new_friend_returns_http_200(self) -> None:
		self.remove_tmp_friend()

		@BaseTest.use_cookie("session", self.shimon.session.session)
		def run(self: TestAddFriend) -> None:
			assertHttpResponse(
				self.add_friend({
					"name": "whatever",
					"id": "testAdd"
				}
			), code=200)

		run(self)

		self.remove_tmp_friend()

	@BaseTest.request_context
	@BaseTest.allow_local
	@BaseTest.unlocked
	def test_bad_uuid_regex_causes_http_400(self) -> None:
		@BaseTest.use_cookie("session", self.shimon.session.session)
		def check(self: TestAddFriend, uuid: str) -> None:
			assertHttpResponse(
				self.add_friend({
					"name": "whatever",
					"id": uuid
				}
			), code=400)

		check(self, "bad uuid")
		check(self, "")
		check(self, "\r\n")
		check(self, "bad!")

	def remove_tmp_friend(self) -> None:
		for i, friend in enumerate(self.shimon.cache["friends"]):
			if friend["id"]=="testAdd":
				del self.shimon.cache["friends"][i]
				break

		for i, history in enumerate(self.shimon.cache["history"]):
			if history["id"]=="testAdd":
				del self.shimon.cache["history"][i]
				break

	def add_friend(self, obj: Dict) -> HttpResponse:
		return add_friend(self.shimon, obj, False)
