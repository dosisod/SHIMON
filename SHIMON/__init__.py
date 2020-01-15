from flask import Response

from typing import Union, Dict, List, Any, Tuple

#can be a flask response or str, with or without an HTTP code (int)
Page=Union[
	Response,
	str,
	Tuple[
		Union[Response, str],
		int
	]
]

#returned json is just a response, added for clarity
Json=Response

#Complex can be many things, including dict, list, str
#technically Complex could be anything, but preferably it is one of the above ones
Complex=Union[Dict, List, str, Any]
