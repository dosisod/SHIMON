from SHIMON.api.error import error_202, error_400
from SHIMON.api.api_base import ApiBase

from typing import TYPE_CHECKING
from SHIMON import HttpResponse

if TYPE_CHECKING:
    from SHIMON.shimon import Shimon


class ApiIntRange(ApiBase):
    cachename = ""
    min_allowed = 0
    max_allowed = 1

    @ApiBase.int_str_required
    def entry(self, shimon: "Shimon", data: str, redirect: bool) -> HttpResponse:
        num = int(data)
        if self.min_allowed <= num <= self.max_allowed:
            shimon.cache.mapper[self.cachename] = num

            return error_202()

        return error_400()
