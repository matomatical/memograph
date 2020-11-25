import heapq
import functools
import itertools

def topk(items, k, key=id, reverse=False):
    items = iter(items)
    heap = Heap(itertools.islice(items, k), key=key, minheap=not reverse)
    for item in items:
        heap.replace_if_gt(item)
    return list(heap)

class Heap:
    def __init__(self, items=None, key=id, minheap=True):
        self.minheap = minheap
        self.key = key
        if items is None:
            self.heap = []
        else:
            self.heap = [self._itemise(i) for i in items]
            heapq.heapify(self.heap)
    def _itemise(self, item):
        if self.minheap:
            return MinHeapItem(item, self.key(item))
        else:
            return MaxHeapItem(item, self.key(item))
    def push(self, item):
        heapq.heappush(self.heap, self._itemise(item))
    def pop(self):
        return heapq.heappop(self.heap).item
    def replace(self, item):
        heapq.heapreplace(self.heap, self._itemise(item))
    def replace_if_gt(self, item):
        i = self._itemise(item)
        if i > self.heap[0]:
            heapq.heapreplace(self.heap, i)
    def peek(self):
        return self.heap[0].item
    def __iter__(self):
        return (i.item for i in self.heap)
    def __len__(self):
        return len(self.heap)
    def __str__(self):
        return "Heap({}, key={}, minheap={})".format(
                [i.item for i in self.heap],
                self.key,
                self.minheap,
            )

class HeapItem:
    def __init__(self, item, key):
        self.item = item
        self.key = key
    def __eq__(self, other):
        return self.key == other.key

@functools.total_ordering
class MinHeapItem(HeapItem):
    def __lt__(self, other):
        return self.key < other.key

@functools.total_ordering
class MaxHeapItem(HeapItem):
    def __lt__(self, other):
        # REVERSE THE COMPARISON
        return self.key > other.key

