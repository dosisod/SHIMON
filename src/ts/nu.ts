/*! MIT Licnse for nu available at -> https://github.com/dosisod/nu */

type AppendableBase=HTMLElement | string

type Appendable=AppendableBase | AppendableBase[]

function nu(name: string, attribs?: {[attrib: string]: any}, appendTo?: Appendable, returnOld?: boolean): HTMLElement | null {
	if (!attribs) {
		return document.getElementById(name)
	}
	let currentNode=document.createElement(name)

	for (const attrib in attribs) {
		(currentNode as {[name: string]: any})[attrib]=attribs[attrib]
	}
	const oldNode=currentNode

	function append(data: HTMLElement | string): void {
		if (data instanceof HTMLElement) {
			currentNode=<HTMLElement>data.appendChild(currentNode).parentNode
		}
		else if (typeof data==="string") {
			currentNode=<HTMLElement>document.getElementById(data).appendChild(currentNode).parentNode
		}
	}

	if (appendTo) {
		if (Array.isArray(appendTo)) {
			appendTo.forEach(function(e: AppendableBase) {
				append(e)
			})
		}
		else {
			append(appendTo)
		}
	}
	if (returnOld) {
		return oldNode
	}
	return currentNode
}