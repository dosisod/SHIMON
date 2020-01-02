class CacheMapper:
	shimon=None
	cache_names={}

	def __init__(self, shimon_ref, maps: map):
		self.shimon=shimon_ref

		self.cache_names=maps

	def __setitem__(self, cache_name: str, value: any) -> None:
		if cache_name not in self.cache_names:
			return

		self.shimon.cache[cache_name]=value
		self.shimon.__dict__[self.cache_names[cache_name]]=value

	def update(self, cache_name: str) -> None:
		if cache_name not in self.cache_names:
			return

		if cache_name in self.shimon.cache:
			self.shimon__dict__[self.cache_names[cache_name]]=self.shimon.cache[cache_name]
		else:
			self.shimon.cache[cache_name]=self.shimon.__dict__[self.cache_names[cache_name]]
