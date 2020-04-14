from SHIMON.api.error import error_400

from typing import Any, Dict, TYPE_CHECKING
from SHIMON.__init__ import HttpResponse

if TYPE_CHECKING:
	from SHIMON.shimon import Shimon

class ApiBase:
	callname=""

	def __init__(self) -> None:
		pass

	def entry(self, shimon: "Shimon", data: Any, redirect: bool) -> HttpResponse:
		pass