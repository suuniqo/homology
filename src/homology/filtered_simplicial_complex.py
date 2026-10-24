from __future__ import annotations

from collections import defaultdict
from collections.abc import Iterable
from typing import Optional

from homology.simplex import Simplex
from homology.simplicial_complex import SimplicialComplex


class FilteredSimplicialComplex:
    """Represents a simplicial complex whose simplices carry filtration timestamps."""

    def _finish_insertion(self, additions: set[Simplex], time: float) -> None:
        """Add simplices to the timestamp dictionary."""
        if not additions:
            return

        self.timestamps[time].update(additions)

        for addition in additions:
            self.time_of[addition] = time

    def __init__(self, generator: Iterable[Simplex], time: float = 0.0) -> None:
        """Initialize the filtered complex with a set of simplices."""
        self.sc: SimplicialComplex = SimplicialComplex(generator)

        self.timestamps: dict[float, set[Simplex]] = defaultdict(set)
        self.time_of: dict[Simplex, float] = {}

        self._finish_insertion(self.sc.face_set, time)

    @property
    def face_set(self) -> set[Simplex]:
        """Return the face set."""
        return self.sc.face_set

    @property
    def filtration_order(self) -> list[Simplex]:
        """Return the filtration order as a sorted list of simplices."""
        return [
            simplex 
            for _, v in sorted(self.timestamps.items()) 
            for simplex in sorted(v, key=lambda s: (s.dim(), s.vertices))
        ]
    
    def insert(self, generator: Iterable[Simplex], time: float) -> None:
        """Insert a generator of simplices at the given timestamp."""
        generator = list(generator)

        for simplex in generator:
            if simplex in self.sc.face_set:
                raise ValueError("'generator' contains an already added simplex")

        additions: set[Simplex] = set()

        for simplex in generator:
            additions.update(simplex.faces())

        additions -= self.sc.face_set

        for addition in additions:
            for face in addition.faces():
                t = self.time_of.get(face)

                if t is not None and t > time:
                    raise ValueError("'generator' contains a face with a bad time value")

        self.sc.insert(generator)
        self._finish_insertion(additions, time)

    def filtration(self, time: float) -> SimplicialComplex:
        """Return the simplicial complex at the given timestamp."""
        return SimplicialComplex(
            simplex 
            for k, v in self.timestamps.items() 
            if k <= time 
            for simplex in v
        )

    def threshold(self, simplex: Simplex) -> Optional[float]:
        """Compute the threshold value of a simplex."""
        return self.time_of.get(simplex)

    def threshold_values(self) -> list[float]:
        """Return the sorted list of all threshold values."""
        return sorted(self.timestamps.keys())
