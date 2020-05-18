from datetime import datetime, timedelta

from testing.base import BaseTest

# TODO: split up session code so it can be tested easier
class TestSession(BaseTest):
    @BaseTest.request_context
    @BaseTest.unlocked
    def test_kill_wipes_session(self) -> None:
        assert self.shimon.session.session

        self.shimon.session.kill()
        assert not self.shimon.session.session

    @BaseTest.request_context
    @BaseTest.unlocked
    def test_check_fails_when_missing_session(self) -> None:
        had_error = self.shimon.session.check({"not session": "", "redirect": False})
        assert had_error

    @BaseTest.request_context
    @BaseTest.unlocked
    def test_check_fails_with_incorrect_session(self) -> None:
        had_error = self.shimon.session.check({"session": "invalid", "redirect": False})
        assert had_error

    @BaseTest.request_context
    @BaseTest.unlocked
    def test_expired_session_ignores_session(self) -> None:
        self.shimon.session.keepalive()

        session_time_length = timedelta(seconds=self.shimon.session.expires + 1)

        self.shimon.session.lastcall = datetime.now() - session_time_length

        had_error = self.shimon.session.check(
            {"session": self.shimon.session.session, "redirect": False}
        )

        assert had_error
