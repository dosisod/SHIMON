from SHIMON.api.add_friend import add_friend

from testing.base import BaseTest

class TestAddFriend(BaseTest):
	@BaseTest.request_context
	@BaseTest.unlocked
	def test_invalid_data_returns_http_400(self):
		assert self.add_friend("invalid")[1]==400

	@BaseTest.request_context
	@BaseTest.allow_local
	@BaseTest.unlocked
	def test_missing_name_param_returns_http_400(self):
		assert self.add_friend({"id": "user id"})[1]==400

	@BaseTest.request_context
	@BaseTest.allow_local
	@BaseTest.unlocked
	def test_missing_id_param_returns_http_400(self):
		assert self.add_friend({"name": "name"})[1]==400

	@BaseTest.request_context
	@BaseTest.allow_local
	@BaseTest.unlocked
	def test_adding_existing_friend_returns_http_400(self):
		user=self.shimon.cache["history"][0]

		assert self.add_friend({
			"name": "anything",
			"id": user["id"]
		})[1]==400

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

		assert self.add_friend({
			"name": "whatever",
			"id": "test add"
		})[1]==200

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
