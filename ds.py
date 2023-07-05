import numpy as np

class Stack:
    def __init__(self):
        self.storage = []
        self.size = 0
    def push(self, data):
        self.storage.append(data)
        self.size += 1
    def pop(self):
        if self.size > 0:
            self.size -= 1
            return self.storage.pop()
        else:
            return None
    def getSize(self):
        return self.size
    def isEmpty(self):
        return self.size == 0
    def peek(self):
        if self.size > 0:
            return self.storage[-1]
        else:
            return None
    def __str__(self):
        return str(self.storage)

class Queue:
    def __init__(self):
        self.storage = []
        self.size = 0

    def enqueue(self, data):
        self.storage.append(data)
        self.size += 1

    def dequeue(self):
        if self.size > 0:
            self.size -= 1
            return self.storage.pop(0)
        else:
            return None

    def getSize(self):
        return self.size

    def isEmpty(self):
        return self.size == 0

    def peek(self):
        if self.size > 0:
            return self.storage[0]
        else:
            return None

    def __str__(self):
        return str(self.storage)

class PriorityQueue(object):
	def __init__(self):
		self.queue = []

	def __str__(self):
		return ' '.join([str(i) for i in self.queue])

	# for checking if the queue is empty
	def isEmpty(self):
		return len(self.queue) == 0

	# for inserting an element in the queue
	def insert(self, data):
		self.queue.append(data)

	# for popping an element based on Priority
	def dequeue(self):
		try:
			max_val = 0
			for i in range(len(self.queue)):
				if self.queue[i]['score'] < self.queue[max_val]['score']:
					max_val = i
			item = self.queue[max_val]
			del self.queue[max_val]
			return item
		except IndexError:
			print()
			exit()