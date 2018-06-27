class MaxHeap: # element: {docID: score}
    def __init__(self):
        self.data = []

    def __init__(self):


    def size(self):
        return len(self.data)

    def isEmpty(self):
        return self.size == 0

    def insert(self, item):
        self.data.append(item)
        self.shiftUp(self.size())

    def max(self):
        self.data[0], self.data[self.size() - 1] = self.data[self.size() - 1], self.data[0]
        max = self.data.pop()
        self.shiftDown(1)
        return max

    def maxK(self, k):
        topK = []
        for k in range(k):
            topK.append(self.max())
        return topK

    def shiftUp(self, p):
        while p > 1 and self.data[p - 1].values()[0] > self.data[(p - 1) // 2].values()[0]:
            self.data[p - 1], self.data[(p - 1) // 2] = self.data[(p - 1) // 2] - self.data[p - 1]
            p = (p - 1) // 2 + 1

    def shiftDown(self, p):
        while 2 * p <= self.size():
            q = 2 * p
            if q + 1 <= self.size():
                if self.data[q - 1].values()[0] < self.data[q].values()[0]:
                    q += 1
            if self.data[p - 1].values()[0] > self.data[q - 1].values()[0]:
                break
            self.data[p - 1], self.data[q - 1] = self.data[q - 1], self.data[p - 1]
            p = q
