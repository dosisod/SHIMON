async function post(arr, redirect) { //construct api call from dictionary
	var encode=(s)=>{ //if any param passed is an object, jsonify it
		if (typeof s=="object") {
			try {
				return JSON.stringify(s)
			}
			catch {
				return s
			}
		}
		return s
	}

	if (redirect) { //create form, submit and follow it
		var form=nu("form", { //make nu empty form
			"action": "/api/",
			"method": "POST"
		})
	
		for (i in arr) {
			nu("input", { //for each element make a nu hidden feild
				"type": "hidden",
				"name": i,
				"value": encode(arr[i])
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
		for (i in arr) fd.append(i, encode(arr[i])) //fill formdata
	
		return fetch("/api/", {method:"POST", body:fd})
			.then(e=>e.json())
			.catch(e=>console.log({"error":e.message})) //returns any error
			.then(e=>{return e}) //return data
	}
}