function url(path): void {
	history.replaceState({}, "", "/" + path)
}