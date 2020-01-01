import base64 as b64

from ..kee import kee

from .error import error_400, error_401

from typing import Union, Dict, Any, List
from ..__init__ import Page, Json

def new_key(self, data: Dict) -> Union[Page, Json]:
	if "new key" in data:
		if self.security.correct_pwd(data["new key"]):
			self.cache["key"]=b64.b64encode(kee(2048).private()).decode()

			#makes sure changes are saved
			self.storage.lock(data["new key"])

			return self.index()

		return error_401()

	return error_400()
