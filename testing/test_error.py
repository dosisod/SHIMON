from SHIMON.renderer import jsonify, render

from SHIMON.api.error import error, error_200

from testing.base import BaseTest


class TestError(BaseTest):
    @BaseTest.app_context
    def test_json_is_jsonified(self) -> None:
        assert error(200, ["test3"], True)[0].json == jsonify(["test3"]).json

    @BaseTest.app_context
    def test_rethrow_param_causes_rethrow(self) -> None:
        assert error(200, "", False, True)[0].json == jsonify({"rethrow": ""}).json

    @BaseTest.request_context
    def test_unreturnable_variable_is_blank(self) -> None:
        assert (
            error(
                200,
                None,  # type: ignore
                False,
            )[
                0
            ].json
            == jsonify({"code": 200, "msg": ""}).json
        )

    @BaseTest.app_context
    def test_error_wrapper_is_same_when_called_directly(self) -> None:
        assert error_200()[0].json == error(200, "OK", False)[0].json

    @BaseTest.app_context
    def test_custom_error_wrapper_is_same_when_called_directly(self) -> None:
        assert error_200("test")[0].json == error(200, "test", False)[0].json
