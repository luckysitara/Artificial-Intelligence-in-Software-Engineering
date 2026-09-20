'use strict';

// Priorities strictly above this value count as "high" (same behavior as the original `priority > 9`).
const MAX_NORMAL_PRIORITY = 9;

// ---------------------------------------------------------------
// Validation: pure, no I/O. Throws before anything is mutated.
// ---------------------------------------------------------------
function validateTask(taskFn, priority) {
  if (typeof taskFn !== 'function') {
    throw new TypeError('Task must be a function.');
  }
  if (priority !== undefined && !Number.isFinite(priority)) {
    throw new TypeError('Priority must be a finite number when provided.');
  }
}

// ---------------------------------------------------------------
// Logging: all console output lives here. The sink is injectable.
// The queue name is always passed in explicitly, so there is no
// ambient `name` lookup and no `this` binding to get wrong.
// ---------------------------------------------------------------
class QueueLogger {
  constructor(sink = console) {
    this.sink = sink;
  }

  starting(queueName) {
    this.sink.log(`Starting queue ${queueName}.`);
  }

  highPriorityAdded(queueName) {
    this.sink.warn(`High priority task added to ${queueName}.`);
  }
}

// ---------------------------------------------------------------
// Storage and state only. addTask adds a task; nothing else.
// ---------------------------------------------------------------
class TaskQueue {
  constructor(name) {
    this.queueName = name;
    this.tasks = [];
    this.isProcessing = false;
  }

  addTask(taskFn, priority, timestamp = Date.now()) {
    const task = { taskFn, priority, timestamp };
    this.tasks.push(task);
    return task;
  }

  startProcessing() {
    this.isProcessing = true;
    // ... logic to process tasks ...
  }

  // The processing logic must call this when the queue drains,
  // otherwise the coordinator will never restart it.
  stopProcessing() {
    this.isProcessing = false;
  }
}

// ---------------------------------------------------------------
// Orchestration: validate -> add -> alert -> schedule.
// If a logger call throws, the task is already queued; the error
// propagates rather than being swallowed.
// ---------------------------------------------------------------
class QueueCoordinator {
  constructor(queue, {
    logger = new QueueLogger(),
    maxNormalPriority = MAX_NORMAL_PRIORITY,
  } = {}) {
    this.queue = queue;
    this.logger = logger;
    this.maxNormalPriority = maxNormalPriority;
  }

  enqueue(taskFn, priority) {
    validateTask(taskFn, priority);
    const task = this.queue.addTask(taskFn, priority);

    if (priority > this.maxNormalPriority) {
      this.logger.highPriorityAdded(this.queue.queueName);
    }
    if (!this.queue.isProcessing) {
      this.logger.starting(this.queue.queueName);
      this.queue.startProcessing();
    }
    return task;
  }
}

module.exports = {
  TaskQueue,
  QueueCoordinator,
  QueueLogger,
  validateTask,
  MAX_NORMAL_PRIORITY,
};

// Usage:
// const queue = new TaskQueue('emails');
// const coordinator = new QueueCoordinator(queue);
// coordinator.enqueue(() => sendEmail(), 10);
