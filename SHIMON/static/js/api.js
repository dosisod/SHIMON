var added_at = 0;
async function post(arr, redirect = false) {
    error(false);
    var session = document.cookie.replace(/(?:(?:^|.*;\s*)session\s*\=\s*([^;]*).*$)|^.*$/, "$1");
    if (session)
        arr["session"] = session;
    arr["redirect"] = !!redirect;
    var encode = (s) => {
        if (typeof s == "object") {
            try {
                return JSON.stringify(s);
            }
            catch { }
        }
        return s;
    };
    if (redirect) {
        var form = nu("form", {
            "id": "api-form",
            "action": "/api/",
            "method": "POST"
        });
        for (var i in arr) {
            nu("input", {
                "type": "hidden",
                "name": i,
                "value": encode(arr[i])
            }, form);
        }
        var submit = nu("input", {
            "type": "submit",
            "style": "visibility: hidden;"
        }, [form, document.body], true);
        submit.click();
        nu("api-form").remove();
    }
    else {
        var fd = new FormData();
        for (var i in arr)
            fd.append(i, encode(arr[i]));
        return fetch("/api/", { method: "POST", body: fd })
            .then(e => e.json())
            .catch(e => {
            console.log({ "error": e.message });
            if (e.message == "NetworkError when attempting to fetch resource.") {
                error("Network Disconnected");
            }
            else if (e.message == "JSON.parse: unexpected character at line 1 column 1 of the JSON data") {
                error("Could Not Handle Request");
            }
        })
            .then(e => {
            if (e["code"] != 200) {
                error(e["msg"]);
            }
            if (e["rethrow"] == "") {
                post(arr, true);
            }
            else
                return e;
        });
    }
}
async function heartbeat() {
    var e = await post({ "ping": "" });
    if (e.message == "NetworkError when attempting to fetch resource.") {
        error("Network Disconnected");
    }
    else
        error(false);
}
function error(msg) {
    if (typeof msg === "string") {
        added_at = Date.now();
        nu("error").style.display = "block";
        nu("error").innerText = msg;
    }
    else {
        if (Date.now() > (added_at + 5000)) {
            nu("error").style.display = "none";
            nu("error").innerText = "";
        }
    }
}
