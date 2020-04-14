from SHIMON.api.toggle import Toggle

class ApiFreshCss(Toggle):
	callname="fresh css"

	def __init__(self) -> None:
		super().__init__(
			path="SHIMON/static/css/font.css",
			name="fresh css"
		)
