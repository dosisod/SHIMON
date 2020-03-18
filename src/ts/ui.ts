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

async function reloadMsgs(): Promise<void> {
	const user=cookie("uname")

	const raw=await postOrPreload({"allfor": user})

	if (raw.length==0) return
	const data=raw["msgs"]

	//must be stored like this as raw can change over time
	const rawId=raw["id"]

	if (data.length==0) {
		replaceTemplate({
			"start": makeNewCard({
				"uuid": raw["hash"],
				"name": user,
				"isClickable": false
			}).outerHTML + blank("Say hi to " + realname(user) + "!"),
			"end": reloadButton(reloadMsgs)
		})

		return
	}

	replaceTemplate({
		"start": makeNewCard({
			"uuid": raw["hash"],
			"name": user,
			"isClickable": false
		}),
		"params": data,
		"builder": (user: IUserMsg)=>{
			return createMsg(user, rawId)
		},
		"end": reloadButton(reloadMsgs)
	})
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
		replaceTemplate({
			"start": blank("Add a friend to start talking!"),
			"end": reloadButton(reloadIndex)
		})

		return
	}

	replaceTemplate({
		"params": recent,
		"builder": (user: IRecentUser)=>{
			return makeNewCard({
				"uuid": user["hash"],
				"name": user["id"],
				"message": user["msgs"][user["msgs"].length-1]["msg"],
				"isClickable": true,
				"usePointer": true
			})
		},
		"end": reloadButton(reloadIndex)
	})
}

async function postOrPreload(data: Dict): Promise<Dict> {
	await checkFriends()

	if (preload) {
		const raw=<Dict>preload
		preload=false

		return raw
	}
	else {
		return (await post(data))["msg"]
	}
}

interface ITemplateData {
	start?: Appendable,
	params?: Dict | false,
	builder?: Function
	end?: Appendable
}

function replaceTemplate(template: ITemplateData): void {
	tray.innerHTML=""
	addAppendable(tray, template.start)

	if (template.params) {
		template.params.forEach((param: Dict, index: number)=>{
			param["index"]=index

			if (template.builder) {
				tray.appendChild(template.builder(param))
			}
		})
	}

	addAppendable(tray, template.end)
}

function addAppendable(node: HTMLElement, append?: Appendable): void {
	if (typeof append==="string") {
		node.innerHTML+=append
	}
	else if (append) {
		node.appendChild(<Node>append)
	}
}

interface ICardData {
	uuid: string,
	name: string,
	message?: string,
	isClickable?: boolean,
	usePointer?: boolean
}

function makeNewCard(card: ICardData): HTMLElement {
	const name=realname(card.name)

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
			"innerText": card.message || ""
		})
	)

	const div=nu("div", {
		"className": card.usePointer ? "holder point" : "holder"
	})

	if (card.isClickable) {
		div.onclick=()=>{
			window.location.href="/@" + card.name
		}
	}

	div.appendChild(makeProfilePic(card.uuid, name))
	div.appendChild(document.createTextNode("\n"))
	div.appendChild(ol)

	const li=nu("li", {
		"className": "item"
	})
	li.appendChild(div)

	return li
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
	profilePic.style.background="#" + color

	//https://stackoverflow.com/a/33890907
	profilePic.style.color=(parseInt(color, 16) > 0xffffff / 2) ?
		"#000" : "#fff"

	return <HTMLDivElement>profilePic
}

function blank(msg: string): string {
	return nu("span", {
		"className": "title center",
		"innerText": msg
	}, nu("div", {
		"className": "holder nopoint blank"
	})).outerHTML
}