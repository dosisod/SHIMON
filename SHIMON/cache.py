from .cache_map import CacheMapper

from typing import Dict, Any, Optional

CacheType=Dict[str, Any]

class Cache:
	_cache: CacheType
	_empty_cache={"": None}

	mapper: CacheMapper

	def __init__(self, cache: Optional[CacheType]=None) -> None:
		if cache:
			self._cache=cache

		else:
			self._cache=self._empty_cache

	def __setitem__(self, key: str, value: Any) -> None:
		self._cache[key]=value

	def __getitem__(self, key: str) -> Any:
		return self._cache[key]

	def is_empty(self) -> bool:
		return self._cache==self._empty_cache

	def wipe(self):
		self._cache=self._empty_cache

	def load(self, cache: CacheType) -> None:
		self._cache=cache

	def export(self) -> CacheType:
		return self._cache
