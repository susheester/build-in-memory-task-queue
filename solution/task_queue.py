import queue
import threading
import time

class TaskQueue:
    def __init__(self):
        self.q = queue.Queue()

        # start one worker- using queue and worker thread
        threading.Thread(target=self._worker, daemon=True).start()

    def enqueue(self, handler, payload):
        print(f"[{time.strftime('%H:%M:%S')}] Task enqueued")
        self.q.put((handler, payload))

    def _worker(self):
        while True:
            handler, payload = self.q.get()
            print(f"[{time.strftime('%H:%M:%S')}] Task started")
            handler(payload)
            print(f"[{time.strftime('%H:%M:%S')}] Task finished")
