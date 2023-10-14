""" Module containing the HeuristicTile class, which is used with the MappedQueue class """
class HeuristicTile:
    """A clsas representing the value of a tile for use in a MappedQueue"""
    def __init__(self, name, value, source, stamp):
        self.name = name
        self.priority = value
        self.source = source
        self.stamp = stamp

    # Representation for easier debugging
    def __repr__(self):
        return f"HeuristicTile({self.name!r}, {self.priority!r}, {self.source!r}, {self.stamp!r})"

    # Comparison based on priority
    def __lt__(self, other):
        return self.priority < other.priority

    def __eq__(self, other):
        return self.priority == other.priority

    # Hashing based on name (assuming task names are unique)
    def __hash__(self):
        return hash(self.name)
