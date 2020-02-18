type Dict={[key: string]: any}

const tray=nu("tray")

interface IFriend {
	hash: string;
	id: string;
	name: string;
}

var friends: IFriend[]=[]

declare var preload: Dict | false

async function checkFriends(): Promise<void> {
	if (!friends.length) {
		friends=(await post({"friends": ""}))["msg"]
	}
}

function realname(id: string): string {
	for (const friend of friends) {
		if (friend["id"]==id) return friend["name"]
	}
	return ""
}

function uname(name: string): string {
	for (const friend of friends) {
		if (friend["name"]==name) return friend["id"]
	}
	return ""
}

async function reloadMsgs(): Promise<void> {
	const user=document.cookie.replace(/(?:(?:^|.*;\s*)uname\s*\=\s*([^;]*).*$)|^.*$/, "$1")

	const raw=await postOrPreload({"allfor": user})

	if (raw.length==0) return
	const data=raw["msgs"]

	//must be stored like this as raw can change over time
	const rawId=raw["id"]

	if (data.length==0) {
		replaceTemplate(
			newCard(
				raw["hash"],
				realname(user),
				"", //message
				false //isClickable
			).outerHTML + blank("Say hi to " + realname(user) + "!"),
			reloadButton(reloadMsgs)
		)

		return
	}

	replaceTemplate(
		newCard(
			raw["hash"],
			realname(user),
			"", //message
			false //isClickable
		),
		reloadButton(reloadMsgs),
		data,
		(user: IUserMsg)=>{
			return createMsg(user, rawId)
		}
	)
	nu("reload").scrollIntoView()
}

interface IUserMsg {
	sending: boolean;
	msg: string;
	index: number;
}

function createMsg(user: IUserMsg, userId: string) {
	const box=nu("span", {
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

				reloadMsgs()
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

interface IRecentUser {
	hash: string;
	id: string;
	msgs: IUserMsg[];
}

async function reloadIndex(): Promise<void> {
	const recent=await postOrPreload({"recent": ""})

	if (recent.length==0) {
		//if there are no msgs to display, display welcome msg
		replaceTemplate(
			blank("Add a friend to start talking!"),
			reloadButton(reloadIndex)
		)

		return
	}

	replaceTemplate(
		undefined,
		reloadButton(reloadIndex),
		recent,
		(user: IRecentUser)=>{
			return newCard(
				user["hash"],
				realname(user["id"]),
				user["msgs"][user["msgs"].length-1]["msg"],
				true, //isClickable
				true //usePointer
			)
		}
	)
}

async function postOrPreload(data: Dict): Promise<Dict> {
	await checkFriends()

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

async function replaceTemplate(start?: Appendable, end?: Appendable, params?: Dict | false, template?: Function): Promise<void> {
	//clear tray, add right bar
	tray.innerHTML=`<div class="rightbar"><a class="rightitem name point" href="/add">ADD FRIEND</a><br><a class="rightitem name point" href="/account">ACCOUNT</a><br><span class="rightitem name point" onclick="save(event)">SAVE</span></div>`

	if (typeof start==="string") {
		tray.innerHTML+=start
	}
	else if (start) {
		tray.appendChild(<Node>start)
	}

	if (params && template) {
		params.forEach((param: Dict, index: number)=>{
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

function newCard(uuid: string, name: string, message: string, isClickable: boolean=false, usePointer: boolean=false): HTMLElement {
	const ol=nu("ol", {})
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

	const div=nu("div", {
		"className": usePointer ? "holder point" : "holder"
	})

	if (isClickable) {
		div.onclick=()=>{
			window.location.href="/@"+uname(name)
		}
	}

	div.appendChild(makeProfilePic(uuid, name))
	div.appendChild(document.createTextNode("\n"))
	div.appendChild(ol)

	const card=nu("li", {
		"className": "item"
	})
	card.appendChild(div)

	return card
}

function reloadButton(func: Function) {
	return nu("span", {
		"className": "center name point",
		"id": "reload",
		"innerText": "RELOAD",
		"onclick": ()=>func()
	})
}

function makeProfilePic(uuid: string, name: string): HTMLDivElement {
	const profilePic=nu("div", {
		"className": "profile-pic-img",
		"innerText": name[0]
	})

	const color=uuid.slice(0, 6)
	profilePic.style.background="#" + uuid.slice(0, 6)

	//https://stackoverflow.com/a/33890907
	profilePic.style.color=(parseInt(color, 16) > 0xffffff / 2) ?
		"#000" : "#fff"

	return <HTMLDivElement>profilePic
}

function blank(msg: string): string {
	return `<div class="holder nopoint blank"><span class="title center">${msg}</span></div>`
}