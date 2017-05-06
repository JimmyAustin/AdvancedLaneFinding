import numpy as np
class RollingAverageTracker(object):
    def __init__(self, count):
        self.count = count
        self.tracked = []

    def add(self, amount):
        self.tracked.append(amount)
        self.tracked = self.tracked[-self.count:]

    def average(self):
        return np.average(self.tracked)
