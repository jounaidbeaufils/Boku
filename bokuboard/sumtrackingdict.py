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
