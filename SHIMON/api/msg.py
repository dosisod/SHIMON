from typing import TYPE_CHECKING

if TYPE_CHECKING:
	from SHIMON.shimon import Shimon

def history_id(self: "Shimon", passed_id: str) -> int:
	for friend in self.cache["friends"]:
		if friend["id"]==passed_id:
			for index, history in enumerate(self.cache["history"]):
				if history["id"]==passed_id:
					return index

	return -1
