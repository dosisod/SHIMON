function nu(name, attribs, append, keep) {
    if (!attribs) {
        return document.getElementById(name);
    }
    let node = document.createElement(name);
    if (attribs) {
        for (const attrib in attribs) {
            node[attrib] = attribs[attrib];
        }
    }
    let old = node;
    function iter(data) {
        if (data instanceof HTMLElement) {
            node = data.appendChild(node).parentNode;
        }
        else if (typeof data === "string") {
            node = document.getElementById(data).appendChild(node).parentNode;
        }
    }
    if (append) {
        let list = [];
        if (!Array.isArray(append))
            list.push(append);
        else
            list = append;
        list.forEach(function (e) {
            iter(e);
        });
    }
    if (keep) {
        return old;
    }
    return node;
}
