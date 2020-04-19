from SHIMON.api.error import error_400

from typing import Any, Dict, Callable, Type, TYPE_CHECKING
from SHIMON.__init__ import HttpResponse

if TYPE_CHECKING:
	from SHIMON.shimon import Shimon

HttpCall=Callable[..., HttpResponse]

def make_required(self: "ApiBase", requested_type: Type, func: HttpCall, *args: Any, **kwargs: Any) -> HttpResponse:
	if type(args[1]) is not requested_type:
		return error_400()

	return func(self, *args, **kwargs)

class ApiBase:
	callname=""
	unlock_required=True

	def __init__(self) -> None:
		pass

	def entry(self, shimon: "Shimon", data: Any, redirect: bool) -> HttpResponse:
		pass

	@staticmethod
	def dict_required(func: HttpCall) -> HttpCall:
		def make_dec(self: ApiBase, *args: Any, **kwargs: Any) -> HttpResponse:
			return make_required(self, dict, func, *args, **kwargs)
		return make_dec

	@staticmethod
	def str_required(func: HttpCall) -> HttpCall:
		def make_dec(self: ApiBase, *args: Any, **kwargs: Any) -> HttpResponse:
			return make_required(self, str, func, *args, **kwargs)
		return make_dec

	@staticmethod
	def bool_required(func: HttpCall) -> HttpCall:
		def make_dec(self: ApiBase, *args: Any, **kwargs: Any) -> HttpResponse:
			return make_required(self, bool, func, *args, **kwargs)
		return make_dec

	@staticmethod
	def int_str_required(func: HttpCall) -> HttpCall:
		def make_dec(self: ApiBase, *args: Any, **kwargs: Any) -> HttpResponse:
			if type(args[1]) is str and args[1].isdigit():
				return func(self, *args, **kwargs)

			else:
				return error_400()

		return make_dec