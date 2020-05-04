var lastError=0

const API_WAIT=5000

async function post(param: {[key: string]: any}, doRedirect: boolean=false): Promise<any> {
  clearError()

  param["redirect"]=!!doRedirect

  if (doRedirect) {
    const form=nu("form", {
      "id": "api-form",
      "action": "/api/",
      "method": "POST"
    })

    nu("input", {
      "type": "hidden",
      "name": "json",
      "value": JSON.stringify(param)
    }, form)

    const submit=nu("input", {
      "type": "submit",
      "style": "visibility: hidden;"
    }, [form, document.body], true)

    submit.click()

    nu("api-form").remove()
  }
  else {
    return fetch("/api/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(param)
    })
    .then(e=>e.json())
    .catch((response)=>{
      if (response.message=="NetworkError when attempting to fetch resource." || response.message=="Failed to fetch") {
        error("Network Disconnected")
        throw new Error("Network Disconnect: " + response.message)
      }
      else if (response.message.startsWith("JSON.parse: unexpected character at")) {
        error("Could Not Handle Request")
        throw new Error("Could Not Handle Request: " + response.message)
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
    clearError()
  }
}

async function setHeartbeat(func?: Function): Promise<void> {
  if (func) {
    setInterval(func, API_WAIT)
  }
  else {
    setInterval(heartbeat, API_WAIT)
  }
}

function clearError(): void {
  error(false)
}

function error(msg: string | boolean): void {
  if (typeof msg==="string") {
    lastError=Date.now()
    nu("error").style.display="block"
    nu("error").innerText=msg
  }
  else {
    if (Date.now() > (lastError + API_WAIT)) {
      nu("error").style.display="none"
      nu("error").innerText=""
    }
  }
}