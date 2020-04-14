from SHIMON.api.send_msg import ApiSendMsg

from testing.base import BaseTest
from testing.util import assertHttpResponse

from SHIMON.__init__ import History, HttpResponse

class TestSendMsg(BaseTest):
	user: History

	@classmethod
	@BaseTest.request_context
	@BaseTest.unlocked
	def setup_class(self) -> None:
		self.user=self.shimon.cache["history"][0]

	@BaseTest.request_context
	def test_invalid_data_returns_http_400(self) -> None:
		assertHttpResponse(
			ApiSendMsg().entry(self.shimon, "not valid", False), # type: ignore
			400
		)

	@BaseTest.request_context
	def test_missing_uname_param_returns_http_400(self) -> None:
		assertHttpResponse(
			ApiSendMsg().entry(self.shimon, {"msg": "hello"}, False),
			400
		)

	@BaseTest.request_context
	def test_missing_msg_param_returns_http_400(self) -> None:
		assertHttpResponse(
			ApiSendMsg().entry(self.shimon, {"uname": "user"}, False),
			400
		)

	@BaseTest.request_context
	@BaseTest.unlocked
	def test_uname_not_in_friend_list_returns_http_400(self) -> None:
		assertHttpResponse(
			self.send_msg_wrapper("hello", uname="not a valid uname"),
			400
		)

	@BaseTest.request_context
	def test_whitespace_only_msg_returns_http_400(self) -> None:
		assertHttpResponse(
			self.send_msg_wrapper("   "),
			400
		)

	@BaseTest.request_context
	def test_empty_msg_or_uname_returns_http_400(self) -> None:
		assertHttpResponse(
			ApiSendMsg().entry(self.shimon, {
				"uname": "whatever",
				"msg": None
			}, False),
			400
		)

		assertHttpResponse(
			ApiSendMsg().entry(self.shimon, {
				"uname": None,
				"msg": "whatever"
			}, False),
			400
		)

	@BaseTest.request_context
	@BaseTest.unlocked
	def test_sending_msg_adds_to_msgs(self) -> None:
		total_msgs=len(self.user["msgs"])

		self.send_msg_wrapper("testing 123")
		assert len(self.shimon.cache["history"][0]["msgs"])==total_msgs + 1

		self.shimon.cache["history"][0]["msgs"].pop()

	def send_msg_wrapper(self, msg: str, uname: str="") -> HttpResponse:
		if not uname:
			uname=self.user["id"]

		return ApiSendMsg().entry(self.shimon, {
			"msg": msg,
			"uname": uname
		}, False)
