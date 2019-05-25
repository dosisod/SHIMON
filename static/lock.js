function lock(e) {
	e.preventDefault()

	str=prompt("Re-enter password to lock")

	//exit if user types nothing
	if (!str) return

	//redirect after lock
	post({"lock": str}, true)
}
