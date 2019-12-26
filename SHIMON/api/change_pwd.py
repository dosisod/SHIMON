from .error import error_202, error_400, error_401

from typing import Dict
from ..__init__ import Page, Json

def change_pwd(self, data: Dict) -> Json:
	if type(data["change pwd"]) is not dict:
		#message contains illegal characters if it was unable to be parsed
		return error_400()

	if "old" in data["change pwd"] and "new" in data["change pwd"]:
		success=self.security.update_pwd(self, data["change pwd"]["old"], data["change pwd"]["new"])
		if not success:
			return error_401("Password could not be updated", data["redirect"])

		return error_202()

	else:
		return error_400(data=data)
