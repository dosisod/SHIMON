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

	@BaseTest.request_context
	def test_reset_cache_actually_resets(self):
		self.shimon.storage.resetCache()

		#randomly generated, check something was added
		assert self.shimon.cache["key"]

		self.shimon.cache._cache.pop("key")

		assert self.shimon.cache._cache == {
			"friends": [],
			"history": [],
			"sha512": "3c9909afec25354d551dae21590bb26e38d53f2173b8d3dc3eee4c047e7ab1c1eb8b85103e3be7ba613b31bb5c9c36214dc9f14a42fd7a2fdb84856bca5c44c2",
			"expiration": 3600,
			"developer": False,
			"version": self.shimon.VERSION,
			"theme": "auto"
		}
