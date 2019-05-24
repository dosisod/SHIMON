function setting(e) { //make api calls based off setting type
	str=e.innerText.toLowerCase()

	if (str=="change password") {
		post({"change pwd": {
			"old": prompt("Enter old password"),
			"new": prompt("Enter new password")
		}})
	}
}