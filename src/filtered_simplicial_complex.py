from __future__ import annotations

from collections import defaultdict
from typing import Iterable, Optional

from simplicial import Simplicial
from simplicial_complex import SimplicialComplex


class FilteredSimplicialComplex():
    def _finish_insertion(self, additions: set[Simplicial], time: float) -> None:
        self.timestamps[time].update(additions)

        for addition in additions:
            self.time_of[addition] = time

    def __init__(self, generator: Iterable[Simplicial]) -> None:
        self.sc: SimplicialComplex = SimplicialComplex(generator)

        self.timestamps: dict[float, set[Simplicial]] = defaultdict(set)
        self.time_of: dict[Simplicial, float] = {}

        self._finish_insertion(self.sc.face_set, 0.0)

    @property
    def face_set(self) -> set[Simplicial]:
        return self.sc.face_set

    @property
    def filtration_order(self) -> list[Simplicial]:
        return [
            simp 
            for _, v in sorted(self.timestamps.items()) 
            for simp in sorted(v, key=Simplicial.dim)
        ]
    
    def insert(self, generator: Iterable[Simplicial], time: float) -> None:
        for face in generator:
            if face in self.sc.face_set:
                raise ValueError("'generator' contains an already added face")

        new_sc = SimplicialComplex(self.sc.face_set)
        additions = new_sc.insert(generator)

        for addition in additions:
            for face in addition.faces():
                t = self.time_of.get(face)

                if t and t > time:
                    raise ValueError("'generator' contains a face with a bad time value")

        self.sc = new_sc
        self._finish_insertion(additions, time)

    def filtration(self, time: float) -> SimplicialComplex:
        return SimplicialComplex(
            simplicial 
            for k, v in self.timestamps.items() 
            if k <= time 
            for simplicial in v
        )

    def threshold(self, simplicial: Simplicial) -> Optional[float]:
        return self.time_of.get(simplicial)

    def threshold_values(self) -> list[float]:
        return list(sorted(self.timestamps.keys()))
