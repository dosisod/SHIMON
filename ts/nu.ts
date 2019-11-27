function nu(name: string, attribs?: [string, any], append?: HTMLElement, keep?: boolean): HTMLElement | null {
	if (!attribs) { //by using nu() without params, you will just get an elemnt by id
		return document.getElementById(name)
	}
	let node=document.createElement(name) //make the element we will be modifying

	if (attribs) {
		for (const attrib in attribs) {
			node[attrib]=attribs[attrib] //set property of node to each passed prop
		}
	}
	let old=node

	function iter(data: HTMLElement | string): void { //allows for append chaining
		if (data instanceof HTMLElement) { //if an html object append directly	
			node=<HTMLElement>data.appendChild(node).parentNode
		}
		else if (typeof data==="string") { //if string assume its an id, grab that id and append
			node=<HTMLElement>document.getElementById(data).appendChild(node).parentNode
		}
	}

	if (append) {
		let list=[]
		if (!Array.isArray(append)) list.push(append) //append to list if not a list
		else list=append //set to list if already a list
		
		list.forEach(function(e) { //append element into each other element
			iter(e)
		})
	}
	if (keep) {
		return old //returns original element (before appending)
	}
	return node //returns element after being appended
}