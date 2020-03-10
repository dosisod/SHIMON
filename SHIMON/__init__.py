from flask import Response

from typing import Union, Dict, List, Tuple

Page=Union[
	Response,
	str,
	Tuple[Response, int],
	Tuple[str, int]
]

HttpResponse=Tuple[Page, int]
AnyResponse=Union[HttpResponse, Page]

Complex=Union[Dict, List, str, Page]
