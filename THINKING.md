# Thinking Log

<!-- This is your scratchpad. Fill it in AS YOU GO, not at the end.
     Rough, fragmentary, honest. Don't polish it.
     Read the README for guidance on how to use this file. -->

## Initial Reaction

- What's your gut take on the problem?

This looks like building a small in-memory job scheduler.
Components I’m thinking about:
- job queue
- timers
- concurrent execution
- delays
- failure handling

- What feels like the hard part?
Retry with delay + shutdown interaction feels tricky, not sure how to handle it

Also:
- “delayed tasks shouldn’t take a concurrency slot”. 
  Looks like can't just sleep inside a worker thread

- What approaches do you see? Which would you rule out and why?
Thinking about using semaphores since I’ve used them before for job scheduling

Not sure yet:
- worker pool vs threads + semaphore
- how to handle delayed tasks (maybe separate scheduler?)


- Anything you're already unsure about?
 - how to handle delayed tasks without blocking threads
 - how retry + delay connect
 - what happens during shutdown with delayed/retry tasks

Also:
- in real life tools like Airflow / Control-M exist for this and it is much easier to use those to create something of this kind.

## Plan

- How will you structure this?

Thinking:
     - Task object - handler, payload, retries, backoff, attempt count, next_run_time
     - ready queue - tasks ready to run
     - delayed queue - priority queue (heap) based on next_run_time


- What are the key design decisions you're making up front?
     - use multiple worker threads to control concurrency (instead of semaphore for now)
     - use threads for execution (simpler than asyncio)
     - delayed tasks should NOT block worker threads → need separate scheduling


- What are you deliberately deferring?
     - supporting async handlers (will assume sync for now can look into async later)
     - optimizing scheduler (simple polling loop is fine)


- What will you build FIRST — the smallest slice that proves something useful?
     1. basic enqueue + run task (no concurrency limit)
     2. add concurrency with semaphore
     3. add delayed tasks (heap + scheduler loop)
     4. add retry with backoff (reuse delayed mechanism)
     5. dead letter queue
     6. shutdown handling

## Progress Notes

<!-- Drop an entry any time you:
     - change direction from your plan
     - hit something unexpected
     - make a trade-off
     - realise you were wrong about something
     - finish a chunk and start the next

     One or two sentences each is fine. Timestamp each one.
     Imagine your pair partner just asked "what are you doing?" — answer that.
     Add as many entries as you need. -->

###05/01 - [15:10]
Started with very basic version where enqueue directly executed task. Realized that’s not actually a queue.

###05/01 - [15:20]
Switched to using queue.Queue + worker thread so tasks are actually queued and processed asynchronously.

###05/01-  [15:35]
Added concurrency by starting multiple worker threads instead of one. This naturally limits number of tasks running at the same time.

###05/01 - [15:40]
Originally thought of using semaphore for concurrency, but worker threads felt simpler to implement for now.

###05/01 - [15:45]
Not sure yet how delayed tasks will fit into this since workers block on queue.get(). Might need separate scheduler.

## Research / References

<!-- Optional. Any docs, articles, past code, or language references you looked at.
     A one-line note on what you took from each is enough. -->

## Retrospective

<!-- After you're done. This section is NOT optional — it's one of the most
     valuable parts of the submission. Be honest.

     - What's the weakest part of your solution? Where's the duct tape?
     - Where would this break in production?
     - What would you do differently with more time?
     - What surprised you about this problem?
     - Anything you tried and threw away? Why? -->
