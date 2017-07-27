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

    def test_put_when_locked(self):
        """锁定时插入"""
        queue_put_locked = RedisQueue("queue_put_locked_" + self.key_rand)
        self.keys.append(queue_put_locked.key)
        # 加锁 验证锁状态
        queue_put_locked.lock(10)
        self.assertTrue(queue_put_locked.locked())
        # 验证加锁时插入失败
        with self.assertRaises(LockError):
            queue_put_locked.put("lock")
        # 解锁 验证锁状态
        queue_put_locked.unlock()
        self.assertFalse(queue_put_locked.locked())
        # 解锁后 验证插入
        self.assertEqual(queue_put_locked.put("unlock"), 1)

    def test_lock_timeout(self):
        """验证锁的超时机制"""
        queue_lock_timeout = RedisQueue("queue_lock_timeout_" + self.key_rand)
        self.keys.append(queue_lock_timeout.key)
        self.keys.append(queue_lock_timeout.key + "_lock")
        # 加锁 验证插入失败
        queue_lock_timeout.lock(6)
        with self.assertRaises(LockError):
            queue_lock_timeout.put("lock")
        # 等待超时 验证插入成功
        time.sleep(6)
        self.assertEqual(queue_lock_timeout.put("unlock"), 1)

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
