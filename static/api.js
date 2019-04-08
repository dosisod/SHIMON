function post(arr) { //construct api call from dictionary
	var form=nu("form", {
		"action": "/api/",
		"method": "POST"
	})

	for (i in arr) {
		nu("input", {
			"type": "hidden",
			"name": i,
			"value": arr[i]
		}, form)
	}
	var submit=nu("input", {
		"type": "submit",
		"style": "visibility: hidden;"
	})
	form.appendChild(submit)
	document.body.appendChild(form)
	submit.click()
}