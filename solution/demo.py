import time
from task_queue import TaskQueue


def sample_task(payload):
    print(f"[{time.strftime('%H:%M:%S')}] Processing {payload}")
    time.sleep(1)


def flaky_task(payload):
    raise Exception("fail")


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

# 3. retry test
queue.enqueue(flaky_task, "retry-task", max_retries=3, backoff_ms=1000)

# 4. dead letter test
queue.enqueue(always_fail, "bad-task", max_retries=2, backoff_ms=500)

# 5. shutdown test
queue.enqueue(slow_task, "slow")

time.sleep(8)

queue.shutdown()

print("\nDead Letters:")
for d in queue.get_dead_letters():
    print(d)