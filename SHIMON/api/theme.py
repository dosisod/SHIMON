import os

from SHIMON.api.error import error_202, error_400
from SHIMON.api.api_base import ApiBase

from typing import TYPE_CHECKING
from SHIMON.__init__ import HttpResponse

if TYPE_CHECKING:
	from SHIMON.shimon import Shimon

class ApiTheme(ApiBase):
	callname="theme"

	def __init__(self) -> None:
		super().__init__()

	def entry(_, self: "Shimon", name: str, redirect: bool) -> HttpResponse:
		return theme(self, name, redirect)

def theme(self: "Shimon", name: str, redirect: bool) -> HttpResponse:
	if type(name) is str:
		path="SHIMON/templates/themes/"
		dirty=os.path.abspath(path + name)

		#dont allow reverse file traversal
		if dirty.startswith(os.getcwd() + "/" + path):
			if os.path.isfile(f"{dirty}.css"):
				self.cache.mapper["theme"]=dirty.split("/")[-1]

				return error_202()

	return error_400()
