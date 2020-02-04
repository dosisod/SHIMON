from .error import error_401

from ..__init__ import HttpResponse

def nuke(self, pwd: str, redirect: bool) -> HttpResponse:
	if self.security.correct_pwd(pwd):
		return self.session.create(fresh=True)

	return error_401()
