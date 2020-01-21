from SHIMON.api.send_msg import send_msg

from testing.base import BaseTest

class TestSendMsg(BaseTest):
	@classmethod
	@BaseTest.request_context
	@BaseTest.unlocked
	def setup_class(self):
		self.user=self.shimon.cache["history"][0]

	@BaseTest.request_context
	def test_invalid_data_returns_http_400(self):
		assert send_msg(self.shimon, "not valid", False)[1]==400

	@BaseTest.request_context
	def test_missing_uname_param_returns_http_400(self):
		assert send_msg(self.shimon, {"msg": "hello"}, False)[1]==400

	@BaseTest.request_context
	def test_missing_msg_param_returns_http_400(self):
		assert send_msg(self.shimon, {"uname": "user"}, False)[1]==400

	@BaseTest.request_context
	@BaseTest.unlocked
	def test_uname_not_in_friend_list_returns_http_400(self):
		assert self.send_msg_wrapper("hello", uname="not a valid uname")[1]==400

	@BaseTest.request_context
	def test_whitespace_only_msg_returns_http_400(self):
		assert self.send_msg_wrapper("   ")[1]==400

	@BaseTest.request_context
	@BaseTest.unlocked
	def test_sending_msg_adds_to_msgs(self):
		total_msgs=len(self.user["msgs"])

		self.send_msg_wrapper("testing 123")
		assert len(self.shimon.cache["history"][0]["msgs"])==total_msgs+1

		self.shimon.cache["history"][0]["msgs"].pop()

	def send_msg_wrapper(self, msg: str, uname: str=""):
		if not uname:
			uname=self.user["id"]

		return send_msg(self.shimon, {
			"msg": msg,
			"uname": uname
		}, False)
