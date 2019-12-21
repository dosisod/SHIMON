//time in ms when last error was set
var added_at=0

const api_wait=5000 //time to wait between api calls in ms

async function post(arr: {[key: string]: any}, redirect: boolean=false): Promise<any> { //construct api call from dictionary
	//if there is an error and it is able to be deleted, clear it
	error(false)

	//grab session cookie if available
	const session=document.cookie.replace(/(?:(?:^|.*;\s*)session\s*\=\s*([^;]*).*$)|^.*$/, "$1")

	if (session) arr["session"]=session
	arr["redirect"]=!!redirect

	const encode=function(str: string): string { //if any param passed is an object, jsonify it
		if (typeof str==="object") {
			try {
				return JSON.stringify(str)
			}
			catch {}
		}
		return str
	}

	if (redirect) { //create form, submit and follow it
		const form=nu("form", { //make nu empty form
			"id": "api-form",
			"action": "/api/",
			"method": "POST"
		})
	
		for (const i in arr) {
			nu("input", { //for each element make a nu hidden feild
				"type": "hidden",
				"name": i,
				"value": encode(arr[i])
			}, form)
		}
		const submit=nu("input", { //make nu submit button
			"type": "submit",
			"style": "visibility: hidden;"
		}, [form, document.body], true)
		
		submit.click() //send form

		nu("api-form").remove()
	}
	else { //only grab data from api
		var fd=new FormData()
		for (const i in arr) fd.append(i, encode(arr[i])) //fill formdata
	
		return fetch("/api/", {method:"POST", body:fd})
			.then(e=>e.json())
			.catch(e=>{
				console.log({"error":e.message})
				if (e.message=="NetworkError when attempting to fetch resource.") {
					error("Network Disconnected")
				}
				else if (e.message=="JSON.parse: unexpected character at line 1 column 1 of the JSON data") {
					error("Could Not Handle Request")
				}
			})
			.then(e=>{
				//if the request is to be rethrown, make the same request with redirects on
				if (e["code"]!=200) { //if error occurs, print it to the screen
					error(e["msg"])
				}
				if (e["rethrow"]=="") {
					post(arr, true)
				}
				else return e //return data
			})
	}
}

//pings the server, checks for connection
async function heartbeat(): Promise<void> {
	const pulse=await post({"ping":""})

	if (pulse.message=="NetworkError when attempting to fetch resource.") {
		error("Network Disconnected")
	}
	else error(false)
}

//if false, try to clear error, else, set error msg
function error(msg: string | boolean): void {
	if (typeof msg==="string") {
		added_at=Date.now()
		nu("error").style.display="block"
		nu("error").innerText=msg
	}
	else {
		if (Date.now()>(added_at+api_wait)) {
			nu("error").style.display="none"
			nu("error").innerText=""
		}
	}
}