from SHIMON.api.external import api_recent, api_friends, api_allfor
from SHIMON.api.error import error, error_200, error_202, error_400
from SHIMON.api.unlock import unlock
from SHIMON.api.send_msg import send_msg
from SHIMON.api.delete_msg import delete_msg
from SHIMON.api.save import save
from SHIMON.api.lock import lock
from SHIMON.api.change_pwd import change_pwd
from SHIMON.api.new_key import new_key
from SHIMON.api.msg_policy import msg_policy
from SHIMON.api.expiration_timer import expiration_timer
from SHIMON.api.theme import theme
from SHIMON.api.devmode import devmode
from SHIMON.api.nuke import nuke
from SHIMON.api.fresh_js import fresh_js
from SHIMON.api.fresh_css import fresh_css
from SHIMON.api.status import status
from SHIMON.api.ping import ping
from SHIMON.api.friends import friends
from SHIMON.api.recent import recent
from SHIMON.api.allfor import allfor
from SHIMON.api.add_friend import add_friend

from typing import Callable, Dict, Any
from SHIMON.__init__ import HttpResponse

call_type=Dict[
	str,
	Callable[
		[Any, Any, bool],
		HttpResponse
	]
]

calls: call_type={

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
"friends": friends,
"recent": recent,
"allfor": allfor,
"add friend": add_friend

}
