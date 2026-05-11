import queue
import threading
import time
import heapq


class TaskQueue:
    def __init__(self, concurrency=3):
        self.q = queue.Queue()
        self.delayed = []

        # worker threads
        for _ in range(concurrency):
            threading.Thread(target=self._worker, daemon=True).start()

        # scheduler thread
        threading.Thread(target=self._scheduler, daemon=True).start()

    def enqueue(self, handler, payload, delay_ms=0):
        print(f"[{time.strftime('%H:%M:%S')}] Task enqueued")

        if delay_ms > 0:
            run_at = time.time() + delay_ms / 1000
            heapq.heappush(self.delayed, (run_at, handler, payload))
        else:
            self.q.put((handler, payload))

    def _worker(self):
        while True:
            handler, payload = self.q.get()
            print(f"[{time.strftime('%H:%M:%S')}] Task started")

            try:
                handler(payload)
                print(f"[{time.strftime('%H:%M:%S')}] Task finished")
            except Exception as e:
                print(f"[{time.strftime('%H:%M:%S')}] Task failed: {e}")

    def _scheduler(self):
        while True:
            now = time.time()

            if self.delayed and self.delayed[0][0] <= now:
                _, handler, payload = heapq.heappop(self.delayed)
                self.q.put((handler, payload))
            else:
                time.sleep(0.1)