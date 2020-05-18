from flask import make_response as _make_response
from flask import render_template, Response
from flask.json import jsonify as _jsonify

from typing import Any, cast, TYPE_CHECKING

if TYPE_CHECKING:
    from SHIMON.shimon import Shimon


def render(self: "Shimon", filepath: str, **kwargs: Any) -> Response:
    return make_response(
        render_template(
            filepath,
            **{
                **kwargs,
                "developer": self.developer,
                "theme": self.theme,
                "fresh_js": self.fresh_js,
                "fresh_css": self.fresh_css,
            }
        )
    )


def make_response(*args: Any) -> Response:
    return cast(Response, _make_response(*args))


# duplicate function of jsonify that returns Response type and not Any
def jsonify(*args: Any, **kwargs: Any) -> Response:
    return cast(Response, _jsonify(*args))
