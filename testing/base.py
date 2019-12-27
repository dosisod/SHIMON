from SHIMON.app import App

class BaseTest:
	pwd="123"

	test_app=App()
	shimon=test_app.shimon

	app_context=test_app.app.app_context()
	request_context=test_app.app.test_request_context()
