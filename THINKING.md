# Thinking Log

<!-- This is your scratchpad. Fill it in AS YOU GO, not at the end.
     Rough, fragmentary, honest. Don't polish it.
     Read the README for guidance on how to use this file. -->

## Initial Reaction

## Initial Reaction

- What's your gut take on the problem?

This looks like building a small in-memory job scheduler
Components I’m thinking about:
- job queue
- timers
- concurrent execution
- delays
- failure handling

- What feels like the hard part?
Retry with delay + shutdown interaction feels tricky, not sure how to handle it

Also:
- “delayed tasks shouldn’t take a concurrency slot”
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

<!-- Still before coding (or right at the start).
     - How will you structure this? Files, types, main components.
     - What are the key design decisions you're making up front?
     - What are you deliberately deferring?
     - What will you build FIRST — the smallest slice that proves something useful? -->

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

### [HH:MM]

### [HH:MM]

### [HH:MM]

### [HH:MM]

### [HH:MM]

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
