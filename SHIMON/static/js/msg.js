async function send(e) {
    if (e.key != "Enter" || !e.target.value)
        return;
    await post({ "send msg": {
            "uname": document.cookie.replace(/(?:(?:^|.*;\s*)uname\s*\=\s*([^;]*).*$)|^.*$/, "$1"),
            "msg": e.target.value
        } }).then(e => {
        if (e.code != 400) {
            reload_msgs();
        }
    });
    e.target.value = "";
}
