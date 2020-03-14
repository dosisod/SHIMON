from flask import Response

from typing import Union, Dict, List, Tuple
from mypy_extensions import TypedDict

HttpResponse=Tuple[Response, int]

class Message(TypedDict):
	msg: str
	sending: bool

class History(TypedDict):
	id: str
	msgs: List[Message]
