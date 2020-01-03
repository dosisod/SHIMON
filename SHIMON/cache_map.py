class CacheMapper:
	shimon=None
	cache_names={}

	def __init__(self, shimon_ref, mapped_vars: dict):
		self.shimon=shimon_ref

		self.cache_names=mapped_vars

	def __setitem__(self, cache_name: str, value: any) -> None:
		if cache_name not in self.cache_names:
			return

		self.shimon.cache[cache_name]=value
		self._update(cache_name, value)

	def update(self, cache_name: str) -> None:
		cache_val=self.cache_names[cache_name]

		if cache_name not in self.cache_names:
			return

		if cache_name in self.shimon.cache:
			self._update(cache_name, self.shimon.cache[cache_name])

		else:
			self.shimon.cache[cache_name]=self.shimon.__dict__[cache_val]

	def _update(self, cache_name: str, value: any) -> None:
		cache_val=self.cache_names[cache_name]

		if type(cache_val) is tuple:
			cache_val[0].__dict__[cache_val[1]]=value

		else:
			self.shimon.__dict__[cache_val]=value
