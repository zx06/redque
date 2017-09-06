from redque import RedisQueue
import threading
import time


class PutThread(threading.Thread):
    def __init__(self, flag, *args, **kwargs):
        threading.Thread.__init__(self, *args, **kwargs)
        self.q = RedisQueue('test')
        self.flag = flag

    def run(self):
        if self.q.lock(30):
            for i in range(10):
                time.sleep(0.001)
                self.q.put(self.flag + '_' + str(i))
            self.q.unlock()
        else:
            print('locked')


if __name__ == '__main__':
    for i in range(50):
        t = PutThread(daemon=True, flag=str(i))
        t.start()
        time.sleep(0.01)

    q = RedisQueue('test')
    time.sleep(5)
    while not q.empty():
        print(q.get())
