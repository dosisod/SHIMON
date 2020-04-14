from SHIMON.api.external import api_recent, api_friends, api_allfor
from SHIMON.api.error import error, error_200, error_202, error_400
from SHIMON.api.unlock import ApiUnlock
from SHIMON.api.send_msg import ApiSendMsg
from SHIMON.api.delete_msg import ApiDeleteMsg
from SHIMON.api.save import ApiSave
from SHIMON.api.lock import ApiLock
from SHIMON.api.change_pwd import ApiChangePwd
from SHIMON.api.new_key import ApiNewKey
from SHIMON.api.msg_policy import ApiMsgPolicy
from SHIMON.api.expiration_timer import ApiExpirationTimer
from SHIMON.api.theme import ApiTheme
from SHIMON.api.devmode import ApiDevmode
from SHIMON.api.nuke import ApiNuke
from SHIMON.api.fresh_js import ApiFreshJs
from SHIMON.api.fresh_css import ApiFreshCss
from SHIMON.api.status import ApiStatus
from SHIMON.api.ping import ApiPing
from SHIMON.api.friends import ApiFriends
from SHIMON.api.recent import ApiRecent
from SHIMON.api.allfor import ApiAllfor
from SHIMON.api.add_friend import ApiAddFriend
from SHIMON.api.api_base import ApiBase

from typing import Dict, Any, Optional
from SHIMON.__init__ import HttpResponse

apicalls=[
	ApiSendMsg(),
	ApiDeleteMsg(),
	ApiSave(),
	ApiLock(),
	ApiChangePwd(),
	ApiNewKey(),
	ApiMsgPolicy(),
	ApiExpirationTimer(),
	ApiTheme(),
	ApiDevmode(),
	ApiNuke(),
	ApiFreshJs(),
	ApiFreshCss(),
	ApiStatus(),
	ApiPing(),
	ApiFriends(),
	ApiRecent(),
	ApiAllfor(),
	ApiAddFriend()
]
