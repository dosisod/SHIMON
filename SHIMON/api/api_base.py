from SHIMON.api.error import error_400

from typing import Any, Callable, Dict, TYPE_CHECKING
from SHIMON.__init__ import HttpResponse

if TYPE_CHECKING:
	from SHIMON.shimon import Shimon

class ApiBase:
	shimon: "Shimon"

	def __init__(self, shimon_ref: "Shimon") -> None:
		self.shimon=shimon_ref

	def entry(self, data: Any, redirect: bool) -> HttpResponse:
		pass