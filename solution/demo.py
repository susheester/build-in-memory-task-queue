import time
from task_queue import TaskQueue


def sample_task(payload):
    print(f"[{time.strftime('%H:%M:%S')}] Processing {payload}")
    time.sleep(1)


def flaky_task(payload):
    if payload["attempt"] < 2:
        payload["attempt"] += 1
        raise Exception("fail")
    print(f"[{time.strftime('%H:%M:%S')}] success")


def always_fail(payload):
    raise Exception("always fails")


queue = TaskQueue(concurrency=2)

# normal tasks
queue.enqueue(sample_task, "Immediate-1")
queue.enqueue(sample_task, "Immediate-2")

# delayed task
queue.enqueue(sample_task, "Delayed-3", delay_ms=3000)

# retry task
queue.enqueue(flaky_task, {"attempt": 0}, max_retries=3, backoff_ms=1000)

# dead letter test
queue.enqueue(always_fail, "bad-task", max_retries=2, backoff_ms=500)

time.sleep(10)

print("\nDead Letters:")
for d in queue.get_dead_letters():
    print(d)