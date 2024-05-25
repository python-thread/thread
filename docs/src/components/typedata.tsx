export interface TypeData {
  [key: string]: string;
}

export const Statuses: string[] = [
  "Idle",
  "Running",
  "Invoking hooks",
  "Completed",
  "Errored",
  "Kill Scheduled",
  "Killed",
];
export const ThreadStatuses: TypeData = {
  Idle: "This means that the thread is idle and ready to be ran.",
  Running: "This means that the thread is currently running.",
  "Invoking hooks": "This means that the thread is currently invoking hooks.",
  Completed:
    "This means that the thread and hooks have completed and is no longer running.",
  Errored: "This means that the thread has errored and is no longer running.",
  "Kill Scheduled":
    "This means that the thread has been scheduled to and will be killed when the next tick occurs.",
  Killed:
    "This means that the thread has been killed and is no longer running.",
};

export const Exceptions: string[] = [
  "ThreadStillRunningError",
  "ThreadNotRunningError",
  "ThreadNotInitializedError",
  "HookRuntimeError",
];
export const ThreadExceptions: TypeData = {
  ThreadStillRunningError:
    "Raised when the thread is still running and cannot invoke the method. You can wait for the thread to terminate by calling `Thread.join()` or check the status with `Thread.status`.",
  ThreadNotRunningError:
    "Raised when the thread is not running and cannot invoke the method. You can run `Thread.start()` to start the thread.",
  ThreadNotInitializedError:
    "Raised when the thread is not initialized and cannot invoke the method. You can initialize the thread by calling `Thread.__init__()`.",
  HookRuntimeError:
    "Raised when an error occurs in a hook. This is usually caused by an exception in a hook. You can find the exception in `Thread.errors`.",
};
