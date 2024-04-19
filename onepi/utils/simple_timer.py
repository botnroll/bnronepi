from threading import Timer
import time


class SimpleTimer:

    def __init__(self, increment, function):
        self.running = False
        self.increment = increment
        self.function = function
        self.time = 0

    def _update(self):
        self._cancel()
        self.running = False
        self.start()
        self.time = self.time + self.increment
        self.function()

    def start(self):
        if not self.running:
            self.timer = Timer(self.increment, self._update)
            self.timer.start()
            self.running = True
        else:
            print("Reset timer first")

    def _cancel(self):
        try:
            self.timer.cancel()
        except:
            pass

    def reset(self):
        self.stop()
        self.time = 0

    def stop(self):
        self._cancel()
        self.running = False

    def get_time(self):
        return self.time
