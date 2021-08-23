
class Stack:
    def __init__(self):
        self.list = []
    
    def is_empty(self):
        return self.list == []

    def push(self, x):
        self.list.append(x)

    def pop(self):
        return self.list.pop()
        
