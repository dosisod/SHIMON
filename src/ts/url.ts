//change url to proper location eg /api -> /login
function url(path): void {
	history.replaceState({}, "", "/"+path)
}