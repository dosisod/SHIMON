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

	user=document.getElementById("uname").innerText //grab user passed from redirect

	raw=await post({"data":{"allfor":user}})
	data=raw["msgs"]

	replace_template(
		new_card(
			raw["id"],
			realname(user),
			"",
			true //return the card instead of appending
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
			"onclick": ()=>reload_msgs()
		})
	)
}

async function replace_template(start, template, params, end) { //replace tray with nu elements
	//start and end are put at the start and end of the tray
	//template is a template to build items in the middle off of
	//params is an array of the params for the template

	await check_friends() //always make sure that the friends list is populated

	tray.innerHTML=""

	if (start) tray.appendChild(start)

	params.forEach(e=>{
		tray.appendChild(template(e)) //spread out params into template
	})

	if (end) tray.appendChild(end)
}

async function replace_tray(arr) { //replaces tray with new data
	tray.innerHTML="" //clear tray

	await check_friends()

	//make sure cards are an array type
	var cards=(arr.constructor.name!="Array")?[arr]:arr

	for (var i of cards) {
		try {
			new_card(
				i["id"], //id from user
				realname(i["id"]), //name for given id
				i["msgs"][0]["msg"] //must recent message from user
			)
		}
		catch {} //just ignore
	}

	nu("span", {
		"className": "center name",
		"innerText": "RELOAD",
		"onclick": ()=>reload()
	}, "tray")
}

function reload() { //reloads recents
	post({"data":"recent"})
		.then(e=>replace_tray(e))
}

function new_card(u, n, m, r) { //returns or appends a new card
	//uuid, name, message, return

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
		"className": "holder",
		"onclick": ()=>post({"msg":uname(n)}, true)
	})

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
	for (i of uuid) bin+=parseInt(i,16).toString(2) //hex to binary string)
	bin="0".repeat(256-bin.length)+bin //add leading bits

	for (i=0;i<256;i++) { //16*16=256 pixels
		//set black or white pixel
		draw.fillStyle=(bin[i]=="1")?"rgb(255,255,255)":"rgb(0,0,0)"
		draw.fillRect(i%16, ~~(i/16), 1, 1) //draw single pixel
	}

	return canv.toDataURL()
}