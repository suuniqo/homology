from __future__ import annotations

from collections import defaultdict
from collections.abc import Iterable

from homology.simplex import Simplex
from homology.utils.DSU import DSU


class SimplicialComplex:
    """Represents a simplicial complex: a set of simplices closed under taking faces."""

    @staticmethod
    def _euler_characteristic(face_set: set[Simplex]) -> int:
        """Compute the Euler characteristic using face dimensions."""
        chi = 0

        for face in face_set:
            if face.dim() % 2 == 0:
                chi += 1
            else:
                chi -= 1

        return chi

    def __init__(self, generator: Iterable[Simplex]) -> None:
        """Initialize the simplicial complex with a set of simplices."""
        self.dim: int = -1
        self._face_set: set[Simplex] = set()

        for simplex in generator:
            faces = simplex.faces()

            self._face_set.update(faces)

            if simplex.dim() > self.dim:
                self.dim = simplex.dim()

        self.euler_characteristic: int = self._euler_characteristic(self.face_set)

    @property
    def face_set(self) -> set[Simplex]:
        """Return the set of all simplices (treat as read-only)."""
        return self._face_set

    def n_faces(self, dim: int) -> set[Simplex]:
        """Return all simplices with the specified dimension."""
        return {face for face in self.face_set if face.dim() == dim}

    def skeleton(self, dim: int) -> set[Simplex]:
        """Return all simplices with dimension less than or equal to the specified value."""
        return {face for face in self.face_set if face.dim() <= dim}

    def st(self, simplex: Simplex) -> set[Simplex]:
        """Return the star of the simplex."""
        res = {member for member in self.face_set if simplex.is_face(member)}

        if not res:
            raise ValueError("'simplex' is not a face")

        return res

    def closed_st(self, simplex: Simplex) -> SimplicialComplex:
        """Return the closed star of the simplex."""
        return SimplicialComplex(self.st(simplex))

    def lk(self, simplex: Simplex) -> set[Simplex]:
        """Return the link of the simplex."""
        closed = self.closed_st(simplex)
        return {elem for elem in closed.face_set if simplex.is_disjoint(elem)}

    def graph(self) -> dict[int, list[int]]:
        """Return a dictionary representing the 1-skeleton as a graph."""
        graph = defaultdict(list)

        for v1, v2 in self.n_faces(1):
            graph[v1].append(v2)
            graph[v2].append(v1)

        return graph

    def connected_components(self) -> int:
        """Return the number of connected components."""
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

    def insert(self, generator: Iterable[Simplex]) -> None:
        """Insert a generator of simplices into the complex."""
        additions = set()

        for simplex in generator:
            difference = simplex.faces() - self.face_set

            additions.update(difference)
            self._face_set.update(difference)

            if simplex.dim() > self.dim:
                self.dim = simplex.dim()

        self.euler_characteristic += self._euler_characteristic(additions)

    def betti_planar(self) -> tuple[int, int]:
        """Computes the pair of betti numbers describing a planar simplicial complex."""

        dsu = DSU()

        betta_0 = 0
        betta_1 = 0

        edges = []

        for face in self._face_set:
            match face.dim():
                case 0:
                    betta_0 += 1
                    dsu.make_set(face.vertices[0])
                case 1:
                    edges.append(face.vertices)
                case 2:
                    betta_1 -= 1
                case _:
                    raise ValueError("The algorithm only works if the simplicial complex is planar")
        
        for u, v in edges:
            repr_u = dsu.find_set(u)
            repr_v = dsu.find_set(v)

            if repr_u == repr_v:
                betta_1 += 1
            else:
                dsu.union_set(repr_u, repr_v)
                betta_0 -= 1
        
        return (betta_0, betta_1)
