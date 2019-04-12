async function post(arr, redirect) { //construct api call from dictionary
	if (redirect) { //create form, submit and follow it
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
		
		submit.click() //send form
	}
	else { //only grab data from api
		var fd=new FormData()
		for (i in arr) fd.append(i, arr[i]) //fill formdata
	
		return fetch("/api/", {method:"post", body:fd})
			.then(e=>e.json())
			.then(e=>{return e}) //return data
	}
}