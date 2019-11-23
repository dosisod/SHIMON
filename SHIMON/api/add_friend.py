from .error import error_400

from typing import Dict
from ..__init__ import Page

def add_friend(self, data: Dict) -> Page:
	if type(data["add friend"]) is not dict:
		#message contains illegal characters if it was unable to be parsed
		return error_400()

	if "name" in data["add friend"] and "id" in data["add friend"]:
		#make sure that name and id are not blank
		if data["add friend"]["name"] and data["add friend"]["id"]:
			#make sure id is not already taken
			for friend in self.cache["friends"]:
				if friend["id"]==data["add friend"]["id"]:
					return self.index(error="Friend already exists")

			#only append the names and ids, dont let user add extra data
			self.cache["friends"].append({
				"id": data["add friend"]["id"],
				"name": data["add friend"]["name"]
			})

			#add blank msg history to cache history
			self.cache["history"].append({
				"id": data["add friend"]["id"],
				"msgs": []
			})

			return self.index()

	return self.index(error="Invalid Request")
