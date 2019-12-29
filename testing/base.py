from SHIMON.app import App

from SHIMON.api.unlock import unlock

class BaseTest:
	pwd="123"

	test_app=App()
	shimon=test_app.shimon

	_app_context=test_app.app.app_context()
	_request_context=test_app.app.test_request_context()

	def app_context(func):
		def with_app_context(self):
			with self._app_context:
				func(self)
		return with_app_context

	def request_context(func):
		def with_request_context(self):
			with self._request_context:
				func(self)
		return with_request_context

	def unlocked(func):
		def while_unlocked(self):
			unlock(self.shimon, {"unlock": self.pwd})
			func(self)
		return while_unlocked
