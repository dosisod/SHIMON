from typing import Union, AnyStr

def encode_anystr(data: AnyStr) -> bytes:
	if isinstance(data, str):
		return data.encode()

	return data
