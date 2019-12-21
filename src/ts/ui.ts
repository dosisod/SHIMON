type Dict={[key: string]: any}

var tray=nu("tray")
var friends=[]

declare var preload: Dict | boolean

async function check_friends(): Promise<void> { //get friends list if list is empty
	if (!friends.length) {
		friends=await post({"data":"friends"}) //wait for response
		friends=friends["msg"]
	}
}

function realname(id: string): string | undefined { //find name from id
	for (const i of friends) {
		if (i["id"]==id) return i["name"]
	}
	return undefined
}

function uname(name: string): string | undefined { //find id from name
	for (const i of friends) {
		if (i["name"]==name) return i["id"]
	}
	return undefined
}

async function reload_msgs(): Promise<void> {
	await check_friends() //make sure friends list is set

	//from MDN docs
	const user=document.cookie.replace(/(?:(?:^|.*;\s*)uname\s*\=\s*([^;]*).*$)|^.*$/, "$1")

	var raw: Dict | boolean
	if (!preload) {
		raw=await post({"data":{"allfor":user}})
		raw=raw["msg"]
	}
	else {
		raw=preload
		preload=false
	}

	if ((<Dict>raw).length==0) return

	const rawid=raw["id"] //must be stored like this as raw can change over time
	const data=raw["msgs"]

	//there is no data to loop through, sho default msg
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
					post({"status":""}).then(e=>{
						var pwd=undefined //only used by msg policy 2
						if (e.msg["msg policy"]==0) {
							if (!confirm("Are you sure you want to delete this message?")) return
						}
						else if (e.msg["msg policy"]==1) {
							pwd=prompt("Enter Password")
							if (!pwd) return
						}
						else if (e.msg["msg policy"]!=2) {
							return
						}

						post({"delete msg":{
							"id": rawid,
							"index": arr["index"],
							"pwd": pwd
						}})

						//reload the indexs of messages by refreshiNg
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
	//scrolls to bottom of page
	nu("reload").scrollIntoView()
}

async function reload_index(): Promise<void> {
	await check_friends()

	var raw: Dict | boolean
	//load from preload if available, else make api call
	if (!preload) {
		raw=await post({"data":"recent"})
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

async function replace_template(start: Complex, end?: Complex, params?: Dict | boolean, template?: Function): Promise<void> { //replace tray with nu elements
	//start and end are put at the start and end of the tray
	//template is a template to build items in the middle off of
	//params is an array of the params for the template

	//clear tray, add right bar
	tray.innerHTML=`<div class="rightbar"><a class="rightitem name point" href="/add">ADD FRIEND</a><br><a class="rightitem name point" href="/account">ACCOUNT</a><br><span class="rightitem name point" onclick="save(event)">SAVE</span></div>`

	if (typeof start==="string") tray.innerHTML+=start
	else if (start) tray.appendChild(<Node>start)

	if (params) {
		(<Dict>params).forEach((e,i)=>{
			e["index"]=i
			//append new item given params for template
			tray.appendChild(template(e))
		})
	}

	if (typeof end==="string") tray.innerHTML+=end
	else if (end) tray.appendChild(<Node>end)
}

function new_card(uuid: string, name: string, message: string, ret: boolean=false, disable: boolean=true, pointer: boolean=false): HTMLElement | undefined { //returns or appends a new card
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
	//if disable is set, onclick wont be added
	if (!disable) div.onclick=()=>window.location.href="/@"+uname(name)

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
	
	if (ret) {
		return card //stop here if you want to return it
	}
	
	tray.appendChild(card) //else just append it
	return undefined
}

function new_img(uuid: string): string { //converts uuid to b64 img of hash
	var canv=<HTMLCanvasElement>(nu("canvas", {
		"width": 16,
		"height": 16
	}))

	var draw: CanvasRenderingContext2D=canv.getContext("2d")

	var bin=""
	for (const i of uuid) {
		const tmp=parseInt(i,16).toString(2) //hex to binary string
		bin+="0".repeat(4-tmp.length)+tmp
	}

	for (let i=0;i<256;i++) { //16*16=256 pixels
		//set black or white pixel
		draw.fillStyle=(bin[i]=="1")?"rgb(255,255,255)":"rgb(0,0,0)"
		draw.fillRect(i%16, ~~(i/16), 1, 1) //draw single pixel
	}

	//return b64 for image src
	return canv.toDataURL()
}

function blank(msg: string): string { //prints welcome msg
	return `<div class="holder nopoint blank"><span class="title center">${msg}</span></div>`
}