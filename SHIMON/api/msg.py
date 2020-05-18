from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from SHIMON.shimon import Shimon


def history_id(self: "Shimon", passed_id: str) -> int:
    for index, friend in enumerate(self.cache["history"]):
        if friend["id"] == passed_id:
            return index

    return -1
