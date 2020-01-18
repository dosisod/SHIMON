# API Integration

This is a list of api commands, their functions, and how to call them.

Any below text wrapped in `""` is a string variable, else it is an integer value.

| Usage | Return | Description |
| ----- | ------ | ----------- |
| `{"unlock": "PWD"}` | `index.html` if success, login page with error msg if error | Tries to unlock cache with PWD as password |
| `{"save": "PWD"}` | Error if invalid, OK if success | Saves current state of SHIMON to cache |
| `{"lock": "PWD"}` | Error if invalid, OK if success | Saves then deletes the session |
| `{"send msg": {"uname": "UNAME", "msg": "MSG"}}` | Error if invalid, OK if success | Send a message MSG to user UNAME |
| `{"delete msg": {"pwd": "PWD", "id": "ID", "index": INDEX}}` | Delete msg at index INDEX from user ID. PWD required when msg_policy is 2 | |
| `{"change pwd": {"old": "OLD", "new": "NEW"}}` | Error if invalid, OK if success | If OLD password is correct, update to NEW string |
| `{"new key": "PWD"}` | Error if invalid, `index.html` if success | If password PWD is correct, update internal RSA key |
| `{"expiration timer": SECONDS}` | Error if SECONDS is not in range, OK if success | Update how long to wait until session expires |
| `{"msg policy": POLICY}` | Error if POLICY is not in range, OK if success | Changes policy for msg deletion |
| `{"theme": "THEME"}` | Error if THEME is not found, OK if it is | Changes theme to THEME |
| `{"devmode": ""}` | OK | Toggles the state of developermode status |
| `{"nuke": "PWD"}` | Fresh `index.html` | Deletes cache if PWD is correct |
| `{"fresh js": "BOOL"}` | OK | Switches from `bundle.js` to using compiled TS files |
| `{"fresh css": "BOOL"}` | OK | Switches from `bundle.css` to css from ./src/css` |
| `{"status": ""}` | Status of app | Gets version, unlock state, developer state, msg policy |
| `{"ping": ""}` | pong | ping pong |
| `{"add friend": {"name": "NAME", "id": "ID"}}` | Redirect to index with completion status | Add a friend with user id ID and give them name NAME |
| `{"data": "friends"}` | Grabs a list of all friends in the friends list | |
| `{"data":"recent"}` | Grabs the most recent even for each friend in the friends list | |
| `{"data": {"allfor": "UNAME"}}` | Grabs all messages sent to and from user UNAME | |