async function post(arr, redirect) { //construct api call from dictionary
	//grab session cookie if available
	session=document.cookie.replace(/(?:(?:^|.*;\s*)session\s*\=\s*([^;]*).*$)|^.*$/, "$1")

	if (session) arr["session"]=session
	arr["redirect"]=!!redirect

	var encode=(s)=>{ //if any param passed is an object, jsonify it
		if (typeof s=="object") {
			try {
				return JSON.stringify(s)
			}
			catch {}
		}
		return s
	}

	if (redirect) { //create form, submit and follow it
		var form=nu("form", { //make nu empty form
			"id": "api-form",
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

		document.getElementById("api-form").remove()
	}
	else { //only grab data from api
		var fd=new FormData()
		for (i in arr) fd.append(i, encode(arr[i])) //fill formdata
	
		return fetch("/api/", {method:"POST", body:fd})
			.then(e=>e.json())
			.catch(e=>{
				console.log({"error":e.message})
				if (e.message=="NetworkError when attempting to fetch resource.") {
					document.getElementById("error").innerText="Network Disconnected"
				}
			})
			.then(e=>{
				//if there is an error redirect to error page
				if (100<=e["error"]&&e["error"]<=505) {
					window.location="/error/"+e["error"]
				}
				else return e //return data
			})
	}
}