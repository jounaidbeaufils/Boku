""" Module containing the HeuristicTile class, which is used with the MappedQueue class """
class HeuristicTile:
    """A clsas representing the value of a tile for use in a MappedQueue"""
    def __init__(self, tile, value):
        self.tile = tile
        self.priority = value

    # Representation for easier debugging
    def __repr__(self):
        return f"HeuristicTile({self.tile!r}, {self.priority!r})"

    # Comparison based on priority
    def __lt__(self, other):
        return self.priority < other.priority

    def __eq__(self, other):
        return self.priority == other.priority

    # Hashing based on tile (assuming tile coord are unique)
    def __hash__(self):
        return hash(self.tile)
