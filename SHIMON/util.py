from typing import Union, cast
from .__init__ import Stringish

def encode_stringish(data: Stringish) -> bytes:
	if type(data) is str:
		return cast(str, data).encode()

	return cast(bytes, data)
