from SHIMON.api.expiration_timer import expiration_timer

from testing.base import BaseTest

class TestExpirationTimer(BaseTest):
	@BaseTest.request_context
	@BaseTest.unlocked
	def test_not_valid_int_returns_http_400(self):
		assert self.expiration_wrapper("not an int")[1]==400

	@BaseTest.request_context
	@BaseTest.unlocked
	def test_oob_int_returns_http_400(self):
		assert self.expiration_wrapper("0")[1]==400
		assert self.expiration_wrapper("9999999")[1]==400

	@BaseTest.request_context
	@BaseTest.unlocked
	def test_valid_int_returns_http_202(self):
		assert self.expiration_wrapper(str(self.shimon.session.expires))[1]==202

	@BaseTest.request_context
	@BaseTest.unlocked
	def test_variables_updated_after_call(self):
		old_cache_value=self.shimon.cache["expiration"]
		old_session_value=self.shimon.session.expires

		self.expiration_wrapper("1337")

		assert self.shimon.cache["expiration"]!=old_cache_value
		assert self.shimon.session.expires!=old_session_value

		self.shimon.cache["expiration"]=old_cache_value
		self.shimon.session.expiration=old_session_value

	def expiration_wrapper(self, num: str):
		return expiration_timer(self.shimon, {"expiration timer": num})
