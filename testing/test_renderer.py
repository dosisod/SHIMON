from flask import make_response as _make_response
from flask.json import jsonify as _jsonify

from SHIMON.renderer import render, make_response, jsonify

from testing.base import BaseTest


class TestRender(BaseTest):
    @BaseTest.request_context
    @BaseTest.unlocked
    def test_all_settings_added_automatically(self) -> None:
        template = render(self.shimon, "testing/render.jinja")

        def assertHasKeys(html: str) -> None:
            keys = ["developer", "theme", "fresh_js", "fresh_css"]

            for key in keys:
                assert html.find(key + "=" + str(getattr(self.shimon, key))) > -1

        assertHasKeys(template.data.decode())

    @BaseTest.request_context
    @BaseTest.unlocked
    def test_make_response_is_same_as_calling_directly(self) -> None:
        make_resp_wrapper = make_response(render(self.shimon, "testing/hello.jinja"))

        make_resp = _make_response(render(self.shimon, "testing/hello.jinja"))

        assert make_resp.data == make_resp_wrapper.data
        assert make_resp.status == make_resp_wrapper.status

    @BaseTest.request_context
    def test_jsonify_is_same_as_calling_directly(self) -> None:
        json_wrapper = jsonify({"hello": "world!"})
        json_original = _jsonify({"hello": "world!"})

        assert json_wrapper.json == json_original.json
        assert json_wrapper.status == json_original.status
