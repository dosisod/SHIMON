import re

from SHIMON.api.error import error_400

from typing import Dict, TYPE_CHECKING
from SHIMON.__init__ import HttpResponse

if TYPE_CHECKING:
	from SHIMON.shimon import Shimon

def add_friend(self: "Shimon", adding: Dict, redirect: bool) -> HttpResponse:
	if type(adding) is not dict:
		#message contains illegal characters if it was unable to be parsed
		return error_400()

	name=adding.get("name", None)
	_id=adding.get("id", None)

	#make sure that name and id are valid
	if name and _id and re.search("^[a-zA-z0-9]+$", _id):
		#make sure id is not already taken
		for friend in self.cache["friends"]:
			if friend["id"]==_id:
				return self.index(error="Friend already exists", code=400)

		#only append the names and ids, dont let user add extra data
		self.cache["friends"].append({
			"id": _id,
			"name": name
		})

		#add blank msg history to cache history
		self.cache["history"].append({
			"id": _id,
			"msgs": []
		})

		return self.index()

	return self.index(error="Invalid Request", code=400)
