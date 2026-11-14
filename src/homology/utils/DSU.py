class DSU:
    """Disjoint-set union structure with path compression and union by size."""

    def __init__(self) -> None:
        """Initializes the data structure."""
        self.parent = {}
        self.size = {}

    def make_set(self, n: int):
        """Add the element n as a new singleton set."""
        self.parent[n] = n
        self.size[n] = 1

    def find_set(self, n: int):
        """Returns the representative of the set containing n."""
        repr = self.parent[n]

        if repr == n:
            return n

        new_repr = self.find_set(repr)
        self.parent[n] = new_repr

        return new_repr

    def union_set(self, n1: int, n2: int) -> bool:
        """Merges the sets containing n1 and n2 and returns whether they were already merged."""
        repr1 = self.find_set(n1)
        repr2 = self.find_set(n2)

        if repr1 == repr2:
            return False

        if self.size[repr1] > self.size[repr2]:
            repr1, repr2 = repr2, repr1

        self.parent[repr1] = repr2
        self.size[repr2] += self.size[repr1]

        return True
