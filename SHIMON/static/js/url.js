function url(s) { //change url to proper location eg /api -> /login
	history.replaceState({}, "", "/"+s)
}