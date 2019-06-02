var tray=document.getElementById("tray")
var friends=[]

async function check_friends() { //get friends list if list is empty
	if (!friends.length) {
		friends=await post({"data":"friends"}) //wait for response
	}
}

function realname(id) { //find name from id
	for (i of friends) {
		if (i["id"]==id) return i["name"]
	}
}

function uname(name) { //find id from name
	for (i of friends) {
		if (i["name"]==name) return i["id"]
	}
}

async function reload_msgs() {
	await check_friends() //make sure friends list is set

	//from MDN docs
	user=document.cookie.replace(/(?:(?:^|.*;\s*)uname\s*\=\s*([^;]*).*$)|^.*$/, "$1")

	raw=await post({"data":{"allfor":user}})
	data=raw["msgs"]

	replace_template(
		new_card(
			raw["id"],
			realname(user),
			"",
			true, //return the card instead of appending
			true //disable clicking of user card
		),
		(arr)=>{ //function template for creating cards
			return nu("span", {
				"className": "msg",
				"innerText": arr["msg"]
			}, [
				nu("div", {
					"className": "holder block "+(arr["sending"]?"sending":"receiving")
				}),
				nu("li", {
					"className": "item"
				})
			])
		},
		data, //parameters to feed the template
		nu("span", { //ending element
			"className": "center name",
			"innerText": "RELOAD",
			"id": "reload",
			"onclick": ()=>reload_msgs()
		})
	)
}

async function reload_index() {
	await check_friends()

	raw=await post({"data":"recent"})

	replace_template(
		undefined,
		(arr)=>{
			return new_card(
				arr["id"], //id of user
				realname(arr["id"]), //realname of id
				arr["msgs"][arr["msgs"].length-1]["msg"], //last message
				true
			)
		},
		raw,
		nu("span", { //ending element
			"className": "center name",
			"innerText": "RELOAD",
			"onclick": ()=>reload_index()
		})

	)
}

async function replace_template(start, template, params, end) { //replace tray with nu elements
	//start and end are put at the start and end of the tray
	//template is a template to build items in the middle off of
	//params is an array of the params for the template

	tray.innerHTML="" //clear old tray

	//always add the right bar (settings and lock buttons)
	div=nu("div", {"className": "rightbar"})

	nu("span", {
		"innerText": "SETTINGS",
		"className": "rightitem name",
		"onclick": (e)=>window.location="/settings"
	}, div)

	nu("br", {}, div)

	nu("span", {
		"innerText": "LOCK",
		"className": "rightitem name",
		"onclick": (e)=>lock(e)
	}, div)

	tray.appendChild(div)

	if (start) tray.appendChild(start)

	params.forEach(e=>{
		//append new item given params for template
		tray.appendChild(template(e))
	})

	if (end) tray.appendChild(end)
}

function new_card(u, n, m, r, d) { //returns or appends a new card
	//uuid, name, message, return (card), disable (click)

	var ol=nu("ol")
	ol.appendChild(
		nu("li", {
			"className": "name hide",
			"innerText": n
		})
	)
	ol.appendChild(
		nu("li", {
			"className": "msg hide",
			"innerText": m
		})
	)

	var div=nu("div", {
		"className": "holder"
	})
	//if disable is set, onclick wont be added
	if (!d) div.onclick=()=>post({"msg":uname(n)}, true)

	div.appendChild(
		nu("img", {
			"src": new_img(u)
		})
	)
	div.appendChild(document.createTextNode("\n"))
	div.appendChild(ol)

	var card=nu("li", {
		"className": "item"
	})
	card.appendChild(div)
	
	if (r) return card //stop here if you want to return it
	
	tray.appendChild(card) //else just append it
}
function new_img(uuid) { //converts uuid to b64 img of hash
	var canv=nu("canvas", {
		"width": 16,
		"height": 16
	})
	var draw=canv.getContext("2d")

	bin=""
	for (i of uuid) bin+=parseInt(i,16).toString(2) //hex to binary string
	bin="0".repeat(256-bin.length)+bin //add leading bits

	for (i=0;i<256;i++) { //16*16=256 pixels
		//set black or white pixel
		draw.fillStyle=(bin[i]=="1")?"rgb(255,255,255)":"rgb(0,0,0)"
		draw.fillRect(i%16, ~~(i/16), 1, 1) //draw single pixel
	}

	//return b64 for image src
	return canv.toDataURL()
}