function lock(e: MouseEvent) {
	e.preventDefault()

	const pwd=prompt("Re-enter password to lock")

	//exit if user types nothing
	if (!pwd) return

	//redirect after lock
	post({"lock": pwd}, true)
}

function save(e: MouseEvent) {
	e.preventDefault()

	const pwd=prompt("Re-enter password to save")

	//exit if user types nothing
	if (!pwd) return

	post({"save": pwd})
		.then(e=>{
			if (e["code"]==200) {
				error("Cache was successfully saved")
			}
		})
}