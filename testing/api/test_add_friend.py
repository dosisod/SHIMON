from SHIMON.api.add_friend import add_friend

from testing.base import BaseTest
from testing.util import assertHttpResponse

class TestAddFriend(BaseTest):
	@BaseTest.request_context
	def test_invalid_data_returns_http_400(self):
		assertHttpResponse(
			self.add_friend("invalid"),
			400
		)

	@BaseTest.request_context
	@BaseTest.allow_local
	@BaseTest.unlocked
	def test_missing_name_param_returns_http_400(self):
		@BaseTest.use_cookie("session", self.shimon.session.session)
		def run(self):
			assertHttpResponse(
				self.add_friend({"id": "user id"}),
				400
			)

		run(self)

	@BaseTest.request_context
	@BaseTest.allow_local
	@BaseTest.unlocked
	def test_missing_id_param_returns_http_400(self):
		@BaseTest.use_cookie("session", self.shimon.session.session)
		def run(self):
			assertHttpResponse(
				self.add_friend({"name": "name"}),
				400
			)

		run(self)

	@BaseTest.request_context
	@BaseTest.allow_local
	@BaseTest.unlocked
	def test_adding_existing_friend_returns_http_400(self):
		user=self.shimon.cache["history"][0]

		@BaseTest.use_cookie("session", self.shimon.session.session)
		def run(self):
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
	def test_adding_new_friend_actually_adds_them(self):
		self.remove_tmp_friend()

		friends=len(self.shimon.cache["friends"])
		self.add_friend({
			"name": "whatever",
			"id": "test add"
		})

		assert len(self.shimon.cache["friends"])==friends+1

		self.remove_tmp_friend()

	@BaseTest.request_context
	@BaseTest.allow_local
	@BaseTest.unlocked
	def test_adding_new_friend_returns_http_200(self):
		self.remove_tmp_friend()

		@BaseTest.use_cookie("session", self.shimon.session.session)
		def run(self):
			assertHttpResponse(
				self.add_friend({
					"name": "whatever",
					"id": "test add"
				}
			), code=200)

		run(self)

		self.remove_tmp_friend()

	def remove_tmp_friend(self):
		for i, friend in enumerate(self.shimon.cache["friends"]):
			if friend["id"]=="test add":
				del self.shimon.cache["friends"][i]
				break

		for i, history in enumerate(self.shimon.cache["history"]):
			if history["id"]=="test add":
				del self.shimon.cache["history"][i]
				break

	def add_friend(self, obj):
		return add_friend(self.shimon, obj, False)
