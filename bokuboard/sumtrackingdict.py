"""A module containing a dictionary that keeps track of the sum of its values."""
class SumTrackingDict(dict):
    """A dictionary that keeps track of the sum of its values."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._total = sum(self.values())

    def __setitem__(self, key, value):
        if key in self:
            self._total -= self[key]  # Subtract the old value from total
        super().__setitem__(key, value)
        self._total += value  # Add the new value to total

    def __delitem__(self, key):
        self._total -= self[key]  # Subtract the value of the removed item from total
        super().__delitem__(key)

    def total(self):
        """Return the sum of all values in the dictionary."""
        return self._total


class SumTrackingDictWithUndo(SumTrackingDict):
    """A dictionary that keeps track of the sum of its values and supports undo operations."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._undo_stack = []

    def __setitem__(self, key, value):
        # If the key already exists, save its current value to the undo stack, otherwise save None
        prev_value = self[key] if key in self else None
        self._undo_stack.append(("set", key, prev_value))
        
        super().__setitem__(key, value)

    def __delitem__(self, key):
        # Save the key and its current value to the undo stack before deletion
        self._undo_stack.append(("del", key, self[key]))
        
        super().__delitem__(key)

    def undo(self):
        """Revert the last operation."""
        if not self._undo_stack:
            raise ValueError("No operations to undo")

        operation, key, prev_value = self._undo_stack.pop()

        if operation == "set":
            if prev_value is None:  # The key was added in the previous operation, so delete it
                super().__delitem__(key)
            else:  # The key was modified in the previous operation, so set it back to its old value
                super().__setitem__(key, prev_value)
        elif operation == "del":
            super().__setitem__(key, prev_value)
