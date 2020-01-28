from flask import Response

from typing import Union, Dict, List, Any, Tuple

Page=Union[
	Response,
	str,
	Tuple[Response, int],
	Tuple[str, int]
]

HttpResponse=Tuple[Page, int]
AnyResponse=Union[HttpResponse, Page]

#returned json is just a response, added for clarity
Json=Page

#Complex can be many things, including dict, list, str
#technically Complex could be anything, but preferably it is one of the above ones
Complex=Union[Dict, List, str, Page]
