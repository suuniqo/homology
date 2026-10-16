from __future__ import annotations
from typing import Iterable
from collections import defaultdict
from simplicial import Simplicial

class SimplicialComplex:
    @staticmethod
    def _euler_characteristic(face_set: set[Simplicial]) -> int:
        chi = 0

        for face in face_set:
            if face.dim() % 2 == 0:
                chi += 1
            else:
                chi -= 1

        return chi

    def __init__(self, generator: Iterable[Simplicial]) -> None:
        self.dim: int = -1
        self.face_set: set[Simplicial] = set()

        for simplicial in generator:
            faces = simplicial.faces()

            self.face_set.update(faces)

            if simplicial.dim() > self.dim:
                self.dim = simplicial.dim()

        self.euler_characteristic: int = self._euler_characteristic(self.face_set)

    def n_faces(self, dim: int) -> set[Simplicial]:
        return {face for face in self.face_set if face.dim() == dim}

    def skeleton(self, dim: int) -> set[Simplicial]:
        return {face for face in self.face_set if face.dim() <= dim}

    def st(self, simplicial: Simplicial) -> set[Simplicial]:
        res = {member for member in self.face_set if simplicial.is_face(member)}

        if not res:
            raise ValueError("'simplicial' is not a face")

        return res

    def closed_st(self, simplicial: Simplicial) -> SimplicialComplex:
        return SimplicialComplex(self.st(simplicial))

    def lk(self, simplicial: Simplicial) -> set[Simplicial]:
        closed = self.closed_st(simplicial)
        return {elem for elem in closed.face_set if simplicial.is_disjoint(elem)}

    def graph(self) -> dict[int, list[int]]:
        graph = defaultdict(list)

        for v1, v2 in self.n_faces(1):
            graph[v1].append(v2)
            graph[v2].append(v1)

        return graph

    def connected_components(self) -> int:
        visited = set()

        graph = self.graph()
        vertices = [v[0] for v in self.n_faces(0)]

        components = 0

        for u in vertices:
            if u in visited:
                continue

            queue = [u]
            visited.add(u)

            while queue:
                v = queue.pop()

                for neig in graph[v]:
                    if neig not in visited:
                        queue.append(neig)
                        visited.add(neig)

            components += 1

        return components

    def insert(self, generator: Iterable[Simplicial]) -> set[Simplicial]:
        additions = set()

        for simplicial in generator:
            difference = simplicial.faces() - self.face_set

            additions.update(difference)
            self.face_set.update(difference)

            if simplicial.dim() > self.dim:
                self.dim = simplicial.dim()

        self.euler_characteristic += self._euler_characteristic(additions)

        return additions
