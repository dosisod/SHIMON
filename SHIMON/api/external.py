#this file contains functions which are used by both the api and shimon

from hashlib import sha256
from copy import deepcopy

from typing import Union, List, Dict
from ..__init__ import Page

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

		#if there are msgs to get, get most recent one
		if len(user["msgs"]) > 0:
			tmp["msgs"]=[user["msgs"][-1]]

		#if this is a new user, show must recent msg as blank
		else:
			tmp["msgs"]=[{
				"sending": False,
				"msg": ""
			}]

		ret.append(tmp)

	return ret

def api_allfor(self, id: str) -> Union[List, Dict]:
	for user in self.cache["history"]:
		if user["id"]==id:
			if self.redraw:
				self.redraw=False

				return {
					"id": user["id"],
					"msgs": user["msgs"],
					"hash": sha256hex(user["id"])
				}

			#dont return data if we shouldnt redraw
			else:
				return []

	return False

def sha256hex(data: Union[str, bytes]) -> str:
	if type(data) is str:
		return sha256(data.encode()).hexdigest()

	else:
		return sha256(data).hexdigest()
