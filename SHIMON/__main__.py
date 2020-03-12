import sys

if sys.version_info[0] < 3:
	raise Exception("Python 3.x is required to run SHIMON.")

from waitress import serve # type: ignore

from SHIMON.app import App

def run(app):
	print("starting SHIMON v" + app.shimon.VERSION + " -> github.com/dosisod/SHIMON\n")

	try:
		serve(
			app.app,
			host=app.IP,
			port=app.PORT,
			threads=6,
			clear_untrusted_proxy_headers=True
		)

	except OSError:
		print("Could not bind to port", app.PORT)
		print("Is SHIMON already running? if not, check port", app.PORT, "availability")

		sys.exit(1)

if __name__=="__main__":
	run(App())
