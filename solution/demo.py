import time
from task_queue import TaskQueue


def sample_task(payload):
    print(f"[{time.strftime('%H:%M:%S')}] Processing {payload}")
    time.sleep(1)


# FIX: handler controls success
def flaky_task(payload):
    if payload["attempt"] < 2:
        payload["attempt"] += 1
        raise Exception("fail")
    print(f"[{time.strftime('%H:%M:%S')}] success")


def always_fail(payload):
    raise Exception("always fails")


def slow_task(payload):
    print(f"[{time.strftime('%H:%M:%S')}] Running slow task")
    time.sleep(2)


queue = TaskQueue(concurrency=2)

# 1. concurrency test
for i in range(5):
    queue.enqueue(sample_task, f"Task-{i}")

# 2. delayed task
queue.enqueue(sample_task, "Delayed-Task", delay_ms=3000)

# 3. retry test (IMPORTANT: dict payload)
queue.enqueue(flaky_task, {"attempt": 0}, max_retries=3, backoff_ms=1000)

# 4. dead letter test
queue.enqueue(always_fail, "bad-task", max_retries=2, backoff_ms=500)

# 5. shutdown test
queue.enqueue(slow_task, "slow")

time.sleep(7)  # enough time for retries to complete

queue.shutdown()

print("\nDead Letters:")
for d in queue.get_dead_letters():
    print(d)