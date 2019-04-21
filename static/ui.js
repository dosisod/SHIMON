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

function new_card(u, n, m) { //adds card to tray
	//uuid, name, message

	var ol=nu("ol")
	ol.appendChild(
		nu("li", {
			"className": "name",
			"innerText": n
		})
	)
	ol.appendChild(
		nu("li", {
			"className": "msg",
			"innerText": m
		})
	)

	var div=nu("div", {
		"className": "holder",
		"onclick": ()=>alert("Click")
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
	tray.appendChild(card)
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