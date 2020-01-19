from SHIMON.api.delete_msg import delete_msg

from testing.base import BaseTest

class TestDeleteMsg(BaseTest):
	@classmethod
	@BaseTest.request_context
	@BaseTest.unlocked
	def setup_class(self):
		self.user=self.shimon.cache["history"][0]

	@BaseTest.request_context
	def test_invalid_data_returns_http_400(self):
		assert self.delete_msg("")[1]==400

	@BaseTest.request_context
	def test_missing_id_param_returns_http_400(self):
		assert self.delete_msg({"index": "0"})[1]==400

	@BaseTest.request_context
	def test_missing_index_param_returns_http_400(self):
		assert self.delete_msg({"id": "test id"})[1]==400

	@BaseTest.request_context
	@BaseTest.unlocked
	def test_missing_password_param_returns_http_401(self):
		self.shimon.msg_policy=1

		assert self.delete_msg({
				"id": self.user["id"],
				"index": "0",
				"pwd": "not the password"
			})[1]==401

	@BaseTest.request_context
	@BaseTest.unlocked
	def test_invalid_index_returns_http_400(self):
		assert self.delete_msg({
			"id": self.user["id"],
			"index": "-1",
			"pwd": self.pwd
		})[1]==400

	def delete_msg(self, obj):
		return delete_msg(self.shimon, obj, False)
