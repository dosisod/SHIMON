from typing import Union, Dict, Tuple, Any, TYPE_CHECKING

if TYPE_CHECKING:
    from SHIMON.shimon import Shimon

CacheDictValue = Union[str, bool, int]

CacheDict = Union[Dict[str, Union[str, Tuple[Any, str]]]]


class CacheMapper:
    cache_names: CacheDict

    def __init__(self, shimon_ref: "Shimon", mapped_vars: CacheDict) -> None:
        self.shimon = shimon_ref

        self.cache_names = mapped_vars

    def __setitem__(self, cache_name: str, value: CacheDictValue) -> None:
        if cache_name not in self.cache_names:
            return

        self.shimon.cache._cache[cache_name] = value
        self._update(cache_name, value)

    def update(self, cache_name: Union[str, list]) -> None:
        if isinstance(cache_name, list):
            for name in cache_name:
                self.update(name)

            return

        cache_val = self.cache_names[cache_name]

        if cache_name not in self.cache_names:
            return

        if cache_name in self.shimon.cache._cache:
            self._update(cache_name, self.shimon.cache._cache[cache_name])

        else:
            if isinstance(cache_val, tuple):
                self.shimon.cache._cache[cache_name] = getattr(
                    self.shimon, getattr(cache_val[0], cache_val[1])
                )

            else:
                self.shimon.cache._cache[cache_name] = getattr(self.shimon, cache_val)

    def _update(self, cache_name: str, value: CacheDictValue) -> None:
        cache_val = self.cache_names[cache_name]

        if isinstance(cache_val, tuple):
            setattr(cache_val[0], cache_val[1], value)

        else:
            setattr(self.shimon, cache_val, value)
