from SHIMON import storage

from testing.base import BaseTest

class TestStorage(BaseTest):
	def test_unlock(self):
		assert storage.unlock(self.pwd)!="{}"
