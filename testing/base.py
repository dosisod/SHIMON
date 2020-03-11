from werkzeug.http import dump_cookie

from SHIMON.app import App

from SHIMON.api.unlock import unlock
from SHIMON.api.lock import lock

def add_data_if_cache_empty(self):
	if len(self.shimon.cache["friends"]) > 0:
		return

	if len(self.shimon.cache["history"]) > 0:
		return

	self.shimon.cache["history"].append({
		"id": self.default_uuid,
		"msgs": [{
				"sending": True,
				"msg": "test msg"
		}]
	})

	self.shimon.cache["friends"].append({
		"id": self.default_uuid,
		"name": self.default_name
	})

class BaseTest:
	pwd="123"

	test_app=App()
	shimon=test_app.shimon

	_app_context=test_app.app.app_context
	_request_context=test_app.app.test_request_context

	#default data to use when cache is empty
	default_name="name"
	default_uuid="uuid"

	def app_context(func):
		def with_app_context(self):
			with self._app_context():
				func(self)

		return with_app_context

	def request_context(func):
		def with_request_context(self):
			with self._request_context():
				func(self)

		return with_request_context

	def use_cookie(name, value):
		def make_cookie(func):
			def with_test_client(self):
				cookie=dump_cookie(name, value)
				with self._request_context(environ_base={"HTTP_COOKIE": cookie}):
					func(self)

			return with_test_client
		return make_cookie

	def unlocked(func):
		def while_unlocked(self):
			unlock(self.shimon, self.pwd, True)

			add_data_if_cache_empty(self)
			func(self)

			lock(self.shimon, self.pwd, True)

		return while_unlocked

	def allow_local(func):
		def while_local(self):
			self.shimon.security._testing=True
			try:
				func(self)
			except AssertionError:
				self.shimon.security._testing=False
				raise

			self.shimon.security._testing=False
		return while_local
