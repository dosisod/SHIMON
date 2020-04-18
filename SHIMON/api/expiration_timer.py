from SHIMON.api.int_range import ApiIntRange

class ApiExpirationTimer(ApiIntRange):
	callname="expiration timer"

	cachename="expiration"
	min_allowed=900
	max_allowed=86400
