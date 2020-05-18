from flask import Response
from pathlib import Path
import base64 as b64
import gnupg as gpg  # type: ignore
import json

from SHIMON.api.error import error, error_401
from SHIMON.renderer import render
from SHIMON.kee import Kee

from typing import Union, Optional, cast, TYPE_CHECKING
from typing_extensions import Literal
from SHIMON import HttpResponse

if TYPE_CHECKING:
    from SHIMON.shimon import Shimon

gpg.logger.setLevel(gpg.logging.ERROR)


class Storage:
    def __init__(self, shimon_ref: "Shimon", filepath: str = "data.gpg") -> None:
        self.shimon = shimon_ref

        self.filepath = filepath
        self._gpg = gpg.GPG()

    def unlock(self, pwd: str) -> Optional[str]:
        data = self.raw_unlock(self.filepath, pwd)

        if data == None:
            return "{}"

        elif data == "":
            return None

        return data

    def raw_unlock(self, filepath: str, pwd: str) -> Optional[str]:
        if self.cache_file_exists(filepath):
            with open(filepath, "rb") as f:
                return cast(
                    str, self._gpg.decrypt_file(f, passphrase=pwd).data.decode()
                )

        return None

    def cache_file_exists(self, filepath: str = "") -> bool:
        return Path(filepath if filepath else self.filepath).is_file()

    def lock(self, pwd: str) -> Optional[HttpResponse]:
        error_status = self.attempt_lock(pwd)

        if error_status == "fail":
            return error(
                401,
                render(
                    self.shimon,
                    "pages/account.jinja",
                    error="Cache could not be locked",
                    version=self.shimon.VERSION,
                ),
                True,
                False,
            )

        elif not error_status:
            return None

        return error_status

    def save(self, pwd: str) -> Optional[HttpResponse]:
        error_status = self.attempt_lock(pwd)

        if error_status == "fail":
            return error_401()

        elif not error_status:
            return None

        return error_status

    def attempt_lock(self, pwd: str) -> Union[HttpResponse, Literal["fail"], None]:
        if not self.shimon.cache or self.shimon.cache.is_empty():
            return error(
                400,
                render(self.shimon, "pages/login.jinja", msg="Please re-open cache"),
                False,
                True,
            )

        if self.shimon.cache["sha512"]:
            if self.shimon.security.correct_pwd(pwd):
                self.raw_lock(
                    self.filepath, json.dumps(self.shimon.cache.export()), pwd
                )

                return None

        return "fail"

    def raw_lock(self, filepath: str, data: str, pwd: str) -> None:
        self._gpg.encrypt(
            data, recipients=None, passphrase=pwd, symmetric=True, output=filepath
        )

        # ensure only the current user can access the file
        Path(filepath).chmod(0o600)

    def resetCache(self) -> None:
        # fill cache with default values
        self.shimon.cache.load(
            {
                "history": [],
                # hash for "123", can be changed in settings
                "sha512": "3c9909afec25354d551dae21590bb26e38d53f2173b8d3dc3eee4c047e7ab1c1eb8b85103e3be7ba613b31bb5c9c36214dc9f14a42fd7a2fdb84856bca5c44c2",
                "key": b64.b64encode(Kee(2048).private()).decode(),
                "expiration": 3600,
                "developer": False,
                "version": self.shimon.VERSION,
                "theme": "auto",
            }
        )

        # save default cache right away
        self.shimon.storage.lock("123")
