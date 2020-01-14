type Dict={[key: string]: any}

var tray=nu("tray")
var friends=[]

declare var preload: Dict | boolean

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
	await check_friends()

	const user=document.cookie.replace(/(?:(?:^|.*;\s*)uname\s*\=\s*([^;]*).*$)|^.*$/, "$1")

	var raw: Dict | boolean
	if (!preload) {
		raw=await post({"allfor": user})
		raw=raw["msg"]
	}
	else {
		raw=preload
		preload=false
	}

	if ((<Dict>raw).length==0) return
	const data=raw["msgs"]

	//must be stored like this as raw can change over time
	const rawid=raw["id"]

	//there is no data to loop through, show default msg
	if (!data.length) {
		replace_template(
			new_card(
				raw["hash"],
				realname(user),
				"",
				true,
				true
			).outerHTML+blank("Say hi to "+realname(user)+"!"),
			nu("span", { //ending element
				"className": "center name point",
				"id": "reload",
				"innerText": "RELOAD",
				"onclick": ()=>reload_msgs()
			})
		)

		return
	}

	replace_template(
		new_card(
			raw["hash"],
			realname(user),
			"",
			true, //return the card instead of appending
			true //disable clicking of user card
		),
		nu("span", { //ending element
			"className": "center name point",
			"innerText": "RELOAD",
			"id": "reload",
			"onclick": ()=>reload_msgs()
		}),
		data, //parameters to feed the template
		(arr)=>{ //function template for creating cards
			var ret=nu("span", {
				"className": arr["sending"]?"x-sending":"x-receiving",
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
							"id": rawid,
							"index": arr["index"],
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
				"innerText": arr["msg"]
			}, [
				nu("div", {
					"className": "holder block "+(arr["sending"]?"sending":"receiving")
				}),
				ret
			])
			return ret
		}
	)
	nu("reload").scrollIntoView()
}

async function reload_index(): Promise<void> {
	await check_friends()

	var raw: Dict | boolean

	if (!preload) {
		raw=await post({"recent": ""})
		raw=raw["msg"]
	}
	else {
		raw=preload
		preload=false
	}

	//if there are no msgs to display, display welcome msg
	if (!(<Dict>raw).length) {
		replace_template(
			blank("Add a friend to start talking!"),
			nu("span", { //ending element
				"className": "center name point",
				"id": "reload",
				"innerText": "RELOAD",
				"onclick": ()=>reload_index()
			})
		)

		return
	}

	replace_template(
		undefined,
		nu("span", { //ending element
			"className": "center name point",
			"id": "reload",
			"innerText": "RELOAD",
			"onclick": ()=>reload_index()
		}),
		raw,
		(arr)=>{
			return new_card(
				arr["hash"], //hash of user id
				realname(arr["id"]), //realname of id
				arr["msgs"][arr["msgs"].length-1]["msg"], //last message
				true,
				false,
				true //use default cursor when hovering
			)
		}
	)
}

//replace tray with nu elements
async function replace_template(start: Appendable, end?: Appendable, params?: Dict | boolean, template?: Function): Promise<void> {
	//start and end are put at the start and end of the tray
	//template is a template to build items in the middle off of
	//params is an array of the params for the template

	//clear tray, add right bar
	tray.innerHTML=`<div class="rightbar"><a class="rightitem name point" href="/add">ADD FRIEND</a><br><a class="rightitem name point" href="/account">ACCOUNT</a><br><span class="rightitem name point" onclick="save(event)">SAVE</span></div>`

	if (typeof start==="string") tray.innerHTML+=start
	else if (start) tray.appendChild(<Node>start)

	if (params) {
		(<Dict>params).forEach((param, index)=>{
			param["index"]=index

			//append new item given params for template
			tray.appendChild(template(param))
		})
	}

	if (typeof end==="string") tray.innerHTML+=end
	else if (end) tray.appendChild(<Node>end)
}

function new_card(uuid: string, name: string, message: string, doReturnCard: boolean=false, disable: boolean=true, pointer: boolean=false): HTMLElement | undefined {
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
		"className": pointer?"holder point":"holder"
	})

	if (!disable) {
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

//converts uuid to b64 img of hash
function new_img(uuid: string): string {
	var canvas=<HTMLCanvasElement>(nu("canvas", {
		"width": 16,
		"height": 16
	}))

	var draw: CanvasRenderingContext2D=canvas.getContext("2d")

	var binary=""
	for (const character of uuid) {
		const bits=parseInt(character, 16).toString(2) //hex to binary string
		binary+="0".repeat(4-bits.length)+bits
	}

	for (let i=0;i<256;i++) {
		//set black or white pixel
		draw.fillStyle=(binary[i]=="1")?"rgb(255,255,255)":"rgb(0,0,0)"

		//draw single pixel
		draw.fillRect(i%16, ~~(i/16), 1, 1)
	}

	return canvas.toDataURL()
}

function blank(msg: string): string {
	return `<div class="holder nopoint blank"><span class="title center">${msg}</span></div>`
}