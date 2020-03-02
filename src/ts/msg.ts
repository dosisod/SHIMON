async function send(keydown: KeyboardEvent): Promise<any> {
	const input=<HTMLInputElement>keydown.target

	if (keydown.key!="Enter") return
	if (!input.value) return

	await post({"send msg": {
		"uname": cookie("uname"),
		"msg": input.value
	}})
	.then((response)=>{
		if (response.code!=400) {
			reloadMsgs()
		}
	})

	input.value=""
}
