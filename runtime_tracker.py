# runtime_tracker.py
import time
import logging

class RuntimeTracker:
    def __init__(self, logger=None):
        self.start_time = time.time()
        self.last_checkpoint = self.start_time
        self.total_runtime = 0
        self.logger = logger or logging.getLogger(__name__)
        self.is_running = False

    def _log_runtime(self, message):
        if self.logger:
            self.logger.info(message)

    def start(self):
        if not self.is_running:
            self.start_time = time.time()
            self.last_checkpoint = self.start_time
            self.is_running = True
            self._log_runtime("Runtime tracking started.")

    def stop(self):
        if self.is_running:
            self.total_runtime += time.time() - self.start_time
            self.is_running = False
            self._log_runtime(f"Runtime tracking stopped. Total runtime: {self.total_runtime:.2f} seconds.")

    def checkpoint(self):
        if self.is_running:
            current_time = time.time()
            elapsed_since_last_checkpoint = current_time - self.last_checkpoint
            self.last_checkpoint = current_time
            self._log_runtime(f"Checkpoint reached. Elapsed time since last checkpoint: {elapsed_since_last_checkpoint:.2f} seconds.")
            return elapsed_since_last_checkpoint
        else:
            self._log_runtime("Runtime tracking is not active. No checkpoint recorded.")

    def get_total_runtime(self):
        if self.is_running:
            current_time = time.time()
            return self.total_runtime + (current_time - self.start_time)
        else:
            return self.total_runtime

    def reset(self):
        self.total_runtime = 0
        self.start_time = time.time()
        self.last_checkpoint = self.start_time
        self._log_runtime("Runtime tracker has been reset.")

# Example usage
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    tracker = RuntimeTracker()
    tracker.start()

    # Simulate some processing
    time.sleep(2)
    tracker.checkpoint()

    time.sleep(3)
    tracker.stop()

    print(f"Total runtime: {tracker.get_total_runtime():.2f} seconds.")


"""A RuntimeTracker class is defined to manage the tracking of runtime for a system or application.
The _log_runtime private method is used for logging runtime events if a logger is provided.
start, stop, checkpoint, get_total_runtime, and reset methods control the tracking of runtime.
The checkpoint method logs the time elapsed since the last checkpoint and can be used to track runtime between specific operations.
The get_total_runtime method calculates the total runtime, considering if the tracker is currently running or not.
The reset method sets the total runtime back to zero and starts the tracking anew."""
