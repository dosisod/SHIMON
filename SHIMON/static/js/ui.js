var tray = nu("tray");
var friends = [];
async function check_friends() {
    if (!friends.length) {
        friends = await post({ "data": "friends" });
        friends = friends["msg"];
    }
}
function realname(id) {
    for (var i of friends) {
        if (i["id"] == id)
            return i["name"];
    }
}
function uname(name) {
    for (var i of friends) {
        if (i["name"] == name)
            return i["id"];
    }
}
async function reload_msgs() {
    await check_friends();
    var user = document.cookie.replace(/(?:(?:^|.*;\s*)uname\s*\=\s*([^;]*).*$)|^.*$/, "$1");
    var raw;
    if (!preload) {
        raw = await post({ "data": { "allfor": user } });
        raw = raw["msg"];
    }
    else {
        raw = preload;
        preload = false;
    }
    if (raw.length == 0)
        return;
    var rawid = raw["id"];
    var data = raw["msgs"];
    if (!data.length) {
        replace_template(new_card(raw["hash"], realname(user), "", true, true).outerHTML + blank("Say hi to " + realname(user) + "!"), nu("span", {
            "className": "center name point",
            "id": "reload",
            "innerText": "RELOAD",
            "onclick": () => reload_msgs()
        }));
        return;
    }
    replace_template(new_card(raw["hash"], realname(user), "", true, true), nu("span", {
        "className": "center name point",
        "innerText": "RELOAD",
        "id": "reload",
        "onclick": () => reload_msgs()
    }), data, (arr) => {
        var ret = nu("span", {
            "className": arr["sending"] ? "x-sending" : "x-receiving",
            "innerText": "x",
            "onclick": (e) => {
                post({ "status": "" }).then(e => {
                    var pwd = undefined;
                    if (e.msg["msg policy"] == 0) {
                        if (!confirm("Are you sure you want to delete this message?"))
                            return;
                    }
                    else if (e.msg["msg policy"] == 1) {
                        pwd = prompt("Enter Password");
                        if (!pwd)
                            return;
                    }
                    else if (e.msg["msg policy"] != 2) {
                        return;
                    }
                    post({ "delete msg": {
                            "id": rawid,
                            "index": arr["index"],
                            "pwd": pwd
                        } });
                    reload_msgs();
                });
            }
        }, nu("li", {
            "className": "item"
        }));
        nu("span", {
            "className": "msg",
            "innerText": arr["msg"]
        }, [
            nu("div", {
                "className": "holder block " + (arr["sending"] ? "sending" : "receiving")
            }),
            ret
        ]);
        return ret;
    });
    nu("reload").scrollIntoView();
}
async function reload_index() {
    await check_friends();
    var raw;
    if (!preload) {
        raw = await post({ "data": "recent" });
        raw = raw["msg"];
    }
    else {
        raw = preload;
        preload = false;
    }
    if (!raw.length) {
        replace_template(blank("Add a friend to start talking!"), nu("span", {
            "className": "center name point",
            "id": "reload",
            "innerText": "RELOAD",
            "onclick": () => reload_index()
        }));
        return;
    }
    replace_template(undefined, nu("span", {
        "className": "center name point",
        "id": "reload",
        "innerText": "RELOAD",
        "onclick": () => reload_index()
    }), raw, (arr) => {
        return new_card(arr["hash"], realname(arr["id"]), arr["msgs"][arr["msgs"].length - 1]["msg"], true, false, true);
    });
}
async function replace_template(start, end, params, template) {
    tray.innerHTML = `<div class="rightbar"><a class="rightitem name point" href="/add">ADD FRIEND</a><br><a class="rightitem name point" href="/account">ACCOUNT</a><br><span class="rightitem name point" onclick="save(event)">SAVE</span></div>`;
    if (typeof start === "string")
        tray.innerHTML += start;
    else if (start)
        tray.appendChild(start);
    if (params) {
        params.forEach((e, i) => {
            e["index"] = i;
            tray.appendChild(template(e));
        });
    }
    if (typeof end === "string")
        tray.innerHTML += end;
    else if (end)
        tray.appendChild(end);
}
function new_card(uuid, name, message, ret = false, disable = true, pointer = false) {
    var ol = nu("ol", {});
    ol.appendChild(nu("li", {
        "className": "name title hide",
        "innerText": name
    }));
    ol.appendChild(nu("li", {
        "className": "msg hide",
        "innerText": message
    }));
    var div = nu("div", {
        "className": pointer ? "holder point" : "holder"
    });
    if (!disable)
        div.onclick = () => window.location.href = "/@" + uname(name);
    div.appendChild(nu("img", {
        "src": new_img(uuid)
    }));
    div.appendChild(document.createTextNode("\n"));
    div.appendChild(ol);
    var card = nu("li", {
        "className": "item"
    });
    card.appendChild(div);
    if (ret)
        return card;
    tray.appendChild(card);
}
function new_img(uuid) {
    var canv = (nu("canvas", {
        "width": 16,
        "height": 16
    }));
    var draw = canv.getContext("2d");
    var bin = "";
    for (let i of uuid) {
        var tmp = parseInt(i, 16).toString(2);
        bin += "0".repeat(4 - tmp.length) + tmp;
    }
    for (let i = 0; i < 256; i++) {
        draw.fillStyle = (bin[i] == "1") ? "rgb(255,255,255)" : "rgb(0,0,0)";
        draw.fillRect(i % 16, ~~(i / 16), 1, 1);
    }
    return canv.toDataURL();
}
function blank(msg) {
    return `<div class="holder nopoint blank"><span class="title center">${msg}</span></div>`;
}
