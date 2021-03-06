const setting = {

button: function(checkbox: HTMLElement): void {
  const selected=checkbox.innerText.toLowerCase().trim() || checkbox.id

  if (selected=="change password") {
    post({"change pwd": {
      "old": askForPassword("Enter old password"),
      "new": askForPassword("Enter new password")
    }})
  }
  else if (selected=="generate new key") {
    askForConfirmation("Are you sure? Generating new key will make your friends unable to talk to you until your new public key is sent out")

    post({
      "new key": askForPassword("Enter password to confirm")
    }, true)
  }
  else if (selected=="devmode") {
    post({"devmode": isChecked(checkbox)}).then(()=>{
      window.location.reload(true)
    })
  }
  else if (selected=="nuke cache") {
    askForConfirmation("Are you sure you want to delete cache?")

    post({
      "nuke": askForPassword("Enter password to confirm")
    }, true)
  }
  else if (selected=="fresh js") {
    post({"fresh js": isChecked(checkbox)}).then(()=>{
      window.location.reload(true)
    })
  }
  else if (selected=="fresh css") {
    post({"fresh css": isChecked(checkbox)}).then(()=>{
      window.location.reload(true)
    })
  }
},

dropdown: function(select: HTMLSelectElement): void {
  const selected=(
    select.getAttribute("data-type") || ""
  ).toLowerCase()

  if (selected=="expiration timer") {
    post({"expiration timer": select.value})
  }
  else if (selected=="msg deletion") {
    post({"msg policy": select.value})
  }
  else if (selected=="theme") {
    post({"theme": select.value}).then(()=>{
      window.location.reload(true)
    })
  }
}

}

function isChecked(checkbox: HTMLElement): boolean {
  return checkbox.className.includes("-unchecked")
}