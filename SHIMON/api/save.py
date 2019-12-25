from .. import storage

from .error import error_200

from typing import Union, Dict
from ..__init__ import Json, Page

def save(self, data: Dict) -> Union[Json, Page]:
	ret=storage.save(self, data["save"])

	#if the lock returns an error, re-return it
	if ret:
		return ret

	#update settings if they were set since last save
	self.msg_policy=self.cache["msg policy"]
	self.session.expires=self.cache["expiration"]
	self.developer=self.cache["developer"]

	return error_200()
