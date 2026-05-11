import time
from task_queue import TaskQueue

def sample_task(payload):
    print(f"[{time.strftime('%H:%M:%S')}] Processing {payload}")
    time.sleep(1)

queue = TaskQueue(concurrency=2)

# immediate tasks
queue.enqueue(sample_task, "Immediate-1")
queue.enqueue(sample_task, "Immediate-2")

# delayed task
queue.enqueue(sample_task, "Delayed-3", delay_ms=3000)

# keep program alive so threads can run
time.sleep(6)
