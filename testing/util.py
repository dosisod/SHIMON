from typing import Tuple
from SHIMON.__init__ import Page, HttpResponse

def assertHttpResponse(data: HttpResponse, code: int) -> None:
	assert data[1]==code

	assert not isinstance(data[0], tuple)
	assert isinstance(data[0], Page.__args__)