from collections import defaultdict
from typing import Iterable, Optional
import utils

from simplicial_complex import SimplicialComplex

class FilteredSimplicialComplex():
    def _finish_insertion(self, additions: set[tuple[int, ...]], time: float) -> None:
        self.timestamps[time].update(additions)

        for addition in additions:
            self.time_of[addition] = time

    def __init__(self, generator: Iterable[tuple[int, ...]]) -> None:
        self.sc = SimplicialComplex(generator)

        self.timestamps = defaultdict(set)
        self.time_of = {}

        self._finish_insertion(self.sc.face_set, 0.0)

    @property
    def face_set(self) -> set[tuple[int, ...]]:
        return self.sc.face_set

    @property
    def filtration_order(self) -> list[tuple[int, ...]]:
        return [
            simp 
            for _, v in sorted(self.timestamps.items()) 
            for simp in sorted(v, key=len)
        ]
    
    def insert(self, generator: Iterable[tuple[int, ...]], time: float) -> None:
        for face in generator:
            if face in self.sc.face_set:
                raise ValueError("'generator' contains an already added face")

        new_sc = SimplicialComplex(self.sc.face_set)
        additions = new_sc.insert(generator)

        for addition in additions:
            for face in utils.power_set(addition):
                t = self.time_of.get(face)

                if t and t > time:
                    raise ValueError("'generator' contains a face with a bad time value")

        self.sc = new_sc
        self._finish_insertion(additions, time)

    def filtration(self, time: float) -> SimplicialComplex:
        return SimplicialComplex(
            simplex 
            for k, v in self.timestamps.items() 
            if k <= time 
            for simplex in v
        )

    def threshold(self, simplex: tuple[int, ...]) -> Optional[float]:
        return self.time_of.get(simplex)
