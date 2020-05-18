from SHIMON.api.toggle import Toggle


class ApiFreshCss(Toggle):
    callname = "fresh css"
    path = "SHIMON/static/css/font.css"
    name = "fresh css"

    def __init__(self) -> None:
        super().__init__()
