from SHIMON.api.expiration_timer import expiration_timer

from testing.base import BaseTest
from testing.util import assertHttpResponse

class TestExpirationTimer(BaseTest):
	@BaseTest.request_context
	def test_not_valid_int_returns_http_400(self):
		assertHttpResponse(
			self.expiration("not an int"),
			400
		)

	@BaseTest.request_context
	def test_oob_int_returns_http_400(self):
		assertHttpResponse(
			self.expiration("0"),
			400
		)

		assertHttpResponse(
			self.expiration("9999999"),
			400
		)

	@BaseTest.request_context
	def test_valid_int_returns_http_202(self):
		assertHttpResponse(
			self.expiration(str(self.shimon.session.expires)),
			202
		)

	@BaseTest.request_context
	def test_variables_updated_after_call(self):
		old_cache_value=self.shimon.cache["expiration"]
		old_session_value=self.shimon.session.expires

		self.expiration("1337")

		assert self.shimon.cache["expiration"]!=old_cache_value
		assert self.shimon.session.expires!=old_session_value

		self.shimon.cache["expiration"]=old_cache_value
		self.shimon.session.expires=old_session_value

	def expiration(self, num: str):
		return expiration_timer(self.shimon, num, False)
