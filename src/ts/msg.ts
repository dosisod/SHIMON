async function send(keydown: KeyboardEvent): Promise<any> {
  const input=<HTMLInputElement>keydown.target

  if (keydown.key!="Enter") return
  if (!input.value) return

  await post({"send msg": {
    "uname": cookie("uname"),
    "msg": input.value
  }})
  .then((response)=>{
    if (response.code!=400) {
      reloadMsgs()
    }
  })

  input.value=""
}

async function reloadMsgs(): Promise<void> {
  const user=cookie("uname")

  const raw=await postOrPreload({"allfor": user})

  if (raw.length==0) return
  const data=raw["msgs"]

  //must be stored like this as raw can change over time
  const rawId=raw["id"]

  if (data.length==0) {
    replaceTemplate({
      "start": makeNewCard({
        "uuid": raw["hash"],
        "name": user,
        "isClickable": false
      }).outerHTML + blank(`Say hi to ${realname(user)}!`)
    })

    return
  }

  replaceTemplate({
    "start": makeNewCard({
      "uuid": raw["hash"],
      "name": user,
      "isClickable": false
    }),
    "params": data,
    "builder": (user: IUserMsg)=>{
      return createMsg(user, rawId)
    }
  })
  nu("reload").scrollIntoView()
}

function createMsg(user: IUserMsg, userId: string) {
  const box=nu("span", {
    "className": user["sending"] ? "x-sending" : "x-receiving",
    "innerText": "x",
    "onclick": ()=>{
      post({"status": ""}).then((response)=>{
        if (response.msg["msg policy"]==0) {
          askForConfirmation("Are you sure you want to delete this message?")
        }
        else if (response.msg["msg policy"]==1) {
          var pwd=askForPassword("Enter Password")
        }
        else if (response.msg["msg policy"]!=2) {
          error("Invalid Request")
        }

        post({"delete msg":{
          "id": userId,
          "index": user["index"],
          "pwd": pwd || ""
        }})

        reloadMsgs()
      })
    }
  }, nu("li", {
    "className": "item"
  }))

  nu("span", {
    "className": "msg",
    "innerText": user["msg"]
  }, [
    nu("div", {
      "className": "holder block " + (
        user["sending"] ? "sending" : "receiving"
      )
    }),
    box
  ])
  return box
}
