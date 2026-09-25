from typing import Iterable
from collections import defaultdict

class SimplicialComplex:
    @staticmethod
    def _power_set(simplicial: tuple[int, ...]) -> list[tuple[int, ...]]:
        n = len(simplicial)

        res = []

        for i in range(1, 1 << n):
            res.append(tuple(
                simplicial[j] for j in range(n) if i & (1 << j)
            ))
        
        return res

    @staticmethod
    def _euler_characteristic(face_set: set[tuple[int, ...]]) -> int:
        chi = 0

        for face in face_set:
            if len(face) - 1 % 2 == 0:
                chi += 1
            else:
                chi -= 1

        return chi

    @staticmethod
    def is_face(s1: tuple[int, ...], s2: tuple[int, ...]) -> bool:
        return all(i in s2 for i in s1)

    @staticmethod
    def is_disjoint(s1: tuple[int, ...], s2: tuple[int, ...]) -> bool:
        return all(i not in s1 for i in s2)

    def __init__(self, generator: Iterable[tuple[int, ...]]) -> None:
        self.cardinality = 0
        self.face_set = set() 

        for simplicial in generator:
            self.face_set.update(self._power_set(simplicial))
            if len(simplicial) > self.cardinality:
                self.cardinality = len(simplicial)

        self.euler_characteristic = self._euler_characteristic(self.face_set)

    @property
    def dimension(self):
        return self.cardinality - 1

    def n_faces(self, dim: int) -> set[tuple[int, ...]]:
        return {face for face in self.face_set if len(face) - 1 == dim}

    def skeleton(self, dim: int) -> set[tuple[int, ...]]:
        return {face for face in self.face_set if len(face) - 1 <= dim}

    def st(self, simplicial: tuple[int, ...]) -> set[tuple[int, ...]]:
        res = {member for member in self.face_set if self.is_face(simplicial, member)}

        if not res:
            raise ValueError("'simplicial' is not a face")

        return res

    def closed_st(self, simplicial: tuple[int, ...]) -> SimplicialComplex:
        return SimplicialComplex(self.st(simplicial))

    def lk(self, simplicial: tuple[int, ...]) -> set[tuple[int, ...]]:
        closed = self.closed_st(simplicial)
        return {elem for elem in closed.face_set if self.is_disjoint(simplicial, elem)}

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
