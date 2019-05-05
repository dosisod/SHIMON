function lock(e) {
	e.preventDefault()

	//dont lock if user says no
	if(!confirm("Do you want to lock?")) return

	post({"lock":""}, true) //redurect after lock
}
