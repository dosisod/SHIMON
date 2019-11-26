from ..session import session_start
from .security import correct_pwd
from .error import error_401

from typing import Union, Dict
from ..__init__ import Page, Json

def nuke(self, data: Dict) -> Union[Page, Json]:
	if correct_pwd(self, data["nuke"]):
		#start a new session as if it is booting for the first time
		return session_start(self, True)

	return error_401()
