function lock(click: MouseEvent) {
	click.preventDefault()

	const pwd=prompt("Re-enter password to lock")
	if (!pwd) return

	//redirect after lock
	post({"lock": pwd}, true)
}

function save(click: MouseEvent) {
	click.preventDefault()

	const pwd=prompt("Re-enter password to save")
	if (!pwd) return

	post({"save": pwd})
		.then((response)=>{
			if (response["code"]==200) {
				error("Cache was successfully saved")
			}
		})
}