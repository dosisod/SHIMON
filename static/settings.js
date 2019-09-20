function setting(e) { //make api calls based off setting type
	str=e.innerText.toLowerCase()||e.id

	if (str=="change password") {
		old=prompt("Enter old password")
		if (!old) return

		nw=prompt("Enter new password")
		if (!nw) return

		post({"change pwd": {
			"old": old,
			"new": nw
		}})
	}
	else if (str=="generate new key") {
		if (!confirm("Are you sure? Generating new key will make your friends unable to talk to you until your new public key is sent out")) return

		pwd=prompt("Enter password to confirm")
		if (!pwd) return

		post({"new key": pwd}, true)
	}
	else if (["15 mins", "1 hour", "5 hours", "1 day"].indexOf(str)>-1) {
		post({"expiration timer": e.value})
	}
	else if (str=="darkmode") {
		post({"darkmode": e.checked}) //darkmode will be set to what is sent here
	}
	else if (str=="devmode") {
		post({"devmode": e.checked}) //developer mode will be set to what is sent here
	}
	else if (str=="nuke cache") {
		if (!confirm("Are you sure you want to delete cache?")) return

		//password is needed for confirmation
		pwd=prompt("Enter password to confirm")
		if (!pwd) return

		post({"nuke": pwd}, true)
	}
}