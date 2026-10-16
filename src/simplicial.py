from __future__ import annotations

import utils


class Simplicial:
    def __init__(self, vertices: tuple[int, ...]) -> None:
        self.vertices: tuple[int, ...] = tuple(sorted((vertices)))

    def dim(self) -> int:
        return len(self.vertices) - 1

    def is_face(self, other: Simplicial) -> bool:
        return all(i in other.vertices for i in self.vertices)

    def is_disjoint(self, other: Simplicial) -> bool:
        return all(i not in self.vertices for i in other.vertices)

    def faces(self):
        return {Simplicial(t) for t in utils.power_set(self.vertices)}

    def __iter__(self):
        return iter(self.vertices)

    def __getitem__(self, index: int) -> int:
        return self.vertices[index]

    def __hash__(self) -> int:
        return hash(self.vertices)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Simplicial):
            return self.vertices == other.vertices
        return NotImplemented
