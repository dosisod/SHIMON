from .error import error_401

from typing import Union, Dict
from ..__init__ import Page, Json

def nuke(self, pwd: str, redirect: bool) -> Union[Page, Json]:
	if self.security.correct_pwd(pwd):
		return self.session.create(fresh=True)

	return error_401()
