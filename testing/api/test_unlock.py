from SHIMON.api.unlock import unlock as _unlock
from SHIMON.api.lock import lock

from testing.base import BaseTest
from testing.util import assertHttpResponse

from SHIMON.__init__ import HttpResponse

class TestUnlock(BaseTest):
	def setup_method(self) -> None:
		self.shimon.login_limiter.reset()

	def teardown_method(self) -> None:
		self.shimon.login_limiter.reset()

	@BaseTest.request_context
	def test_incorrect_pwd_adds_to_attempts(self) -> None:
		self.unlock("not the password")

		assert self.shimon.login_limiter.attempts==1

	@BaseTest.request_context
	def test_valid_pwd_ignored_when_in_cooldown(self) -> None:
		self.unlock("invalid pwd 1")
		self.unlock("invalid pwd 2")
		self.unlock("invalid pwd 3")

		self.unlock(self.pwd)

		assert self.shimon.login_limiter.in_cooldown()

	@BaseTest.request_context
	def test_correct_pwd_resets_login_limiter(self) -> None:
		self.shimon.login_limiter.attempts==1
		self.shimon.login_limiter.cooldown_start==1

		self.unlock(self.pwd)

		assert self.shimon.login_limiter.attempts==0
		assert self.shimon.login_limiter.cooldown_start==0

	@BaseTest.request_context
	def test_mistached_versions_shows_warning_page(self) -> None:
		old_version=self.shimon.VERSION
		self.shimon.VERSION="different version"

		unlocked_html=self.unlock(self.pwd)[0].data
		lock(self.shimon, self.pwd, False)

		warn_html=self.shimon.session.create(
			target="pages/warn.jinja"
		)[0].data

		self.shimon.cache.mapper["version"]=old_version
		lock(self.shimon, self.pwd, False)

		assert unlocked_html==warn_html

	@BaseTest.request_context
	def test_invalid_pwd_returns_http_401(self) -> None:
		assertHttpResponse(
			self.unlock("not the pwd"),
			401
		)

	def unlock(self, pwd: str) -> HttpResponse:
		return _unlock(
			self.shimon,
			pwd,
			redirect=False
		)
