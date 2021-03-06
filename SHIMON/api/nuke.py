from SHIMON.api.error import error_401
from SHIMON.api.api_base import ApiBase

from typing import TYPE_CHECKING
from SHIMON import HttpResponse

if TYPE_CHECKING:
    from SHIMON.shimon import Shimon


class ApiNuke(ApiBase):
    callname = "nuke"

    def __init__(self) -> None:
        super().__init__()

    @ApiBase.str_required
    def entry(_, self: "Shimon", pwd: str, redirect: bool) -> HttpResponse:
        return nuke(self, pwd, redirect)


def nuke(self: "Shimon", pwd: str, redirect: bool) -> HttpResponse:
    if self.security.correct_pwd(pwd):
        self.storage.resetCache()
        return self.session.create()

    return error_401()
