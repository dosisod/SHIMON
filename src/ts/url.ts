function url(path): void { //change url to proper location eg /api -> /login
	history.replaceState({}, "", "/"+path)
}