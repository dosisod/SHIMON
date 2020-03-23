from werkzeug.http import dump_cookie

from SHIMON.app import App

from SHIMON.api.unlock import unlock
from SHIMON.api.lock import lock

from typing import Callable, Any

def add_data_if_cache_empty(self: "BaseTest") -> None:
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
	pwd="123" # nosec

	test_app=App()
	shimon=test_app.shimon

	_app_context=test_app.app.app_context
	_request_context=test_app.app.test_request_context

	#default data to use when cache is empty
	default_name="name"
	default_uuid="uuid"

	@staticmethod
	def app_context(func: Callable[..., None]) -> Callable[..., Any]:
		def with_app_context(self: BaseTest) -> None:
			with self._app_context(): # type: ignore
				func(self)

		return with_app_context

	@staticmethod
	def request_context(func: Callable[..., None]) -> Callable[..., Any]:
		def with_request_context(self: BaseTest) -> None:
			with self._request_context():
				func(self)

		return with_request_context

	@staticmethod
	def use_cookie(name: str, value: str) -> Callable[..., Any]:
		def make_cookie(func: Callable[..., Any]) -> Callable[..., Any]:
			def with_test_client(self: BaseTest, *args: Any) -> None:
				cookie=dump_cookie(name, value)
				with self._request_context(environ_base={"HTTP_COOKIE": cookie}):
					func(self, *args)

			return with_test_client
		return make_cookie

	@staticmethod
	def unlocked(func: Callable[..., None]) -> Callable[..., Any]:
		def while_unlocked(self: BaseTest) -> None:
			unlock(self.shimon, self.pwd, True)

			add_data_if_cache_empty(self)
			func(self)

			lock(self.shimon, self.pwd, True)

		return while_unlocked

	@staticmethod
	def allow_local(func: Callable[..., None]) -> Callable[..., Any]:
		def while_local(self: BaseTest) -> None:
			self.shimon.security._testing=True
			try:
				func(self)
			except AssertionError:
				self.shimon.security._testing=False
				raise

			self.shimon.security._testing=False
		return while_local
