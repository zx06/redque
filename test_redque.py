"""第一次写测试代码。养成一个好习惯，从现在开始吧
"""
import random
import time
import unittest
import uuid

import redis

from redque import EmptyError, LockError, RedisQueue


class TestRedisQueue(unittest.TestCase):
    """由于使用的是json进行序列化，所以测试了所有json数据类型
    """

    def setUp(self):
        """设置"""
        self.red = redis.Redis()
        self.key_rand = str(uuid.uuid1())
        self.keys = []

    def del_key(self, key):
        """删除key"""
        self.red.delete(key)

    def test_qsize(self):
        """测试qsize()"""
        queue_qsize = RedisQueue("queue_qsize_" + self.key_rand)
        self.keys.append(queue_qsize.key)
        self.del_key(queue_qsize.key)
        num = random.randint(1, 10)
        for i in range(num):
            queue_qsize.put(i)
        self.assertEqual(queue_qsize.qsize(), num)

    def test_empty(self):
        """测试empty()"""
        queue_empty = RedisQueue("queue_empty_" + self.key_rand)
        self.keys.append(queue_empty.key)
        self.del_key(queue_empty.key)
        self.assertTrue(queue_empty.empty())
        queue_empty.put("empty")
        self.assertFalse(queue_empty.empty())

    def test_put(self):
        """测试put()"""
        queue_put = RedisQueue("queue_put_" + self.key_rand)
        self.keys.append(queue_put.key)
        items = [x for x in range(random.randint(1, 10))]
        for i in items:
            qsize = queue_put.put(i)
            self.assertEqual(queue_put.qsize(), qsize)
        for i in items:
            item = queue_put.get()
            self.assertEqual(item, i)

    def test_lock(self):
        """测试加锁"""
        queue_lock = RedisQueue("queue_lock_" + self.key_rand)
        self.keys.append(queue_lock.key)
        # 加锁 无锁时加锁
        self.assertTrue(queue_lock.lock(5))
        # 加锁 有锁时加锁
        self.assertFalse(queue_lock.lock())
        # 加锁 超时后加锁
        time.sleep(6)
        self.assertTrue(queue_lock.lock())
        # 加锁 解锁后加锁
        queue_lock.unlock()
        self.assertTrue(queue_lock.lock())



    def test_get_nowait_when_empty(self):
        """测试异常"""
        queue_err = RedisQueue("queue_err_" + self.key_rand)
        self.del_key(queue_err.key)
        with self.assertRaises(EmptyError):
            queue_err.get_nowait()

    def tearDown(self):
        """清理"""
        for key in self.keys:
            self.del_key(key)


if __name__ == '__main__':
    unittest.main(verbosity=1)
