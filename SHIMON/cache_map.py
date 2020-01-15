from typing import Union, Dict, Tuple, Any, cast

CacheDictValue=Union[str, Tuple[Any, str]]

CacheDict=Union[
	Dict[str, str],
	Dict[str, CacheDictValue]
]

class CacheMapper:
	cache_names: CacheDict

	def __init__(self, shimon_ref, mapped_vars: CacheDict):
		self.shimon=shimon_ref

		self.cache_names=mapped_vars

	def __setitem__(self, cache_name: str, value: CacheDictValue) -> None:
		if cache_name not in self.cache_names:
			return

		self.shimon.cache[cache_name]=value
		self._update(cache_name, value)

	def update(self, cache_name: Union[str, list]) -> None:
		if type(cache_name) is list:
			for name in cache_name:
				self.update(name)

			return

		cache_val=self.cache_names[
			cast(str, cache_name)
		]

		if cache_name not in self.cache_names:
			return

		if cache_name in self.shimon.cache:
			self._update(
				cast(str, cache_name),
				self.shimon.cache[cache_name]
			)

		else:
			self.shimon.cache[cache_name]=self.shimon.__dict__[cache_val]

	def _update(self, cache_name: str, value: CacheDictValue) -> None:
		cache_val=self.cache_names[cache_name]

		if type(cache_val) is tuple:
			cache_tuple=cast(tuple, cache_val)

			cache_tuple[0].__dict__[cache_tuple[1]]=value

		else:
			self.shimon.__dict__[cache_val]=value
