from SHIMON.renderer import jsonify

from SHIMON.api.error import error, error_200

from testing.base import BaseTest

class TestError(BaseTest):
	@BaseTest.app_context
	def test_true_as_string_is_True(self):
		assert error(200, "testing", "true")[0]=="testing"

	@BaseTest.app_context
	def test_string_returned_as_is(self):
		assert error(200, "testing", True)[0]=="testing"

	@BaseTest.app_context
	def test_ints_returned_as_is(self):
		assert error(200, 1337, True)[0]==1337

	@BaseTest.app_context
	def test_json_is_jsonified(self):
		assert error(200, ["test3"], True)[0].json==jsonify(["test3"]).json

	@BaseTest.app_context
	def test_rethrow_param_causes_rethrow(self):
		assert error(200, None, False, True)[0].json==jsonify({"rethrow":""}).json

	@BaseTest.app_context
	def test_unreturnable_variable_is_blank(self):
		assert error(200, None, False)[0].json==jsonify({"code":200,"msg":""}).json

	@BaseTest.app_context
	def test_error_wrapper_is_same_when_called_directly(self):
		assert error_200()[0].json==error(200, "OK", False)[0].json

	@BaseTest.app_context
	def test_custom_error_wrapper_is_same_when_called_directly(self):
		assert error_200("test")[0].json==error(200, "test", False)[0].json
