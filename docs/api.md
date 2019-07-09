# API Integration

This is a list of api commands, their functions, and how to call them

| Name | Args | Return | Description |
| "unlock" | PWD (string) | Home screen if success, login page with error msg if error | Tries to unlock cache with PWD as password |
| "save" | PWD (string) | Error if invalid, OK if success | Saves current state of SHIMON to cache |
| "lock" | PWD (string) | Error if invalid, OK if success | Saves then deletes the session |
| "send msg" | UNAME (string), MSG (string) | Error if invalid, OK if success | Send a message MSG to user UNAME |
| "change pwd" | OLD (string), NEW (string) | Error if invalid, OK if success | If OLD password is correct, update to NEW string |
| "new key" | PWD (string) | Error if invalid, `index.html` if success | If password PWD is correct, update internal RSA key |
| "expiration timer" | SECONDS (int) | Error if SECONDS is not in range, OK if success | Update how long to wait until session expires |
| "nuke" | PWD (string) |  | Deletes cache if PWD is correct |
| "status" | | Status of app | Gets version and unlock state |
| "ping" | | pong | ping pong |
| "msg" | UNAME (string) | Redirect | Goes to page for user UNAME |