from SHIMON.api.toggle import Toggle


class ApiFreshJs(Toggle):
    callname = "fresh js"
    path = "SHIMON/static/js/api.js"
    name = "fresh js"

    def __init__(self) -> None:
        super().__init__()
