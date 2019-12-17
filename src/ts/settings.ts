const setting = {

button: function(e: HTMLElement): void { //make api calls based off setting type
	const str=e.innerText.toLowerCase()||e.id

	if (str=="change password") {
		const old=prompt("Enter old password")
		if (!old) return

		const nw=prompt("Enter new password")
		if (!nw) return

		post({"change pwd": {
			"old": old,
			"new": nw
		}})
	}
	else if (str=="generate new key") {
		if (!confirm("Are you sure? Generating new key will make your friends unable to talk to you until your new public key is sent out")) return

		const pwd=prompt("Enter password to confirm")
		if (!pwd) return

		post({"new key": pwd}, true)
	}
	else if (str=="devmode") {
		post({"devmode": e.className.includes("-unchecked")}).then(()=>{
			window.location.reload(true) //reload with dev mode settings loaded
		})
	}
	else if (str=="nuke cache") {
		if (!confirm("Are you sure you want to delete cache?")) return

		//password is needed for confirmation
		const pwd=prompt("Enter password to confirm")
		if (!pwd) return

		post({"nuke": pwd}, true)
	}
	else if (str=="fresh js") {
		post({"fresh js": e.className.includes("-unchecked")}).then(()=>{
			window.location.reload(true) //force reload with new js files
		})
	}
	else if (str=="fresh css") {
		post({"fresh css": e.className.includes("-unchecked")}).then(()=>{
			window.location.reload(true) //force reload with new css files
		})
	}
},

dropdown: function(e: HTMLSelectElement): void {
	const type=e.attributes["data-type"].value

	if (type=="EXPIRATION TIMER") {
		post({"expiration timer": e.value})
	}
	else if (type=="MSG DELETION") {
		post({"msg policy": e.value})
	}
	else if (type=="THEME") {
		post({"theme": e.value}).then(()=>{
			//force reload, show new colorscheme
			window.location.reload(true)
		})
	}
}

}