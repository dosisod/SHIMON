var tray=document.getElementById("tray")

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
		"onclick": ()=>alert(1)
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