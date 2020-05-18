from SHIMON.renderer import render, make_response
from SHIMON.api.api_base import ApiBase
from SHIMON.api.error import error_400

from typing import Optional, TYPE_CHECKING
from SHIMON import HttpResponse

if TYPE_CHECKING:
    from SHIMON.shimon import Shimon


class ApiLock(ApiBase):
    callname = "lock"

    def __init__(self) -> None:
        super().__init__()

    @ApiBase.str_required
    def entry(_, self: "Shimon", pwd: str, redirect: bool) -> HttpResponse:
        return lock(self, pwd, redirect)


def lock(self: "Shimon", pwd: str, redirect: bool) -> HttpResponse:
    # dont kill session unless user will be directed to login
    if not redirect:
        return error_400()

    returned_error = self.storage.lock(pwd)
    if returned_error:
        return returned_error

    # clean up object states
    self.cache.wipe()
    self.session.kill()

    res = make_response(
        render(self, "pages/login.jinja", error="Cache has been locked")
    )

    res.set_cookie("uname", "", expires=0)
    res.set_cookie("session", "", expires=0)

    return res, 200
