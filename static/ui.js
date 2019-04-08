tray=document.getElementById("tray")

function new_card(u, n, m) { //adds new card to tray
	var name=document.createElement("li") //upper part of card (name)
	name.className="name"
	name.innerText=n
	var msg=document.createElement("li") //lower part of card (last msg)
	msg.className="msg"
	msg.innerText=m
	var ol=document.createElement("ol") //holds li elements
	ol.appendChild(name)
	ol.appendChild(msg)

	var div=document.createElement("div") //holds img and ol elements
	div.onclick=()=>alert(1) //placeholder function
	var img=new Image()
	img.src=new_img(u)
	div.appendChild(img)
	div.appendChild(document.createTextNode("\n"))
	div.appendChild(ol)

	var card=document.createElement("li")
	card.className="item"
	card.appendChild(div)

	tray.appendChild(card)
}
function new_img(uuid) { //converts uuid to b64 img of hash
	//
}