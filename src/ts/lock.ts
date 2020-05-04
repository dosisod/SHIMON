function lock(click: MouseEvent) {
  click.preventDefault()

  post({
    "lock": askForPassword("Re-enter password to lock")
  }, true)
}

function save(click: MouseEvent) {
  click.preventDefault()

  post({
    "save": askForPassword("Re-enter password to save")
  })
  .then((response)=>{
    if (response["code"]==200) {
      error("Cache was successfully saved")
    }
  })
}