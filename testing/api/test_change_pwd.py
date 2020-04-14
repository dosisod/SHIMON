from SHIMON.api.change_pwd import ApiChangePwd

from testing.base import BaseTest
from testing.util import assertHttpResponse

from typing import Dict
from SHIMON.__init__ import HttpResponse

class TestChangePwd(BaseTest):
	@BaseTest.request_context
	def test_invalid_data_returns_http_400(self) -> None:
		assertHttpResponse(
			self.change_pwd("invalid data"), # type: ignore
			400
		)

	@BaseTest.request_context
	def test_missing_oldpwd_param_returns_http_400(self) -> None:
		assertHttpResponse(
			self.change_pwd({"new": "321"}),
			400
		)

	@BaseTest.request_context
	def test_missing_newpwd_param_returns_http_400(self) -> None:
		assertHttpResponse(
			self.change_pwd({"old": "123"}),
			400
		)

	@BaseTest.request_context
	@BaseTest.unlocked
	def test_invalid_pwd_returns_http_401(self) -> None:
		assertHttpResponse(
			self.change_pwd({"old": "not the password", "new": "321"}),
			401
		)

	@BaseTest.request_context
	@BaseTest.unlocked
	def test_correct_pwd_returns_http_202(self) -> None:
		assertHttpResponse(
			self.change_pwd({"old": "123", "new": "123"}),
			202
		)

	@BaseTest.request_context
	@BaseTest.unlocked
	def test_correct_pwd_updates_cache_sha512(self) -> None:
		assert self.shimon.security.correct_pwd("new_pwd")==False

		self.change_pwd({"old": "123", "new": "new_pwd"})

		assert self.shimon.security.correct_pwd("new_pwd")==True

	def change_pwd(self, obj: Dict) -> HttpResponse:
		return ApiChangePwd().entry(self.shimon, obj, True)
