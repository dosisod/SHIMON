from SHIMON import HttpResponse

def assertHttpResponse(data: HttpResponse, code: int) -> None:
	assert data[1]==code