from flask import Flask, request, abort, Response, make_response
from werkzeug.exceptions import HTTPException
from datetime import datetime, timedelta
from pathlib import Path
import traceback
import json

from SHIMON.api.external import api_recent, api_friends, api_allfor
from SHIMON.cache_map import CacheMapper
from SHIMON.api.error import http_codes
from SHIMON.api.entry import api_entry
from SHIMON.login import LoginLimiter
from SHIMON.security import Security
from SHIMON.session import Session
from SHIMON.storage import Storage
from SHIMON.renderer import render
from SHIMON.cache import Cache

from typing import Union
from SHIMON import HttpResponse


class Shimon:
    def __init__(self) -> None:
        self.VERSION = "0.1.1"

        self.login_limiter = LoginLimiter()
        self.session = Session(self)
        self.security = Security(self)
        self.storage = Storage(self)

        self.cache = Cache()

        self.cache.mapper = CacheMapper(
            self,
            {
                "msg policy": "msg_policy",
                "expiration": (self.session, "expires"),
                "developer": "developer",
                "fresh js": "fresh_js",
                "fresh css": "fresh_css",
                "theme": "theme",
                "version": "VERSION",
            },
        )

        # stores whether or not the msg page should redraw
        self.redraw = False

        self.developer = True

        # when this flag is set, the fresh (TS compiled) js is used
        self.fresh_js = False

        # stores whether css should be taken from minified file or "fresh" files
        self.fresh_css = False

        self.theme = "auto"

        # changes which method of deletion to use when deleting msgs
        # 0 confirm before delete (default)
        # 1 require password
        # 2 never ask
        self.msg_policy = 0

    def error(self, ex: Union[int, Exception]) -> HttpResponse:
        return_code = 500

        if isinstance(ex, HTTPException):
            return_code = ex.code or 500

        elif isinstance(ex, int):
            return_code = ex if (300 <= ex <= 417) else 400

        tb = ""
        if isinstance(ex, BaseException) and self.developer:
            tb = traceback.format_exc()

        return (
            render(
                self,
                "pages/error.jinja",
                error=return_code,
                url=request.url,
                traceback=tb,
                msg=http_codes.get(return_code, ""),
            ),
            return_code,
        )

    def index(self, error: str = "", code: int = 200) -> HttpResponse:
        self.security.check_local()

        if not self.storage.cache_file_exists():
            self.storage.resetCache()
            return self.session.create()

        had_error = self.security.check_session()

        if self.cache.is_empty():
            return render(self, "pages/login.jinja"), 401

        elif had_error:
            return render(self, "pages/login.jinja", error="Invalid session"), 401

        res = make_response(
            render(
                self,
                "pages/index.jinja",
                error=error,
                preload=json.dumps(api_recent(self)),
                friends=json.dumps(api_friends(self)),
            )
        )

        res.set_cookie("uname", "", expires=0)

        return res, code

    def settings(self) -> HttpResponse:
        ret = self.security.check_all()
        if ret:
            return ret

        themes = []

        theme_folder = Path("SHIMON/templates/themes/").resolve()
        for theme in theme_folder.iterdir():
            if Path(theme).is_file() and theme.name.endswith(".css"):
                themes.append((theme.name[:-4],) * 2)

        return (
            render(
                self,
                "pages/settings.jinja",
                seconds=self.session.expires,
                msg_policy=self.msg_policy,
                themes=themes,
            ),
            200,
        )

    def account(self) -> HttpResponse:
        ret = self.security.check_all()
        if ret:
            return ret

        return render(self, "pages/account.jinja", version=self.VERSION), 200

    def msg(self, uuid: str) -> HttpResponse:
        ret = self.security.check_all()
        if ret:
            return ret

        for friend in self.cache["history"]:
            if friend["id"] == uuid:
                break
        else:
            abort(404)

        self.redraw = True

        res = make_response(
            render(
                self,
                "pages/msg.jinja",
                preload=json.dumps(api_allfor(self, uuid)),
                friends=json.dumps(api_friends(self)),
            )
        )
        res.set_cookie("uname", uuid)

        self.redraw = True

        return res, 200

    def add(self) -> HttpResponse:
        ret = self.security.check_all()
        if ret:
            return ret

        return render(self, "pages/add.jinja"), 200

    def login(self) -> HttpResponse:
        self.security.check_local()

        if self.cache.is_empty():
            return render(self, "pages/login.jinja"), 200

        else:
            return self.index(error="Already logged in", code=301)

    def api(self) -> HttpResponse:
        self.security.check_local()

        form = request.form.to_dict()

        if form:
            if "json" in form:
                return api_entry(self, json.loads(form["json"]))

            else:
                return api_entry(self, form)

        else:
            return api_entry(self, request.json)
