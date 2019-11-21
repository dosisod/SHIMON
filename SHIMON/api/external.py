from hashlib import sha256
from copy import deepcopy

from typing import Union, List, Dict
from ..__init__ import Page

#below are functions which are used by both the api and shimon
def api_friends(self) -> List:
	ret=deepcopy(self.cache["friends"])
	for i in ret:
		i["hash"]=sha256hex(i["id"])

	return ret

def api_recent(self) -> List:
	ret=[]

	for user in self.cache["history"]:
		tmp={
			"id": user["id"],
			"hash": sha256hex(user["id"]),
		}

		if len(user["msgs"]) > 0: #if there are msgs to get, get most recent one
			tmp["msgs"]=[user["msgs"][-1]]

		else: #if this is a new user, show must recent msg as blank
			tmp["msgs"]=[{
				"sending": False,
				"msg": ""
			}]

		ret.append(tmp)

	return ret

def api_allfor(self, id: str) -> Union[List, Dict]:
	for user in self.cache["history"]:
		if user["id"]==id:
			if self.redraw: #only return data if there was a change
				self.redraw=False
				#return all messages from user
				return {
					"id": user["id"],
					"msgs": user["msgs"],
					"hash": sha256hex(user["id"])
				}

			else: #else return empty
				return []

	return False

def sha256hex(data: Union[str, bytes]) -> str: #returns the sha256 hex digest for given data
	if type(data) is str:
		return sha256(data.encode()).hexdigest()

	else:
		return sha256(data).hexdigest()
