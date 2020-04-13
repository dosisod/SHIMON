from SHIMON.api.api_base import ApiBase

from testing.base import BaseTest
from testing.util import assertHttpResponse

class TestApiBase(BaseTest):
	@BaseTest.request_context
	@BaseTest.unlocked
	def test_object_creation(self) -> None:
		obj=ApiBase(self.shimon)

	def test_shimon_exists_on_instance(self) -> None:
		obj=ApiBase(self.shimon)

		assert obj.shimon

	def test_entry_dry_run(self) -> None:
		obj=ApiBase(self.shimon)
		obj.entry(None, False)
