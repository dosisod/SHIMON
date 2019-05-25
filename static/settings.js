function setting(e) { //make api calls based off setting type
	str=e.innerText.toLowerCase()

	if (str=="change password") {
		old=prompt("Enter old password")
		nw=prompt("Enter new password")

		//exit if either are not set
		if (!old||!nw) return

		post({"change pwd": {
			"old": old,
			"new": nw
		}})
	}
}