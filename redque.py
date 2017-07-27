"""基于redis的队列
原文:http://peter-hoffmann.com/2012/python-simple-queue-redis-queue.html
再原作者的基础上增加使用了json进行序列化,尽量接近官方queue模块
"""
import json
import time

import redis


class RedisQueue(object):

    def __init__(self, name, namespace="redque", **redis_kw):
        self.__db = redis.StrictRedis(**redis_kw)
        self.key = "%s:%s" % (namespace, name)
        self.__lock_key = self.key + "_lock"

    def qsize(self):
        return self.__db.llen(self.key)

    def empty(self):
        return self.qsize() == 0

    def put(self, item):
        if self.locked():
            raise LockError
        json_item = json.dumps(item)
        return self.__db.rpush(self.key, json_item)

    def get(self, block=True, timeout=None):
        if block:
            json_item = self.__db.blpop(self.key, timeout=timeout)
            # blpop返回的是一个(key,value)的tuple,只需要获取value
            if json_item:
                json_item = json_item[1]
        else:
            json_item = self.__db.lpop(self.key)

        item = None
        if json_item:
            item = json.loads(json_item)
        else:
            raise EmptyError
        return item

    def get_nowait(self):
        return self.get(False)

    def lock(self, timeout=30):
        lock_timeout = time.time() + timeout
        self.__db.setnx(self.__lock_key, str(lock_timeout))

    def unlock(self):
        self.__db.delete(self.__lock_key)

    def locked(self):
        _lock = self.__db.get(self.__lock_key)
        if _lock and float(_lock) > time.time():
            return True
        else:
            self.unlock()
            return False


class EmptyError(Exception):
    pass


class LockError(Exception):
    pass
