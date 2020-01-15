from typing import Union, AnyStr, cast

def encode_anystr(data: AnyStr) -> bytes:
	if type(data) is str:
		return cast(str, data).encode()

	return cast(bytes, data)
