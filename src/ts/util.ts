function cookie(name: string) {
	return document.cookie.replace(
		new RegExp("(?:(?:^|.*;\\s*)" + name + "\\s*\\=\\s*([^;]*).*$)|^.*$"),
		"$1"
	)
}
