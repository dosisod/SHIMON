var last_error=0

const api_wait=5000

async function post(param: {[key: string]: any}, doRedirect: boolean=false): Promise<any> {
	clear_error()

	param["session"]=document.cookie.replace(/(?:(?:^|.*;\s*)session\s*\=\s*([^;]*).*$)|^.*$/, "$1")
	param["redirect"]=!!doRedirect

	//if any param passed is an object, jsonify it
	const encode=function(str: string): string {
		if (typeof str==="object") {
			try {
				return JSON.stringify(str)
			}
			catch {}
		}
		return str
	}

	if (doRedirect) {
		const form=nu("form", {
			"id": "api-form",
			"action": "/api/",
			"method": "POST"
		})
	
		for (const key in param) {
			nu("input", {
				"type": "hidden",
				"name": key,
				"value": encode(param[key])
			}, form)
		}
		const submit=nu("input", {
			"type": "submit",
			"style": "visibility: hidden;"
		}, [form, document.body], true)
		
		submit.click()

		nu("api-form").remove()
	}
	else {
		var formData=new FormData()
		for (const key in param) {
			formData.append(
				key,
				encode(param[key])
			)
		}
	
		return fetch("/api/", {method: "POST", body: formData})
			.then(e=>e.json())
			.catch((response)=>{
				console.log({"error": response.message})
				if (response.message=="NetworkError when attempting to fetch resource.") {
					error("Network Disconnected")
				}
				else if (response.message=="JSON.parse: unexpected character at line 1 column 1 of the JSON data") {
					error("Could Not Handle Request")
				}
			})
			.then((response)=>{
				if (response["code"]!=200) {
					error(response["msg"])
				}
				if (response["rethrow"]=="") {
					post(param, true)
				}
				else {
					return response
				}
			})
	}
}

async function heartbeat(): Promise<void> {
	const pulse=await post({"ping": ""})

	if (pulse.message=="NetworkError when attempting to fetch resource.") {
		error("Network Disconnected")
	}
	else {
		clear_error()
	}
}

function clear_error(): void {
	error(false)
}

function error(msg: string | boolean): void {
	if (typeof msg==="string") {
		last_error=Date.now()
		nu("error").style.display="block"
		nu("error").innerText=msg
	}
	else {
		if (Date.now()>(last_error+api_wait)) {
			nu("error").style.display="none"
			nu("error").innerText=""
		}
	}
}