from collections import deque

class Stack:

    def __init__(self):
        self.stack = deque()


    def empty(self):
        if len(self.stack) == 0:
            return True
        return False
        # return len(self.stack) == 0

    def peek(self):
        temporal = len(self.stack) - 1
        return self.stack[temporal]


    def push(self, element):
        self.stack.append(element)

    def pop(self):
        return self.stack.pop()