type Dict={[key: string]: any}

var tray=nu("tray")
var friends=[]

declare var preload: Dict | false

async function check_friends(): Promise<void> {
	if (!friends.length) {
		friends=await post({"friends": ""})
		friends=friends["msg"]
	}
}

function realname(id: string): string | undefined {
	for (const friend of friends) {
		if (friend["id"]==id) return friend["name"]
	}
	return undefined
}

function uname(name: string): string | undefined {
	for (const friend of friends) {
		if (friend["name"]==name) return friend["id"]
	}
	return undefined
}

async function reload_msgs(): Promise<void> {
	const user=document.cookie.replace(/(?:(?:^|.*;\s*)uname\s*\=\s*([^;]*).*$)|^.*$/, "$1")

	const raw=await post_or_preload({"allfor": user})

	if (raw.length==0) return
	const data=raw["msgs"]

	//must be stored like this as raw can change over time
	const rawId=raw["id"]

	if (data.length==0) {
		replace_template(
			new_card(
				raw["hash"],
				realname(user),
				"", //message
				true, //doReturnCard
				false //isClickable
			).outerHTML + blank("Say hi to " + realname(user) + "!"),
			reload_button(reload_msgs)
		)

		return
	}

	replace_template(
		new_card(
			raw["hash"],
			realname(user),
			"", //message
			true, //doReturnCard
			false //isClickable
		),
		reload_button(reload_msgs),
		data,
		(user)=>{
			return create_msg(user, rawId)
		}
	)
	nu("reload").scrollIntoView()
}

function create_msg(user, userId) {
	var box=nu("span", {
		"className": user["sending"] ? "x-sending" : "x-receiving",
		"innerText": "x",
		"onclick": ()=>{
			post({"status": ""}).then((response)=>{
				if (response.msg["msg policy"]==0) {
					askForConfirmation("Are you sure you want to delete this message?")
				}
				else if (response.msg["msg policy"]==1) {
					var pwd=askForPassword("Enter Password")
				}
				else if (response.msg["msg policy"]!=2) {
					error("Invalid Request")
				}

				post({"delete msg":{
					"id": userId,
					"index": user["index"],
					"pwd": pwd || ""
				}})

				reload_msgs()
			})
		}
	}, nu("li", {
		"className": "item"
	}))

	nu("span", {
		"className": "msg",
		"innerText": user["msg"]
	}, [
		nu("div", {
			"className": "holder block " + (
				user["sending"] ? "sending" : "receiving"
			)
		}),
		box
	])
	return box
}

async function reload_index(): Promise<void> {
	const recent=await post_or_preload({"recent": ""})

	if (recent.length==0) {
		//if there are no msgs to display, display welcome msg
		replace_template(
			blank("Add a friend to start talking!"),
			reload_button(reload_index)
		)

		return
	}

	replace_template(
		undefined,
		reload_button(reload_index),
		recent,
		(user)=>{
			return new_card(
				user["hash"],
				realname(user["id"]),
				user["msgs"][user["msgs"].length-1]["msg"],
				true, //doReturnCard
				true, //isClickable
				true //usePointer
			)
		}
	)
}

async function post_or_preload(data: Dict): Promise<Dict> {
	await check_friends()

	if (preload) {
		const raw=<Dict>preload
		preload=false

		return raw
	}
	else {
		return (
			await post(data)
		)["msg"]
	}
}

async function replace_template(start: Appendable, end?: Appendable, params?: Dict | false, template?: Function): Promise<void> {
	//clear tray, add right bar
	tray.innerHTML=`<div class="rightbar"><a class="rightitem name point" href="/add">ADD FRIEND</a><br><a class="rightitem name point" href="/account">ACCOUNT</a><br><span class="rightitem name point" onclick="save(event)">SAVE</span></div>`

	if (typeof start==="string") {
		tray.innerHTML+=start
	}
	else if (start) {
		tray.appendChild(<Node>start)
	}

	if (params) {
		params.forEach((param, index)=>{
			param["index"]=index

			tray.appendChild(template(param))
		})
	}

	if (typeof end==="string") {
		tray.innerHTML+=end
	}
	else if (end) {
		tray.appendChild(<Node>end)
	}
}

function new_card(uuid: string, name: string, message: string, doReturnCard: boolean=false, isClickable: boolean=false, usePointer: boolean=false): HTMLElement | undefined {
	var ol=nu("ol", {})
	ol.appendChild(
		nu("li", {
			"className": "name title hide",
			"innerText": name
		})
	)
	ol.appendChild(
		nu("li", {
			"className": "msg hide",
			"innerText": message
		})
	)

	var div=nu("div", {
		"className": usePointer ? "holder point" : "holder"
	})

	if (isClickable) {
		div.onclick=()=>{
			window.location.href="/@"+uname(name)
		}
	}

	div.appendChild(
		nu("img", {
			"src": new_img(uuid),
			"alt": name+"'s profile img"
		})
	)
	div.appendChild(document.createTextNode("\n"))
	div.appendChild(ol)

	var card=nu("li", {
		"className": "item"
	})
	card.appendChild(div)
	
	if (doReturnCard) {
		return card
	}
	
	tray.appendChild(card)
	return undefined
}

function reload_button(func) {
	return nu("span", {
		"className": "center name point",
		"id": "reload",
		"innerText": "RELOAD",
		"onclick": ()=>func()
	})
}

function new_img(uuid: string): string {
	var canvas=<HTMLCanvasElement>(nu("canvas", {
		"width": 16,
		"height": 16
	}))

	var draw: CanvasRenderingContext2D=canvas.getContext("2d")

	var binary=""
	for (const character of uuid) {
		const bits=parseInt(character, 16)
			.toString(2)

		binary+="0".repeat(4-bits.length)+bits
	}

	for (let i=0; i<256; i++) {
		draw.fillStyle=(binary[i]=="1") ?
			"rgb(255,255,255)" :
			"rgb(0,0,0)"

		draw.fillRect(i%16, ~~(i / 16), 1, 1)
	}

	return canvas.toDataURL()
}

function blank(msg: string): string {
	return `<div class="holder nopoint blank"><span class="title center">${msg}</span></div>`
}