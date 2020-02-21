import os

from .error import error_202, error_400

from ..__init__ import HttpResponse

def theme(self, theme: str, redirect: bool) -> HttpResponse:
	if type(theme) is str:
		path="SHIMON/templates/themes/"
		dirty=os.path.abspath(path + theme)

		#dont allow reverse file traversal
		if dirty.startswith(os.getcwd() + "/" + path):
			if os.path.isfile(dirty + ".css"):
				self.cache.mapper["theme"]=dirty.split("/")[-1]

				return error_202()

	return error_400()
