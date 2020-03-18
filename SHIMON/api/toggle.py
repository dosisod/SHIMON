import os

from SHIMON.api.error import error_200

from typing import TYPE_CHECKING
from SHIMON.__init__ import HttpResponse

if TYPE_CHECKING:
	from SHIMON.shimon import Shimon

class Toggle:
	def __init__(self, path: str, name: str):
		self.path=path
		self.name=name

	def __call__(self, shimon: "Shimon", enable: bool, _: bool) -> HttpResponse:
		if os.path.isfile(self.path):
			shimon.cache.mapper[self.name]=enable

		else:
			shimon.cache.mapper[self.name]=False

		return error_200()
