function setting(e) { //make api calls based off setting type
	str=e.innerText.toLowerCase()

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
	else if (["15 mins", "1 hour", "5 hours", "1 day"].indexOf(str)>-1) {
		post({"expiration timer": e.value})
	}
}