from ..security import correct_pwd
from .error import error_401

from typing import Union, Dict
from ..__init__ import Page, Json

def nuke(self, data: Dict) -> Union[Page, Json]:
	if correct_pwd(self, data["nuke"]):
		return self.session.create(self, fresh=True)

	return error_401()
