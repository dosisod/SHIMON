function lock(e) {
	e.preventDefault()

	//redirect after lock
	post({
		"lock": prompt("Re-enter password to lock")
	}, true)
}
