import os

from .error import error_202, error_400

from typing import Union, Dict, Any, List
from ..__init__ import Json

def theme(self, theme: str, redirect: bool) -> Json:
	if type(theme) is str:
		clean=os.path.abspath("SHIMON/templates/themes/"+theme)

		#dont allow reverse file traversal
		if clean.startswith(os.getcwd()+"/SHIMON/templates/themes/"):
			if os.path.isfile(clean+".css"):
				self.cache_mapper["theme"]=clean.split("/")[-1]

				return error_202()

	return error_400()
