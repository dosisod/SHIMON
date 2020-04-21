from hashlib import sha256
from copy import deepcopy

from SHIMON.encoding import encode_anystr

from typing import Union, List, Dict, AnyStr, TYPE_CHECKING
from typing_extensions import Literal

if TYPE_CHECKING:
	from SHIMON.shimon import Shimon

def api_friends(self: "Shimon") -> List:
	friends: List=deepcopy(self.cache["history"])
	for friend in friends:
		friend["hash"]=sha256hex(friend["id"])

	return friends

def api_recent(self: "Shimon") -> List:
	recent=[]

	for user in self.cache["history"]:
		recent_user={
			"id": user["id"],
			"hash": sha256hex(user["id"]),
			"msgs": [user["msgs"][-1] if len(user["msgs"]) > 0 else {
				"sending": False,
				"msg": ""
			}]
		}

		recent.append(recent_user)

	return recent

def api_allfor(self: "Shimon", id: str) -> Union[List, Dict, Literal[False]]:
	for user in self.cache["history"]:
		if user["id"]==id:
			break
	else:
		return False

	if not self.redraw:
		return []

	self.redraw=False

	return {
		"id": user["id"],
		"msgs": user["msgs"],
		"hash": sha256hex(user["id"])
	}

def sha256hex(data: AnyStr) -> str:
	return sha256(encode_anystr(data)).hexdigest()
