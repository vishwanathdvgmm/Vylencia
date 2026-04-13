# core/clock.py

import time

class Clock:
    def __init__(self, tick_seconds=0.1):
        self.tick_seconds = tick_seconds

    def tick(self):
        time.sleep(self.tick_seconds)
