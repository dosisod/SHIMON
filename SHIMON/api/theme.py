import os

from .error import error_202, error_400

from typing import Union, Dict, Any, List
from ..__init__ import Json

def theme(self, data: Dict) -> Json:
	if type(data["theme"]) is str:
		clean=os.path.abspath("templates/themes/"+data["theme"])

		if clean.startswith(os.getcwd()+"/templates/themes/"): #dont allow reverse file traversal
			if os.path.isfile(clean+".css"):
				self.cache["theme"]=clean.split("/")[-1]
				self.theme=self.cache["theme"]

				return error_202()

	return error_400()
