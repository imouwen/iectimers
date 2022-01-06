"""
   Some IEC 61131-3 timers for Python
   Code by @imouwen
"""


import arrow

# Base class for timers
class TIMER:
    def __init__(self):
        self.IN = False
        self.Q = False
        self.PT = 0
        self.ET = 0
        self.time = None

    def __call__(self, IN = None, PT = None):
        if IN is not None:
            self.IN = bool(IN)
        if (PT is not None):
            self.PT = max(0, float(PT))

        return self.update()

    def update(self):
        pass

class TON(TIMER):
    def update(self):
        if not self.IN:
            self.Q = False
            self.ET = 0
            self.time = None
        else:
            now = arrow.utcnow()
            if self.time is not None:
                self.ET += (now - self.time).total_seconds()
                self.ET = min(self.ET, self.PT)
            
            self.time = now

            self.Q = (self.ET >= self.PT)

        return self.Q

class TOF(TIMER):
    def __init__(self):
        TIMER.__init__(self)
        self.TON = TON()

    def update(self):
        self.TON(IN = self.Q and (not self.IN), PT = self.PT)

        if self.IN:
            self.Q = True
            self.ET = 0
        elif self.Q:
            self.Q = not self.TON.Q
            self.ET = self.TON.ET
        else:
            self.ET = 0

        return self.Q

class TP(TIMER):
    def __init__(self):
        TIMER.__init__(self)
        self.TON = TON()

    def update(self):
        self.TON(IN = self.IN or self.Q, PT = self.PT)
    
        self.ET = self.TON.ET

        if self.TON.Q:
            self.Q = False
        elif self.IN:
            self.Q = True
