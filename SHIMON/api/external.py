from hashlib import sha256
from copy import deepcopy

from ..util import encode_anystr

from typing import Union, List, Dict, AnyStr
from ..__init__ import Page

def api_friends(self) -> List:
	friends: List=deepcopy(self.cache["friends"])
	for friend in friends:
		friend["hash"]=sha256hex(friend["id"])

	return friends

def api_recent(self) -> List:
	recent=[]

	for user in self.cache["history"]:
		recent_user={
			"id": user["id"],
			"hash": sha256hex(user["id"]),
		}

		if len(user["msgs"]) > 0:
			recent_user["msgs"]=[user["msgs"][-1]]

		else:
			#if this is a new user, use blank message
			recent_user["msgs"]=[{
				"sending": False,
				"msg": ""
			}]

		recent.append(recent_user)

	return recent

def api_allfor(self, id: str) -> Union[List, Dict, bool]:
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

def sha256hex(data: AnyStr) -> str:
	return sha256(encode_anystr(data)).hexdigest()
