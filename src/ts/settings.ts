const setting = {

button: function(e: HTMLElement): void { //make api calls based off setting type
	const selected=e.innerText.toLowerCase()||e.id

	if (selected=="change password") {
		const oldPwd=prompt("Enter old password")
		if (!oldPwd) return

		const newPwd=prompt("Enter new password")
		if (!newPwd) return

		post({"change pwd": {
			"old": oldPwd,
			"new": newPwd
		}})
	}
	else if (selected=="generate new key") {
		if (!confirm("Are you sure? Generating new key will make your friends unable to talk to you until your new public key is sent out")) return

		const pwd=prompt("Enter password to confirm")
		if (!pwd) return

		post({"new key": pwd}, true)
	}
	else if (selected=="devmode") {
		post({"devmode": e.className.includes("-unchecked")}).then(()=>{
			window.location.reload(true) //reload with dev mode settings loaded
		})
	}
	else if (selected=="nuke cache") {
		if (!confirm("Are you sure you want to delete cache?")) return

		//password is needed for confirmation
		const pwd=prompt("Enter password to confirm")
		if (!pwd) return

		post({"nuke": pwd}, true)
	}
	else if (selected=="fresh js") {
		post({"fresh js": e.className.includes("-unchecked")}).then(()=>{
			window.location.reload(true) //force reload with new js files
		})
	}
	else if (selected=="fresh css") {
		post({"fresh css": e.className.includes("-unchecked")}).then(()=>{
			window.location.reload(true) //force reload with new css files
		})
	}
},

dropdown: function(e: HTMLSelectElement): void {
	const selected=e.attributes["data-type"].value

	if (selected=="EXPIRATION TIMER") {
		post({"expiration timer": e.value})
	}
	else if (selected=="MSG DELETION") {
		post({"msg policy": e.value})
	}
	else if (selected=="THEME") {
		post({"theme": e.value}).then(()=>{
			//force reload, show new colorscheme
			window.location.reload(true)
		})
	}
}

}