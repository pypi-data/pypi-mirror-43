from tbas.datatypes import Memory


class Buffer(object):
    def __init__(self, max_length=512):
        self.buffer: Memory = []
        self.max_length = max_length

    def __repr__(self):
        out = ""
        for k in self.buffer:
            if k == 0:
                return out
            out += chr(max(0, k))
        return out

    def enqueue(self, newval):
        if len(self.buffer) < self.max_length:
            self.buffer.append(newval)

    def dequeue_filo(self):
        if len(self.buffer) == 0:
            return 0
        return self.buffer.pop()

    def dequeue_fifo(self):
        if len(self.buffer) == 0:
            return 0
        val = self.buffer[0]
        self.buffer = self.buffer[1:]
        return val

    def clear(self):
        self.buffer = []
