var tray=nu("tray")
var friends=[]

async function check_friends() { //get friends list if list is empty
	if (!friends.length) {
		friends=await post({"data":"friends"}) //wait for response
		friends=friends["msg"]
	}
}

function realname(id) { //find name from id
	for (var i of friends) {
		if (i["id"]==id) return i["name"]
	}
}

function uname(name) { //find id from name
	for (var i of friends) {
		if (i["name"]==name) return i["id"]
	}
}

async function reload_msgs() {
	await check_friends() //make sure friends list is set

	//from MDN docs
	var user=document.cookie.replace(/(?:(?:^|.*;\s*)uname\s*\=\s*([^;]*).*$)|^.*$/, "$1")

	if (!preload) {
		var raw=await post({"data":{"allfor":user}})
		raw=raw["msg"]
	}
	else {
		var raw=preload
		preload=false
	}

	if (raw.length==0) return

	var rawid=raw["id"] //must be stored like this as raw can change over time
	var data=raw["msgs"]

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
				"onclick": (e)=>{
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

async function reload_index() {
	await check_friends()

	//load from preload if available, else make api call
	if (!preload) {
		var raw=await post({"data":"recent"})
		raw=raw["msg"]
	}
	else {
		var raw=preload
		preload=false
	}

	//if there are no msgs to display, display welcome msg
	if (!raw.length) {
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

async function replace_template(start, end, params, template) { //replace tray with nu elements
	//start and end are put at the start and end of the tray
	//template is a template to build items in the middle off of
	//params is an array of the params for the template

	//clear tray, add right bar
	tray.innerHTML=`<div class="rightbar"><a class="rightitem name point" href="/add">ADD FRIEND</a><br><a class="rightitem name point" href="/account">ACCOUNT</a><br><span class="rightitem name point" onclick="save(event)">SAVE</span></div>`

	if (typeof start==="string") tray.innerHTML+=start
	else if (start) tray.appendChild(start)

	if (params) {
		params.forEach((e,i)=>{
			e["index"]=i
			//append new item given params for template
			tray.appendChild(template(e))
		})
	}

	if (end) tray.appendChild(end)
}

function new_card(uuid, name, message, ret, disable, pointer) { //returns or appends a new card
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
	if (!disable) div.onclick=()=>window.location="/msg/"+uname(name)

	div.appendChild(
		nu("img", {
			"src": new_img(uuid)
		})
	)
	div.appendChild(document.createTextNode("\n"))
	div.appendChild(ol)

	var card=nu("li", {
		"className": "item"
	})
	card.appendChild(div)
	
	if (ret) return card //stop here if you want to return it
	
	tray.appendChild(card) //else just append it
}

function new_img(uuid) { //converts uuid to b64 img of hash
	var canv=nu("canvas", {
		"width": 16,
		"height": 16
	})
	var draw=canv.getContext("2d")

	var bin=""
	for (var i of uuid) {
		var tmp=parseInt(i,16).toString(2) //hex to binary string
		bin+="0".repeat(4-tmp.length)+tmp
	}

	for (var i=0;i<256;i++) { //16*16=256 pixels
		//set black or white pixel
		draw.fillStyle=(bin[i]=="1")?"rgb(255,255,255)":"rgb(0,0,0)"
		draw.fillRect(i%16, ~~(i/16), 1, 1) //draw single pixel
	}

	//return b64 for image src
	return canv.toDataURL()
}

function blank(msg) { //prints welcome msg
	return `<div class="holder nopoint blank"><span class="title center">${msg}</span></div>`
}