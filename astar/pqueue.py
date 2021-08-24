

class Pqueue:

    def __init__(self, priority=(lambda x: x)):
        """ Compare should be a function that takes an element of the queue and returns its priority """
        self.heap = []
        self.priority = priority

    def push(self, x):
        self.heap.append(x)
        self._filter_up(len(self.heap) - 1)

    def pop(self):
        if len(self.heap) == 1:
            return self.heap.pop()
        retval = self.heap[0]
        self.heap[0] = self.heap.pop()
        self._heapify()
        return retval

    def is_empty(self):
        return self.heap == []

    def _filter_up(self, i):
        parent = (i - 1) // 2
        if parent >= 0 and self.priority(self.heap[parent]) > self.priority(self.heap[i]):
            self.heap[parent], self.heap[i] = self.heap[i], self.heap[parent]
            self._filter_up(parent)

    def _heapify(self):
        self._heapify_helper(0)

    def _heapify_helper(self, i):
        min = i
        left_child = 2 * i + 1
        right_child = 2 * i + 2
        if (left_child < len(self.heap) and 
                self.priority(self.heap[left_child]) < self.priority(self.heap[i])
                ):
            min = left_child
        if (right_child < len(self.heap) and 
                self.priority(self.heap[right_child]) < self.priority(self.heap[min])
                ):
            min = right_child
        if min != i:
            self.heap[i], self.heap[min] = self.heap[min], self.heap[i]
            self._heapify_helper(min)


q = Pqueue()
