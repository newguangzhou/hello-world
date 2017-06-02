# -*- coding: utf-8 -*-
import json
import urllib
import logging
import datetime
import traceback
from lib import error_codes
import pymongo
from tornado.web import asynchronous
from tornado import gen
from helper_handler import HelperHandler

from lib import utils
from lib import sys_config
from lib.sys_config import SysConfig


class AddDeviceInfo(HelperHandler):
    @gen.coroutine
    def _deal_request(self):
        logging.debug("AddDeviceInfo, %s", self.dump_req())

        self.set_header("Content-Type", "application/json; charset=utf-8")
        device_dao = self.settings["device_dao"]
        pet_dao = self.settings["pet_dao"]
        conf = self.settings["appconfig"]
        res = {"status": error_codes.EC_SUCCESS}

        uid = None
        token = None
        imei = None
        device_name = None
        try:
            uid = int(self.get_argument("uid"))
            token = self.get_argument("token")
            #st = yield self.check_token("OnAddDeviceInfo", res, uid, token)
            #if not st:
            #    return

            imei = self.get_argument("imei")
            device_name = self.get_argument("device_name")
        except Exception, e:
            logging.warning("AddDeviceInfo, invalid args, %s %s",
                            self.dump_req(), str(e))
            res["status"] = error_codes.EC_INVALID_ARGS
            self.res_and_fini(res)
            return

        # try:
        #     bind_res = yield pet_dao.bind_device(uid, imei)
        # except pymongo.errors.DuplicateKeyError, e:
        #     user_dao = self.settings["user_dao"]
        #     res["status"] = error_codes.EC_EXIST
        #     try:
        #         info = yield user_dao.get_user_info(uid, ("phone_num"))
        #         res["old_account"] = info["phone_num"]
        #     except Exception,ee:
        #         logging.warning("AddDeviceInfo, error, imei has exit but can't get the old account: %s %s", self.dump_req(),
        #                         self.dump_exp(ee))
        #         res["old_account"] = ""
        #     self.res_and_fini(res)
        #     return


        info = {}
        if imei is not None:
            info["imei"] = imei
        if device_name is not None:
            info["device_name"] = device_name
        info["sim_deadline"] = datetime.datetime.now() + datetime.timedelta(days=180)
        info["uid"] = uid;
        try:
            yield device_dao.update_device_info(**info)
        except pymongo.errors.DuplicateKeyError, e:
            user_dao = self.settings["user_dao"]
            res["status"] = error_codes.EC_EXIST
            try:
                info = yield user_dao.get_user_info(uid, ("phone_num"))
                res["old_account"] = info["phone_num"]
            except Exception, ee:
                logging.warning("AddDeviceInfo, error, imei has exit but can't get the old account: %s %s",
                                self.dump_req(),
                                self.dump_exp(ee))
                res["old_account"] = ""
            self.res_and_fini(res)
            return
        except Exception, e:
            logging.warning("AddDeviceInfo, error, %s %s", self.dump_req(),
                            self.dump_exp(e))
            res["status"] = error_codes.EC_SYS_ERROR
            self.res_and_fini(res)
            return

# 成功
        logging.debug("AddDeviceInfo, success %s", self.dump_req())
        self.res_and_fini(res)

    def post(self):
        return self._deal_request()

    def get(self):
        return self._deal_request()
