# redque
基于redis的分布式队列
- 基础使用
```python
import redque
q = redque.RedisQueue("que")
q.put(1)
q.get()
```
- 加锁
```python
import redque
q = redque.RedisQueue("que")
q.lock()
q.put(1) # 会抛出异常
q.locked() # True
q.unlock()
q.locked() # False
q.put(1) # 正常加入队列
```
