from SHIMON.api.delete_msg import delete_msg

from testing.base import BaseTest
from testing.util import assertHttpResponse

from typing import Dict
from SHIMON.__init__ import History, HttpResponse

class TestDeleteMsg(BaseTest):
	user: History

	@classmethod
	@BaseTest.request_context
	@BaseTest.unlocked
	def setup_class(self) -> None:
		self.user=self.shimon.cache["history"][0]

	@BaseTest.request_context
	def test_invalid_data_returns_http_400(self) -> None:
		assertHttpResponse(
			self.delete_msg(""), # type: ignore
			400
		)

	@BaseTest.request_context
	@BaseTest.unlocked
	def test_missing_id_param_returns_http_400(self) -> None:
		assertHttpResponse(
			self.delete_msg({"index": "0"}),
			400
		)

	@BaseTest.request_context
	def test_missing_index_param_returns_http_400(self) -> None:
		assertHttpResponse(
			self.delete_msg({"id": "test id"}),
			400
		)

	@BaseTest.request_context
	@BaseTest.unlocked
	def test_missing_password_with_policy_1_returns_http_401(self) -> None:
		old_policy=self.shimon.msg_policy
		self.shimon.cache.mapper["msg policy"]=1

		assertHttpResponse(
			self.delete_msg({
				"id": self.user["id"],
				"index": "0",
				"pwd": "not the password"
			}),
			401
		)

		self.shimon.cache.mapper["msg policy"]=old_policy

	@BaseTest.request_context
	def test_invalid_index_returns_http_400(self) -> None:
		assertHttpResponse(
			self.delete_msg({
				"id": self.user["id"],
				"index": "-1",
				"pwd": self.pwd
			}),
			400
		)

	def delete_msg(self, obj: Dict) -> HttpResponse:
		return delete_msg(self.shimon, obj, False)
