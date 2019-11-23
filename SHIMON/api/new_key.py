import base64 as b64

from ..security import correct_pwd
from ..storage import lock
from ..kee import kee

from .error import error, error_400

from typing import Union, Dict, Any, List
from ..__init__ import Page, Json

def new_key(self, data: Dict) -> Union[Page, Json]:
	#pwd cannot be blank
	if data["new key"]:
		#password required to change key
		if correct_pwd(self, data["new key"]):
			self.cache["key"]=b64.b64encode(kee(2048).private()).decode()

			lock(self, data["new key"]) #makes sure changes are saved

			return self.index()

		return error(401, "Incorrect password", False, False)

	return error_400()
