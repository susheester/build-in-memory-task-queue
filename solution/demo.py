import time
from task_queue import TaskQueue


def sample_task(payload):
    print(f"[{time.strftime('%H:%M:%S')}] Processing {payload}")
    time.sleep(1)


queue = TaskQueue(concurrency=2)

queue.enqueue(sample_task, "Immediate-1")
queue.enqueue(sample_task, "Immediate-2")
queue.enqueue(sample_task, "Delayed-3", delay_ms=3000)

time.sleep(6)