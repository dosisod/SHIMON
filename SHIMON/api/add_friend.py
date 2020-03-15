from SHIMON.api.error import error_400

from typing import Dict, TYPE_CHECKING
from SHIMON.__init__ import HttpResponse

if TYPE_CHECKING:
	from SHIMON.shimon import Shimon

def add_friend(self: "Shimon", friend: Dict, redirect: bool) -> HttpResponse:
	if type(friend) is not dict:
		#message contains illegal characters if it was unable to be parsed
		return error_400()

	if "name" in friend and "id" in friend:
		#make sure that name and id are not blank
		if friend["name"] and friend["id"]:
			#make sure id is not already taken
			for _friend in self.cache["friends"]:
				if _friend["id"]==friend["id"]:
					return self.index(error="Friend already exists", code=400)

			#only append the names and ids, dont let user add extra data
			self.cache["friends"].append({
				"id": friend["id"],
				"name": friend["name"]
			})

			#add blank msg history to cache history
			self.cache["history"].append({
				"id": friend["id"],
				"msgs": []
			})

			return self.index()

	return self.index(error="Invalid Request", code=400)
