import json

from SHIMON.api.status import status

from testing.base import BaseTest
from testing.util import assertHttpResponse

class TestStatus(BaseTest):
	@BaseTest.request_context
	def test_always_returns_http_200(self):
		assertHttpResponse(
			self.status("true"),
			200
		)

	@BaseTest.request_context
	def test_that_redirect_flag_doesnt_change_output(self):
		assert self.status("true")[0].json== \
			json.loads(self.status("false")[0].data)["msg"]

	def status(self, redirect: str):
		return status(self.shimon, None, redirect)
