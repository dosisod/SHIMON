from flask import abort
import json

from ..security import check_all

#api related functions, in order of appearence
from .external import api_recent, api_friends, api_allfor
from .error import error, error_200, error_202, error_400
from .unlock import unlock
from .send_msg import send_msg
from .delete_msg import delete_msg
from .save import save
from .lock import lock
from .change_pwd import change_pwd
from .new_key import new_key
from .msg_policy import msg_policy
from .expiration_timer import expiration_timer
from .theme import theme
from .devmode import devmode
from .nuke import nuke
from .fresh_js import fresh_js
from .fresh_css import fresh_css
from .status import status
from .ping import ping
from ._data import _data
from .add_friend import add_friend

from typing import Union, Dict
from ..__init__ import Page, Json

def handler(self, data: Dict) -> Union[Page, Json]: #handles all api requests
	for attr in data: #loop through and convert to json
		data[attr]=api_decode(data[attr])

	if "unlock" in data and not self.cache: #try and unlock cache (if cache is not unlocked)
		return unlock(self, data)

	ret=check_all(self)
	if ret: return ret

	if "send msg" in data:
		return send_msg(self, data)

	elif "delete msg" in data:
		return delete_msg(self, data)

	elif "save" in data: #user only wants to encrypt cache
		return save(self, data)

	elif "lock" in data: #user wants to encrypt cache and log out
		return lock(self, data)

	elif "change pwd" in data:
		return change_pwd(self, data)

	elif "new key" in data:
		return new_key(self, data)

	elif "msg policy" in data:
		return msg_policy(self, data)

	elif "expiration timer" in data:
		return expiration_timer(self, data)

	elif "theme" in data:
		return theme(self, data)

	elif "devmode" in data:
		return devmode(self, data)

	elif "nuke" in data: #user wants to delete cache
		return nuke(self, data)

	elif "fresh js" in data:
		return fresh_js(self, data)

	elif "fresh css" in data:
		return fresh_css(self, data)

	elif "status" in data:
		return status(self, data)

	elif "ping" in data:
		return ping(self, data)

	elif "data" in data: #requesting data from cache
		return _data(self, data)

	elif "add friend" in data:
		return add_friend(self, data)

	else:
		#if the call is not recognized, throw a 400 error
		return error_400()

	abort(500) #if anything above exits and gets to here, make sure the user knows of the error

def api_decode(s: str) -> Union[Dict, str]: #decodes json if possible
	if s.startswith("[") or s.startswith("{"):
		try:
			return json.loads(s) #potentialy json, try to parse
		except:
			pass

	return s #return if not json or if the json was malformed