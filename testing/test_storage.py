import os

from testing.base import BaseTest

class TestStorage(BaseTest):
	@BaseTest.request_context
	def test_correct_pwd_doesnt_return_none(self):
		assert self.shimon.storage.unlock(self.pwd)!=None

	@BaseTest.request_context
	def test_incorrect_pwd_returns_none(self):
		assert self.shimon.storage.unlock("not the password")==None

	@BaseTest.request_context
	def test_default_cache_path_exists(self):
		assert self.shimon.storage.cache_file_exists()==True

	@BaseTest.request_context
	def test_invalid_cache_path_doesnt_exist(self):
		assert self.shimon.storage.cache_file_exists("not a file")==False

	@BaseTest.request_context
	def test_cache_file_is_chmod_600_after_writing(self):
		cache=self.shimon.storage.filepath

		#manually set to chmod 777
		os.chmod(cache, 0o777)

		@BaseTest.unlocked
		def lock(self):
			pass

		lock(self)

		#make sure file is changed to chmod 600
		assert (os.stat(cache).st_mode & 0o777) == 0o600
