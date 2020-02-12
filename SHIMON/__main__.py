from waitress import serve # type: ignore
import sys

from .app import App

def run(app: App) -> None:
	print("starting SHIMON v" + app.shimon.VERSION + " -> github.com/dosisod/SHIMON")
	print("")

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
