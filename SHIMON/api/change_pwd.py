from .error import error_202, error_400, error_401

from typing import Dict
from ..__init__ import Page, Json

def change_pwd(self, pwds: Dict, redirect: bool) -> Json:
	if type(pwds) is not dict:
		#message contains illegal characters if it was unable to be parsed
		return error_400()

	if "old" in pwds and "new" in pwds:
		success=self.security.update_pwd(pwds["old"], pwds["new"])
		if not success:
			return error_401("Password could not be updated", redirect)

		return error_202()

	else:
		return error_400()
