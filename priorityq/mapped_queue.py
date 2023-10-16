# -*- coding: utf-8 -*-
#
# priorityq: An object-oriented priority queue with updatable priorities.
#
# Copyright 2018 Edward L. Platt
#
# This software is released under multiple licenses. See the LICENSE file for
# more information.
#
# Authors:
#   Edward L. Platt <ed@elplatt.com>
"""Priority queue class with updatable priorities.
"""

import heapq

__all__ = ['MappedQueue']


class MappedQueue():
    """The MappedQueue class implements an efficient minimum heap. The
    smallest element can be popped in O(1) time, new elements can be pushed
    in O(log n) time, and any element can be removed or updated in O(log n)
    time. The queue cannot contain duplicate elements and an attempt to push an
    element already in the queue will have no effect.

    MappedQueue complements the heapq package from the python standard
    library. While MappedQueue is designed for maximum compatibility with
    heapq, it has slightly different functionality.

    Examples
    --------

    A `MappedQueue` can be created empty or optionally given an array of
    initial elements. Calling `push()` will add an element and calling `pop()`
    will remove and return the smallest element.

    >>> q = MappedQueue([916, 50, 4609, 493, 237])
    >>> q.push(1310)
    True
    >>> x = [q.pop() for i in range(len(q.h))]
    >>> x
    [50, 237, 493, 916, 1310, 4609]

    Elements can also be updated or removed from anywhere in the queue.

    >>> q = MappedQueue([916, 50, 4609, 493, 237])
    >>> q.remove(493)
    >>> q.update(237, 1117)
    >>> x = [q.pop() for i in range(len(q.h))]
    >>> x
    [50, 916, 1117, 4609]

    References
    ----------
    .. [1] Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2001).
       Introduction to algorithms second edition.
    .. [2] Knuth, D. E. (1997). The art of computer programming (Vol. 3).
       Pearson Education.
    """

    def __init__(self, data=None):
        """Priority queue class with updatable priorities.
        """
        if data is None:
            data = []
        self.h = list(data)
        self.d = dict()
        self._heapify()

    def __len__(self):
        return len(self.h)

    def _heapify(self):
        """Restore heap invariant and recalculate map."""
        heapq.heapify(self.h)
        self.d = dict([(elt, pos) for pos, elt in enumerate(self.h)])
        if len(self.h) != len(self.d):
            raise AssertionError("Heap contains duplicate elements")

    def push(self, elt):
        """Add an element to the queue."""
        # If element is already in queue, do nothing
        if elt in self.d:
            return False
        # Add element to heap and dict
        pos = len(self.h)
        self.h.append(elt)
        self.d[elt] = pos
        # Restore invariant by sifting down
        self._siftdown(pos)
        return True

    def pop(self):
        """Remove and return the smallest element in the queue."""
        # Remove smallest element
        elt = self.h[0]
        del self.d[elt]
        # If elt is last item, remove and return
        if len(self.h) == 1:
            self.h.pop()
            return elt
        # Replace root with last element
        last = self.h.pop()
        self.h[0] = last
        self.d[last] = 0
        # Restore invariant by sifting up, then down
        pos = self._siftup(0)
        self._siftdown(pos)
        # Return smallest element
        return elt

    def update(self, elt, new):
        """Replace an element in the queue with a new one."""
        # Replace
        pos = self.d[elt]
        self.h[pos] = new
        del self.d[elt]
        self.d[new] = pos
        # Restore invariant by sifting up, then down
        pos = self._siftup(pos)
        self._siftdown(pos)

    def remove(self, elt):
        """Remove an element from the queue."""
        # Find and remove element
        try:
            pos = self.d[elt]
            del self.d[elt]
        except KeyError as e:
            # Not in queue
            raise ValueError(f"Element ({elt}) not in queue") from e
        # If elt is last item, remove and return
        if pos == len(self.h) - 1:
            self.h.pop()
            return
        # Replace elt with last element
        last = self.h.pop()
        self.h[pos] = last
        self.d[last] = pos
        # Restore invariant by sifting up, then down
        pos = self._siftup(pos)
        self._siftdown(pos)

    def _siftup(self, pos):
        """Move element at pos down to a leaf by repeatedly moving the smaller
        child up."""
        h, d = self.h, self.d
        elt = h[pos]
        # Continue until element is in a leaf
        end_pos = len(h)
        left_pos = (pos << 1) + 1
        while left_pos < end_pos:
            # Left child is guaranteed to exist by loop predicate
            left = h[left_pos]
            try:
                right_pos = left_pos + 1
                right = h[right_pos]
                # Out-of-place, swap with left unless right is smaller
                if right < left:
                    h[pos], h[right_pos] = right, elt
                    pos, right_pos = right_pos, pos
                    d[elt], d[right] = pos, right_pos
                else:
                    h[pos], h[left_pos] = left, elt
                    pos, left_pos = left_pos, pos
                    d[elt], d[left] = pos, left_pos
            except IndexError:
                # Left leaf is the end of the heap, swap
                h[pos], h[left_pos] = left, elt
                pos, left_pos = left_pos, pos
                d[elt], d[left] = pos, left_pos
            # Update left_pos
            left_pos = (pos << 1) + 1
        return pos

    def _siftdown(self, pos):
        """Restore invariant by repeatedly replacing out-of-place element with
        its parent."""
        h, d = self.h, self.d
        elt = h[pos]
        # Continue until element is at root
        while pos > 0:
            parent_pos = (pos - 1) >> 1
            parent = h[parent_pos]
            if parent > elt:
                # Swap out-of-place element with parent
                h[parent_pos], h[pos] = elt, parent
                parent_pos, pos = pos, parent_pos
                d[elt] = pos
                d[parent] = parent_pos
            else:
                # Invariant is satisfied
                break
        return pos

class MappedQueueWithUndo(MappedQueue):
    """A MappedQueue with undo functionality. 
       This is my personal addition for the purpose of the boku assignment.
    """
    def __init__(self, data=None):
        if data is None:
            data = []
        super().__init__(data)
        self._history = []

    def get_element(self, elt):
        """Return the element if it exists in the priority queue, otherwise return None."""
        return elt if elt in self.d else None
        
    def push(self, elt):
        """Add an element to the queue."""
        result = super().push(elt)
        if result:  # Only add to history if the element was actually added
            self._history.append(('remove', elt))
        return result

    def pop(self):
        """Remove and return the smallest element in the queue."""
        elt = super().pop()
        self._history.append(('push', elt))
        return elt

    def update(self, elt, new):
        """Replace an element in the queue with a new one.
        if the element is not in the queue, add it.
        """
        if elt not in self.d:
            super().push(new)
        else:
            # Before updating, store the original value in history
            self._history.append(('update', new, elt))
            super().update(elt, new)

    def remove(self, elt):
        """Remove an element from the queue."""
        # Store the removed element for undo purposes
        self._history.append(('push', elt))
        super().remove(elt)

    def undo(self):
        """Undo the last operation."""
        if not self._history:
            print("MappedQueueWithUndo had no history to undo.")
            return
        
        action, *args = self._history.pop()
        # Call the inverse function without recording to history
        if action == 'push':
            self._silent_push(*args)
        elif action == 'remove':
            self._silent_remove(*args)
        elif action == 'update':
            self._silent_update(*args)

    def _silent_push(self, elt):
        """Push without recording to history."""
        super().push(elt)

    def _silent_remove(self, elt):
        """Remove without recording to history."""
        super().remove(elt)

    def _silent_update(self, elt, new):
        """Update without recording to history."""
        super().update(elt, new)