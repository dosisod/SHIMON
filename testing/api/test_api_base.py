from SHIMON.api.api_base import ApiBase
from SHIMON.api.api_calls import apicalls

from testing.base import BaseTest
from testing.util import assertHttpResponse

class TestApiBase(BaseTest):
	@BaseTest.request_context
	@BaseTest.unlocked
	def test_object_creation(self) -> None:
		obj=ApiBase()

	def test_entry_dry_run(self) -> None:
		obj=ApiBase()
		obj.entry(self.shimon, None, False)

def test_all_api_calls() -> None:
	for apicall in apicalls.values():
		assert apicall.callname
