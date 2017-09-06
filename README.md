# redque
![travis-ci](https://api.travis-ci.org/noob-xu/redque.svg?branch=master)

基于redis的分布式队列
- 基础使用
```python
import redque
q = redque.RedisQueue("que")
q.put(1)
q.get()
```

- 锁(多进程或者分布式场景)
*不是真正意义上的锁，只是提供一个标记*
```python
import redque
q = redque.RedisQueue("que")
# put之前检查是否有锁，加锁成功返回True(原本没有锁),
# 失败返回False(该队列已经被加锁)
if q.lock(timeout=30):
    for i in range(100)
        q.put(i)
    q.unlock() # put结束后删除锁
```
