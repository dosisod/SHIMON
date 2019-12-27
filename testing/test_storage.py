from SHIMON import storage

from testing.base import BaseTest

class TestStorage(BaseTest):
	def test_correct_pwd_doesnt_return_none(self):
		assert storage.unlock(self.pwd)!=None

	def test_incorrect_pwd_returns_none(self):
		assert storage.unlock("not the password")==None
