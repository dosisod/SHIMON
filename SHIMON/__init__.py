from flask import Response

from typing import Union, Dict, List, Tuple
from mypy_extensions import TypedDict

Page=Union[
	Response,
	str,
	Tuple[Response, int],
	Tuple[str, int]
]

HttpResponse=Tuple[Page, int]
AnyResponse=Union[HttpResponse, Page]

class Message(TypedDict):
	msg: str
	sending: bool

class History(TypedDict):
	id: str
	msgs: List[Message]
