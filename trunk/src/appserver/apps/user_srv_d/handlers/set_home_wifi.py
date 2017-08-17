# -*- coding: utf-8 -*-
import json
import urllib
import logging
import datetime
import traceback
from lib import error_codes

from tornado.web import asynchronous
from tornado import gen
from helper_handler import HelperHandler

from lib import utils
from lib import sys_config
from lib.sys_config import SysConfig


class SetHomeWifi(HelperHandler):
    @gen.coroutine
    def _deal_request(self):
        logging.debug("SetHomeWifi, %s", self.dump_req())

        self.set_header("Content-Type", "application/json; charset=utf-8")
        user_dao = self.settings["user_dao"]
        pet_dao = self.settings["pet_dao"]
        terminal_rpc = self.settings["terminal_rpc"]
        conf = self.settings["appconfig"]
        res = {"status": error_codes.EC_SUCCESS}

        uid = None
        wifi_ssid = None
        wifi_bssid = None
        # wifi_power = None
        try:
            uid = int(self.get_argument("uid"))
            token = self.get_argument("token")
            st = yield self.check_token("SetHomeWifi", res, uid, token)
            if not st:
               return
            wifi_ssid = self.get_argument("wifi_ssid")
            wifi_bssid = self.get_argument("wifi_bssid")
            # wifi_power = self.get_argument("wifi_power")
        except Exception, e:
            logging.warning("SetHomeWifi, invalid args, %s %s",
                            self.dump_req(), str(e))
            res["status"] = error_codes.EC_INVALID_ARGS
            self.res_and_fini(res)
            return

        try:

            #info = yield pet_dao.get_user_pets(uid, ("pet_id", ))
            #if info is None:
            #    logging.warning("SetHomeWifi, not found, %s", self.dump_req())
            #    res["status"] = error_codes.EC_PET_NOT_EXIST
            #    self.res_and_fini(res)
            #    return

            set_res = yield pet_dao.set_home_wifi(uid, {"wifi_ssid": wifi_ssid,
                                                        "wifi_bssid":
                                                        wifi_bssid})
            if set_res.matched_count <= 0:
                logging.warning("SetHomeWifi, set fail, %s", self.dump_req())
                res["status"] = error_codes.EC_SYS_ERROR
                self.res_and_fini(res)
        except Exception, e:
            logging.warning("SetHomeWifi, error, %s %s", self.dump_req(),
                            self.dump_exp(e))
            res["status"] = error_codes.EC_SYS_ERROR
            self.res_and_fini(res)
            return

# 成功
        logging.debug("SetHomeWifi, success %s", self.dump_req())
        self.res_and_fini(res)



    @gen.coroutine
    def _deal_request_post(self):
        logging.debug("SetHomeWifi, %s", self.dump_req())

        self.set_header("Content-Type", "application/json; charset=utf-8")
        user_dao = self.settings["user_dao"]
        pet_dao = self.settings["pet_dao"]
        terminal_rpc = self.settings["terminal_rpc"]
        conf = self.settings["appconfig"]
        res = {"status": error_codes.EC_SUCCESS}

        uid = None
        wifi_ssid = None
        wifi_bssid = None
        arround_wifilist=None
        # wifi_power = None
        try:
            uid = int(self.get_argument("uid"))
            token = self.get_argument("token")
            pet_id=self.get_argument("pet_id")
            st = yield self.check_token("SetHomeWifi", res, uid, token)
            if not st:
               return
            wifi_ssid = self.get_argument("wifi_ssid")
            wifi_bssid = self.get_argument("wifi_bssid")
            home_wifi={"wifi_ssid":wifi_ssid,"wifi_bssid":wifi_bssid}
            # logging.error("arround_wifi",self.request.body)
            arround_wifilist=json.loads(self.request.body)
            new_common_wifi = utils.get_new_common_wifi_from_client(
                None, arround_wifilist, home_wifi)
            yield pet_dao.add_common_wifi_info(long(pet_id),
                                                    new_common_wifi)
            # wifi_power = self.get_argument("wifi_power")
        except Exception, e:
            logging.warning("SetHomeWifi, invalid args, %s %s",
                            self.dump_req(), str(e))
            res["status"] = error_codes.EC_INVALID_ARGS
            self.res_and_fini(res)
            return

        try:

            #info = yield pet_dao.get_user_pets(uid, ("pet_id", ))
            #if info is None:
            #    logging.warning("SetHomeWifi, not found, %s", self.dump_req())
            #    res["status"] = error_codes.EC_PET_NOT_EXIST
            #    self.res_and_fini(res)
            #    return

            set_res = yield pet_dao.set_home_wifi(uid, {"wifi_ssid": wifi_ssid,
                                                        "wifi_bssid":
                                                        wifi_bssid})
            if set_res.matched_count <= 0:
                logging.warning("SetHomeWifi, set fail, %s", self.dump_req())
                res["status"] = error_codes.EC_SYS_ERROR
                self.res_and_fini(res)
        except Exception, e:
            logging.warning("SetHomeWifi, error, %s %s", self.dump_req(),
                            self.dump_exp(e))
            res["status"] = error_codes.EC_SYS_ERROR
            self.res_and_fini(res)
            return

# 成功
        logging.debug("SetHomeWifi, success %s", self.dump_req())
        self.res_and_fini(res)

    def post(self):
        return self._deal_request_post()

    def get(self):
        return self._deal_request()