from pathlib import Path

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

	@ApiBase.str_required
	def entry(_, self: "Shimon", name: str, redirect: bool) -> HttpResponse:
		return theme(self, name, redirect)

def theme(self: "Shimon", name: str, redirect: bool) -> HttpResponse:
	themes=Path("SHIMON/templates/themes/")
	dirty=(themes / name).resolve()

	#dont allow reverse file traversal
	if str(dirty).startswith(str(Path.cwd() / themes)):
		if Path(f"{dirty}.css").is_file():
			self.cache.mapper["theme"]=dirty.parts[-1]

			return error_202()

	return error_400()
