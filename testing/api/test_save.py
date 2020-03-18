from SHIMON.api.save import save as _save

from testing.base import BaseTest
from testing.util import assertHttpResponse

from SHIMON.__init__ import HttpResponse

class TestSave(BaseTest):
	@BaseTest.request_context
	@BaseTest.unlocked
	def test_invalid_pwd_returns_http_401(self) -> None:
		assertHttpResponse(
			self.save("not the password"),
			401
		)

	@BaseTest.request_context
	@BaseTest.unlocked
	def test_valid_password_returns_http_200(self) -> None:
		assertHttpResponse(
			self.save(self.pwd),
			200
		)

	@BaseTest.request_context
	@BaseTest.unlocked
	def test_valid_password_updates_variables(self) -> None:
		self.shimon.msg_policy= -1
		self.shimon.session.expires= -1

		old=self.shimon.developer
		self.shimon.developer=not old

		self.save(self.pwd)

		assert self.shimon.msg_policy is not -1
		assert self.shimon.session.expires is not -1
		assert self.shimon.developer==old

	def save(self, pwd: str) -> HttpResponse:
		return _save(self.shimon, pwd, False)
