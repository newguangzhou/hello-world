# -*- coding: utf-8 -*-

from tornado import gen

from auth_mongo_dao import AuthMongoDAO

class AuthDAO:
    @staticmethod
    def new(*args, **kwargs):
        mongo_dao = AuthMongoDAO(*args, **kwargs)
        inst = AuthDAO(db_dao = mongo_dao)
        return inst
    
    def __init__(self, **kwargs):
        self._db_dao = kwargs["db_dao"]
   
    def __getattr__(self, attr):
        return getattr(self._db_dao, attr)
 
