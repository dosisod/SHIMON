import os

from .error import error_200

from ..__init__ import HttpResponse

class Toggle:
	def __init__(self, path: str, name: str):
		self.path=path
		self.name=name

	def __call__(self, shimon, enable: bool, _: bool) -> HttpResponse:
		if os.path.isfile(self.path):
			shimon.cache.mapper[self.name]=enable

		else:
			shimon.cache.mapper[self.name]=False

		return error_200()
