from SHIMON.api.toggle import Toggle

class ApiFreshJs(Toggle):
	callname="fresh js"

	def __init__(self) -> None:
		super().__init__(
			path="SHIMON/static/js/api.js",
			name="fresh js"
		)
