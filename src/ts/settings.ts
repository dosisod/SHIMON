const setting = {

button: function(checkbox: HTMLElement): void {
	const selected=checkbox.innerText.toLowerCase() || checkbox.id

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
		post({"devmode": checkbox.className.includes("-unchecked")}).then(()=>{
			//reload with dev mode settings loaded
			window.location.reload(true)
		})
	}
	else if (selected=="nuke cache") {
		if (!confirm("Are you sure you want to delete cache?")) return

		const pwd=prompt("Enter password to confirm")
		if (!pwd) return

		post({"nuke": pwd}, true)
	}
	else if (selected=="fresh js") {
		post({"fresh js": checkbox.className.includes("-unchecked")}).then(()=>{
			//force reload with new js files
			window.location.reload(true)
		})
	}
	else if (selected=="fresh css") {
		post({"fresh css": checkbox.className.includes("-unchecked")}).then(()=>{
			//force reload with new css files
			window.location.reload(true)
		})
	}
},

dropdown: function(select: HTMLSelectElement): void {
	const selected=select.attributes["data-type"].value

	if (selected=="EXPIRATION TIMER") {
		post({"expiration timer": select.value})
	}
	else if (selected=="MSG DELETION") {
		post({"msg policy": select.value})
	}
	else if (selected=="THEME") {
		post({"theme": select.value}).then(()=>{
			//force reload, show new colorscheme
			window.location.reload(true)
		})
	}
}

}