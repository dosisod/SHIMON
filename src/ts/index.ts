async function reloadIndex(): Promise<void> {
  const recent=await postOrPreload({"recent": ""})

  if (recent.length==0) {
    //if there are no msgs to display, display welcome msg
    replaceTemplate({
      "start": blank("Add a friend to start talking!")
    })

    return
  }

  replaceTemplate({
    "params": recent,
    "builder": (user: IRecentUser)=>{
      return makeNewCard({
        "uuid": user["hash"],
        "name": user["id"],
        "message": user["msgs"][user["msgs"].length-1]["msg"],
        "isClickable": true,
        "usePointer": true
      })
    }
  })
}
