from typing import Union, Dict, Tuple, Any, cast

CacheDictValue=Union[str, Tuple[Any, str]]

CacheDict=Union[
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
		if isinstance(cache_name, list):
			for name in cache_name:
				self.update(name)

			return

		cast(str, cache_name)
		cache_val=self.cache_names[cache_name]

		if cache_name not in self.cache_names:
			return

		if cache_name in self.shimon.cache:
			self._update(
				cache_name,
				self.shimon.cache[cache_name]
			)

		else:
			if isinstance(cache_val, tuple):
				self.shimon.cache[cache_name]= \
					self.shimon.__dict__[
						cache_val[0].__dict__[cache_val[1]]
					]

			else:
				self.shimon.cache[cache_name]= \
					self.shimon.__dict__[cache_val]

	def _update(self, cache_name: str, value: CacheDictValue) -> None:
		cache_val=self.cache_names[cache_name]

		if isinstance(cache_val, tuple):
			cache_val[0].__dict__[cache_val[1]]=value

		else:
			self.shimon.__dict__[cache_val]=value
