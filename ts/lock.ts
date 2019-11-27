import { post, error } from "./api";

function lock(e: MouseEvent) {
	e.preventDefault()

	var str=prompt("Re-enter password to lock")

	//exit if user types nothing
	if (!str) return

	//redirect after lock
	post({"lock": str}, true)
}

function save(e: MouseEvent) {
	e.preventDefault()

	var str=prompt("Re-enter password to save")

	//exit if user types nothing
	if (!str) return

	post({"save": str})
		.then(e=>{
			if (e["code"]==200) {
				error("Cache was successfully saved")
			}
		})
}