from waitress import serve

from SHIMON.app import App

if __name__=="__main__":
	app=App()

	print("starting SHIMON v"+app.shimon.VERSION+" -> github.com/dosisod/SHIMON")
	print("")

	try:
		serve(app.app, host=app.IP, port=app.PORT, threads=6)

	except OSError:
		print("Could not bind to port "+str(app.PORT))
		print("Is SHIMON already running? if not, check port "+str(app.PORT)+" availability")
