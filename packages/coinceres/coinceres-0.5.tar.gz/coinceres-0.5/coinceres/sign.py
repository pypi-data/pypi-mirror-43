# -*- coding: utf-8 -*-
import hashlib
import copy


class SignMixin(object):
    secret_key = None

    @classmethod
    def join_list(cls, payload: list) -> str:
        return "&".join(payload)

    @classmethod
    def sorted_dict(cls, payload: dict) -> list:
        return sorted(["{}={}".format(key, value) for key, value in payload.items()])

    def sign(self, data: dict = None) -> str:
        payload = copy.deepcopy(data)
        if data is None:
            payload = dict()
        pre_sign_list = self.sorted_dict(payload)
        pre_sign_list.append("secret={}".format(self.secret_key))
        pre_sign = self.join_list(pre_sign_list)
        return hashlib.sha256(pre_sign.encode("utf8")).hexdigest()
