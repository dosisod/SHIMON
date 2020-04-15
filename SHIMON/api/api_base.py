from SHIMON.api.error import error_400

from typing import Any, Dict, Callable, TYPE_CHECKING
from SHIMON.__init__ import HttpResponse

if TYPE_CHECKING:
	from SHIMON.shimon import Shimon

class ApiBase:
	callname=""

	def __init__(self) -> None:
		pass

	def entry(self, shimon: "Shimon", data: Any, redirect: bool) -> HttpResponse:
		pass

	@staticmethod
	def dict_required(func: Callable[..., HttpResponse]) -> Callable[..., HttpResponse]:
		def make_dec(self: ApiBase, *args: Any, **kwargs: Any) -> HttpResponse:
			if type(args[1]) is not dict:
				return error_400()

			return func(self, *args, **kwargs)

		return make_dec