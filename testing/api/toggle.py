from pathlib import Path
import shutil

from testing.base import BaseTest
from testing.http import assertHttpResponse

from SHIMON import HttpResponse


class FreshToggle(BaseTest):
    path = ""
    name = ""

    def func(self, enable: bool) -> HttpResponse:
        pass

    @BaseTest.request_context
    def test_not_having_fresh_file_ignores_value(self) -> None:
        self.run_without_fresh_file()
        self.assertValue(False)

    @BaseTest.request_context
    def test_enabling_without_having_fresh_file_returns_http_400(self) -> None:
        assertHttpResponse(self.run_without_fresh_file(), 400)

    @BaseTest.request_context
    def test_having_fresh_file_accepts_value(self) -> None:
        self.run_with_fresh_file()
        self.assertValue(True)

    @BaseTest.request_context
    def test_enabling_with_fresh_file_returns_http_200(self) -> None:
        assertHttpResponse(self.run_with_fresh_file(), 200)

    @BaseTest.request_context
    def test_disabled_when_set_to_false(self) -> None:
        self.shimon.cache.mapper[self.name] = False

        self.func(False)

        self.assertValue(False)

    @BaseTest.request_context
    def test_non_bool_input_returns_http_400(self) -> None:
        not_a_bool = 123

        assertHttpResponse(
            self.func(not_a_bool),  # type: ignore
            400,
        )

    def test_sane_path_and_name_values(self) -> None:
        assert self.path
        assert self.name

    def assertValue(self, value: bool) -> None:
        assert (
            getattr(
                self.shimon,
                self.shimon.cache.mapper.cache_names[self.name],  # type: ignore
            )
            == value
        )

        assert self.shimon.cache[self.name] == value

    def run_without_fresh_file(self) -> HttpResponse:
        self.shimon.cache.mapper[self.name] = False

        if Path(self.path).is_file():
            backup_file = f"{self.path}.bak"

            shutil.move(self.path, backup_file)
            ret = self.func(True)
            shutil.move(backup_file, self.path)

        else:
            ret = self.func(True)

        return ret

    def run_with_fresh_file(self) -> HttpResponse:
        self.shimon.cache.mapper[self.name] = False

        if not Path(self.path).is_file():
            Path(self.path).touch()
            ret = self.func(True)
            Path(self.path).unlink()

        else:
            ret = self.func(True)

        return ret
