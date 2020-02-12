from threading import Thread
from socket import socket

from SHIMON.__main__ import run

from testing.base import BaseTest

class TestMain(BaseTest):
	def test_main_exit_code_is_1_when_port_in_use(self) -> None:
		sock=socket()
		sock.bind((
			self.test_app.IP,
			self.test_app.PORT
		))
		sock.listen()

		try:
			run(self.test_app)

		except SystemExit as e:
			assert e.code==1

		sock.close()
