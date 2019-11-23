from .error import error, error_202, error_400
from ..security import update_pwd

from typing import Dict
from ..__init__ import Page, Json

def change_pwd(self, data: Dict) -> Json:
	if type(data["change pwd"]) is not dict:
		#message contains illegal characters if it was unable to be parsed
		return error_400()

	if "old" in data["change pwd"] and "new" in data["change pwd"]:
		tmp=update_pwd(self, data["change pwd"]["old"], data["change pwd"]["new"])
		if tmp:
			return error_202() #password was updated successfull

		else:
			return error(401, "Password could not be updated", data["redirect"], False) #incorrect info was given

	else:
		return error_400(data=data) #invalid request
