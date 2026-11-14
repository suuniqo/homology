from __future__ import annotations

import homology.utils.math as utils


class Simplex:
    """Represents a simplex in topology, a set of vertices defining a geometric structure."""

    def __init__(self, vertices: tuple[int, ...]) -> None:
        """Initialize the Simplex object by providing the set of vertices."""

        # the vertices are sorted, so that the simplices (1,2,3) and (3,2,1) get the same representation
        verts = tuple(sorted(vertices))

        if len(set(verts)) != len(verts):
            raise ValueError("A simplex cannot contain repeated vertices")

        self._vertices: tuple[int, ...] = verts

    @property
    def vertices(self) -> tuple[int, ...]:
        """Return the sorted, immutable vertices of the simplex."""
        return self._vertices

    def dim(self) -> int:
        """Return the dimension of the simplex."""
        return len(self._vertices) - 1

    def is_face(self, other: Simplex) -> bool:
        """Return True if self is a face of the given simplex."""
        return set(self._vertices).issubset(other._vertices)

    def is_disjoint(self, other: Simplex) -> bool:
        """Return True if self and other share no common vertices."""
        return set(self._vertices).isdisjoint(other._vertices)

    def faces(self) -> set[Simplex]:
        """Return a set of all face simplices."""
        return {Simplex(t) for t in utils.power_set(self._vertices)}

    def __iter__(self):
        """Return an iterator over vertices."""
        return iter(self._vertices)

    def __getitem__(self, index: int) -> int:
        """Return the vertex at the specified index."""
        return self._vertices[index]

    def __hash__(self) -> int:
        """Return the hash value for use in sets and dictionaries."""
        return hash(self._vertices)

    def __eq__(self, other: object) -> bool:
        """Return True if self and other represent the same vertices."""
        if isinstance(other, Simplex):
            return self._vertices == other._vertices

        return NotImplemented

    def __repr__(self) -> str:
        """Return a readable representation of the simplex."""
        return f"Simplex({self._vertices})"
