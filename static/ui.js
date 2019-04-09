function new_card(u, n, m) { //adds card to tray
	//uuid, name, message

	tray=document.getElementById("tray")

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
	//
}