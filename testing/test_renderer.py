from flask.json import jsonify as _jsonify

from SHIMON.renderer import render, jsonify

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
    def test_jsonify_is_same_as_calling_directly(self) -> None:
        json_wrapper = jsonify({"hello": "world!"})
        json_original = _jsonify({"hello": "world!"})

        assert json_wrapper.json == json_original.json
        assert json_wrapper.status == json_original.status
