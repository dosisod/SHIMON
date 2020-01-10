async function send(keydown: KeyboardEvent): Promise<any> {
	const input=<HTMLInputElement>keydown.target

	if (keydown.key!="Enter") return
	if (!input.value) return

	await post({"send msg": {
		"uname": document.cookie.replace(/(?:(?:^|.*;\s*)uname\s*\=\s*([^;]*).*$)|^.*$/, "$1"),
		"msg": input.value
	}})
	.then((response)=>{
		if (response.code!=400) {
			reload_msgs()
		}
	})

	input.value=""
}
