import os

from SHIMON.api.error import error_202, error_400

from typing import TYPE_CHECKING
from SHIMON.__init__ import HttpResponse

if TYPE_CHECKING:
	from SHIMON.shimon import Shimon

def theme(self: "Shimon", theme: str, redirect: bool) -> HttpResponse:
	if type(theme) is str:
		path="SHIMON/templates/themes/"
		dirty=os.path.abspath(path + theme)

		#dont allow reverse file traversal
		if dirty.startswith(os.getcwd() + "/" + path):
			if os.path.isfile(f"{dirty}.css"):
				self.cache.mapper["theme"]=dirty.split("/")[-1]

				return error_202()

	return error_400()
