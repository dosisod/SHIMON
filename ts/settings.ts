function setting(e) { //make api calls based off setting type
	var type=e.attributes["data-type"] //this is only set for dropdowns
	if (type) type=type.value

	var str=e.innerText.toLowerCase()||e.id

	if (str=="change password") {
		var old=prompt("Enter old password")
		if (!old) return

		var nw=prompt("Enter new password")
		if (!nw) return

		post({"change pwd": {
			"old": old,
			"new": nw
		}})
	}
	else if (str=="generate new key") {
		if (!confirm("Are you sure? Generating new key will make your friends unable to talk to you until your new public key is sent out")) return

		var pwd=prompt("Enter password to confirm")
		if (!pwd) return

		post({"new key": pwd}, true)
	}
	else if (type=="EXPIRATION TIMER") {
		post({"expiration timer": e.value})
	}
	else if (type=="MSG DELETION") {
		post({"msg policy": e.value})
	}
	else if (type=="THEME") {
		post({"theme": e.value}).then(e=>{
			//force reload, show new colorscheme
			window.location.reload(true)
		})
	}
	else if (type=="ENABLE DEVELOPER MODE") {
		post({"devmode": e.className.includes("-unchecked")}).then(e=>{
			window.location.reload(true) //reload with dev mode settings loaded
		})
	}
	else if (str=="nuke cache") {
		if (!confirm("Are you sure you want to delete cache?")) return

		//password is needed for confirmation
		var pwd=prompt("Enter password to confirm")
		if (!pwd) return

		post({"nuke": pwd}, true)
	}
	else if (str=="fresh js") {
		post({"fresh js": e.className.includes("-unchecked")}).then(e=>{
			window.location.reload(true) //force reload with new js files
		})
	}
}