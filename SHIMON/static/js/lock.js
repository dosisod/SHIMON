function lock(e) {
    e.preventDefault();
    var str = prompt("Re-enter password to lock");
    if (!str)
        return;
    post({ "lock": str }, true);
}
function save(e) {
    e.preventDefault();
    var str = prompt("Re-enter password to save");
    if (!str)
        return;
    post({ "save": str })
        .then(e => {
        if (e["code"] == 200) {
            error("Cache was successfully saved");
        }
    });
}
