# Thinking Log

## Initial Reaction

- What's your gut take on the problem?

This looks like building a small in-memory job scheduler.

Thinking it needs:
- some kind of queue
- timers for delayed tasks
- multiple workers for concurrency
- retry / failure handling


- What feels like the hard part?

Retry + delay + shutdown all interacting feels messy.

Also this part:
“delayed tasks shouldn’t take a concurrency slot”

So I can’t just do time.sleep inside a worker, that would block a slot.


- What approaches do you see? Which would you rule out and why?

First thought was semaphores since I’ve used them before.

But not sure yet:
- worker pool vs threads + semaphore
- how to handle delayed tasks cleanly


- Anything you're already unsure about?

- how to schedule delayed tasks without blocking threads
- retry probably connects to delay somehow?
- what happens to delayed/retry tasks during shutdown

Also in real life I’d just use something like Airflow or Control-M, but here it’s more about understanding the mechanics.


---

## Plan

- How will you structure this?

Thinking:
- task object with handler, payload, retries, backoff, attempt count
- normal queue for ready tasks
- heap for delayed tasks (sorted by run time)


- Key decisions for now

- use multiple worker threads for concurrency (simpler than semaphores for now)
- stick to threads instead of asyncio
- delayed tasks handled separately so they don’t block workers


- What I’m deferring

- async handler support (will assume sync for now)
- optimizing scheduler (polling loop should be fine)


- Build order

1. basic enqueue + run
2. add concurrency with worker threads
3. add delayed tasks (heap + scheduler)
4. add retry (reuse delay logic)
5. dead letter queue
6. shutdown



## Progress Notes

### [04/14 13:00]
Looked through the task. Feels like a mini job scheduler.

### [04/28 10:30 am]
Sketched out rough plan.

### [05/01 10:15]
Started coding in VS Code.

### [05/01 11:00]
Initially just ran task directly inside enqueue. Realized that’s not really a queue.

### [05/01 12:00]
Switched to queue.Queue + worker thread. Now tasks actually queue up.

### [05/01 13:00]
Added multiple worker threads. This handles concurrency naturally.
Was thinking about semaphores but threads felt simpler.

### [05/01 14:00]
Not sure yet how delayed tasks will fit in since workers block on queue.get(). Need to try something, got another idea.
Definitely taking more time than expected.

### [05/08 09:15]
Started working on delayed execution. The code is at least running without errors.

### [05/08 10:00 AM]
Using heap to store delayed tasks with run time.

### [05/08 11:00 AM]
Added scheduler thread to move tasks from heap to main queue.

### [05/08 11:30 am]
Originally thought of just sleeping inside worker, but that blocks concurrency. This is not working as expected not good.

### [05/08 12:30 PM]
Delay logic is finally working now.

### [05/08 1:00 PM]
Confirmed delayed tasks run at correct time and don’t block workers.

### [05/10 09:30 AM]
Started retry logic. udpated the code file. Committed changes to main.

### [05/10 10:15 AM]
Realized retry is basically delayed execution again.
Reused delayed queue for retries instead of building separate system. Much simpler.

### [05/11 9:30 am]
Added dead letter queue to capture tasks that failed after all retries.
Stored handler name, payload, error, and attempt count for easier debugging.

### [05/11 1:55 PM]
Added graceful shutdown. Used flag to stop accepting new tasks and tracked active tasks.

### [05/11 2:04 PM]
Shutdown waits until currently running tasks finish before completing.

### [05/28 10:00 AM]
Checked the code against the feedback that flaky_task was not reaching success state. Investigated and found inconsistency in retry state handling.

### [05/31 1:30 PM]
Fixed by aligning retry logic so that queue owns attempt tracking instead of mixing handler and queue state.

### [05/31 3:00 PM]
Updated THINKING.md based on feedback and debugging process.

## Assumptions:
- supporting only synchronous handlers for now (did not implement async handling for now)
- in-memory only, no persistence (tasks lost on restart)
- simple polling scheduler is acceptable for this exercise
- using threads instead of more complex concurrency models


## Retrospective

- Weakest part

Scheduler uses sleep loop. Not very efficient. Also no locking around delayed queue → could have race conditions. Not sure how to handle this better!


- Where this breaks

Under heavy load or real concurrency, heap + queue might not be fully safe. Also everything is in-memory, so crash = lost tasks.


- What I’d do differently

Would separate scheduler more cleanly and maybe use condition variables instead of polling. Also track task states more explicitly. To be honest we should use some scheduling tools like Airflow, Control-M which can better handle such tasks.


- What surprised me

Retry became way simpler once I reused the delay mechanism instead of overthinking it.


- What I tried and dropped

Tried sleeping inside worker for delay — quickly realized it blocks concurrency so moved to scheduler + heap approach.
