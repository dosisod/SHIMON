from SHIMON.api.save import save

from testing.base import BaseTest
from testing.util import assertHttpResponse

class TestSave(BaseTest):
	@BaseTest.request_context
	@BaseTest.unlocked
	def test_invalid_pwd_returns_http_401(self):
		assertHttpResponse(
			self.save("not the password"),
			401
		)

	@BaseTest.request_context
	@BaseTest.unlocked
	def test_valid_password_returns_http_200(self):
		assertHttpResponse(
			self.save(self.pwd),
			200
		)

	@BaseTest.request_context
	@BaseTest.unlocked
	def test_valid_password_updates_variables(self):
		self.shimon.msg_policy=None
		self.shimon.session.expires=None
		self.shimon.developer=None

		self.save(self.pwd)

		assert self.shimon.msg_policy!=None
		assert self.shimon.session.expires!=None
		assert self.shimon.developer!=None

	def save(self, pwd: str):
		return save(self.shimon, pwd, False)
