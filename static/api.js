function post(arr) { //construct api call from dictionary
	var form=nu("form", { //make nu empty form
		"action": "/api/",
		"method": "POST"
	})

	for (i in arr) {
		nu("input", { //for each element make a nu hidden feild
			"type": "hidden",
			"name": i,
			"value": arr[i]
		}, form)
	}
	var submit=nu("input", { //make nu submit button
		"type": "submit",
		"style": "visibility: hidden;"
	}, [form, document.body], true)
	
	submit.click()
}