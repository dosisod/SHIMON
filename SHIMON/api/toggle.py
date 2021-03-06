from pathlib import Path

from SHIMON.api.error import error_200, error_400
from SHIMON.api.api_base import ApiBase

from typing import TYPE_CHECKING
from SHIMON import HttpResponse

if TYPE_CHECKING:
    from SHIMON.shimon import Shimon


class Toggle(ApiBase):
    path = ""
    name = ""

    @ApiBase.bool_required
    def entry(self, shimon: "Shimon", enable: bool, _: bool) -> HttpResponse:
        if Path(self.path).is_file():
            shimon.cache.mapper[self.name] = enable
            return error_200()

        shimon.cache.mapper[self.name] = False
        return error_400("Missing required file(s)")
