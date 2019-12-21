async function send(e: KeyboardEvent): Promise<any> { //send msg to user
	const target=<HTMLInputElement>e.target

	if (e.key!="Enter") return
	if (!target.value) return

	//wait for message to send before procceding
	await post({"send msg":{
		"uname": document.cookie.replace(/(?:(?:^|.*;\s*)uname\s*\=\s*([^;]*).*$)|^.*$/, "$1"),
		"msg": target.value
	}}).then(e=>{
		if (e.code!=400) {
			//reload and scroll to bottom of page if msg was valid
			reload_msgs()
		}
	})

	target.value=""
}
