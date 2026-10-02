from collections import defaultdict
from typing import Iterable
import utils

from simplicial_complex import SimplicialComplex

class FilteredSimplicialComplex():
    def _finish_insertion(self, additions: set[tuple[int, ...]], time: float) -> None:
        self.timestamps[time].update(self.sc.face_set)

        for addition in additions:
            self.time_of[addition] = time

    def __init__(self, generator: Iterable[tuple[int, ...]]) -> None:
        self.sc = SimplicialComplex(generator)

        self.timestamps = defaultdict(set)
        self.time_of = {}

        self._finish_insertion(self.sc.face_set, 0.0)
    
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
