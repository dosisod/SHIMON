async function send(e) { //send msg to user
	//only send if enter was pressed
	if (e.key!="Enter"||!e.target.value) return

	//wait for message to send before procceding
	await post({"send msg":{
		"uname": document.cookie.replace(/(?:(?:^|.*;\s*)uname\s*\=\s*([^;]*).*$)|^.*$/, "$1"),
		"msg": e.target.value
	}}).then(e=>{
		if (e.code!=400) {
			//reload and scroll to bottom of page if msg was valid
			reload_msgs()
		}
	})

	e.target.value="" //reset input box
}
