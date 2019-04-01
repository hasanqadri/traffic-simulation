
from collections import deque
import time

import threading
from threading import Lock


def run_job(runtime, callback=None):
    """
    Simulate running the job for runtime, call the callback function
    after completion.
    """
    time.sleep(runtime)
    if callback:
        callback()


class Resource():
    def __init__(self, count):
        self.job_pool           = deque()
        self.pool_lock          = Lock()

        self.available_workers  = count
        self.worker_lock        = Lock()


    def dispatch(self, runtime):
        print("Dispatching sleep for {}s".format(runtime))
        t = threading.Thread(
            target=run_job,
            args=(runtime,),
            kwargs={"callback": self.finish_job},
        )
        # print("Starting thread: {}".format(t.name))
        t.start()


    def add_job(self, runtime):
        self.worker_lock.acquire()

        dispatched = False  # Indicates if job has been dispatched.
        if self.available_workers > 0:
            self.available_workers -= 1
            self.dispatch(runtime)
            dispatched = True

        self.worker_lock.release()

        if dispatched:
            return

        # Otherwise, add to the job pool
        self.pool_lock.acquire()
        self.job_pool.append(runtime)
        self.pool_lock.release()


    def finish_job(self):
        # If we have job in the pool, just dispatch a new
        # job from the pool immediately.
        dispatched = False
        self.pool_lock.acquire()
        if self.job_pool:
            runtime = self.job_pool.popleft()  # Pop from Queue
            self.dispatch(runtime)
            dispatched = True
        self.pool_lock.release()

        if not dispatched:
            self.worker_lock.acquire()
            self.available_workers += 1
            self.worker_lock.release()


if __name__ == "__main__":
    res = Resource(2)
    res.add_job(4)
    res.add_job(1)
    res.add_job(1)
    res.add_job(4)
    res.add_job(1)
