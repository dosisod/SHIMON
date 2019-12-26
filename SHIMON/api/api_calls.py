from .external import api_recent, api_friends, api_allfor
from .error import error, error_200, error_202, error_400
from .unlock import unlock
from .send_msg import send_msg
from .delete_msg import delete_msg
from .save import save
from .lock import lock
from .change_pwd import change_pwd
from .new_key import new_key
from .msg_policy import msg_policy
from .expiration_timer import expiration_timer
from .theme import theme
from .devmode import devmode
from .nuke import nuke
from .fresh_js import fresh_js
from .fresh_css import fresh_css
from .status import status
from .ping import ping
from ._data import _data
from .add_friend import add_friend

calls={

"send msg": send_msg,
"delete msg": delete_msg,
"save": save,
"lock": lock,
"change pwd": change_pwd,
"new key": new_key,
"msg policy": msg_policy,
"expiration timer": expiration_timer,
"theme": theme,
"devmode": devmode,
"nuke": nuke,
"fresh js": fresh_js,
"fresh css": fresh_css,
"status": status,
"ping": ping,
"data": _data,
"add friend": add_friend

}
