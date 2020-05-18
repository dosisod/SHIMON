from SHIMON.api.error import error_200
from SHIMON.api.api_base import ApiBase

from typing import TYPE_CHECKING
from SHIMON import HttpResponse

if TYPE_CHECKING:
    from SHIMON.shimon import Shimon


class ApiStatus(ApiBase):
    callname = "status"
    unlock_required = False

    def __init__(self) -> None:
        super().__init__()

    def entry(_, self: "Shimon", __: None, redirect: bool) -> HttpResponse:
        return status(self, __, redirect)


def status(self: "Shimon", _: None, redirect: bool) -> HttpResponse:
    unlocked = not self.cache.is_empty()

    return error_200(
        {
            "version": self.VERSION,
            "unlocked": unlocked,
            "developer": self.developer,
            "msg policy": self.msg_policy if unlocked else None,
        },
        redirect,
    )
