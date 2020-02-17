function url(path: string): void {
	history.replaceState({}, "", "/" + path)
}