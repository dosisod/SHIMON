import re

from SHIMON.api.api_base import ApiBase
from SHIMON.api.error import error_400

from typing import Dict, TYPE_CHECKING
from SHIMON import HttpResponse

if TYPE_CHECKING:
    from SHIMON.shimon import Shimon


class ApiAddFriend(ApiBase):
    callname = "add friend"

    def __init__(self) -> None:
        super().__init__()

    @ApiBase.dict_required
    def entry(_, self: "Shimon", adding: Dict, redirect: bool) -> HttpResponse:
        return add_friend(self, adding, redirect)


def add_friend(self: "Shimon", adding: Dict, redirect: bool) -> HttpResponse:
    name = adding.get("name")
    _id = adding.get("id")

    # make sure that name and id are valid
    if not name or not _id or not re.search("^[a-zA-z0-9]+$", _id):
        return self.index(error="Invalid Request", code=400)

    # make sure id is not already taken
    for friend in self.cache["history"]:
        if friend["id"] == _id:
            return self.index(error="Friend already exists", code=400)

    self.cache["history"].append({"id": _id, "msgs": [], "name": name})

    return self.index()
