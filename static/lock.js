function lock(e) {
	e.preventDefault()

	var str=prompt("Re-enter password to lock")

	//exit if user types nothing
	if (!str) return

	//redirect after lock
	post({"lock": str}, true)
}

function save(e) {
	e.preventDefault()

	var str=prompt("Re-enter password to save")

	//exit if user types nothing
	if (!str) return

	post({"save": str})
		.then(e=>{
			if (e["code"]==200) {
				document.getElementById("error").style.display="block"
				document.getElementById("error").innerText="Cache was successfully saved"
			}
		})
}