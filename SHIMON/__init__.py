from flask import Response

from typing import Union, Dict, List, Any

#can be a flask response or raw html response
Page=Union[Response, str]

#json returned from api_error is still a Response, just alias it to make more sense
Json=Response

#Complex can be many things, including dict, list, str
#technically Complex could be anything, but preferably it is one of the above ones
Complex=Union[Dict, List, str, Any]

#methods where a string or bytes can be automatically converted is "Stringish"
Stringish=Union[str, bytes]
