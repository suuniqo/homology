from collections import defaultdict
from itertools import product
from functools import reduce
import math

from simplex import Simplex
from filtered_simplicial_complex import FilteredSimplicialComplex
import utils

class VietorisRipsFiltration:
    """Builds the Vietoris-Rips filtered simplicial complex of a point cloud."""

    def __init__(self, points: list[tuple[float, ...]]):
        self.points = points
        self.sc = FilteredSimplicialComplex(Simplex((i,)) for i in range(len(points)))

    def _max_simplex(self, simplex: Simplex, neigs: dict[int, set[int]]) -> set[Simplex]:
        # print(simplex.vertices)
        # TODO: Make `res` a accumulation parameter instead of returning and copying it
        res = set()

        common_neigs = reduce(lambda x, y: x.intersection(y), (neigs[u] for u in simplex.vertices))

        for v in common_neigs:
            # Generates simplex `simplex` + [v]
            new_simplicial = Simplex(tuple(list(simplex.vertices) + [v]))
            res.add(new_simplicial)
            res.update(self._max_simplex(new_simplicial, neigs).difference(self.sc.face_set))

        return res

    def build(self) -> FilteredSimplicialComplex:
        n = len(self.points)
        dist = {
            i : {
                j: utils.sq_distance(self.points[i], self.points[j])
                for j in range(n) 
                if i != j
            }
            for i in range(n)
        }

        dist_rev: dict[float, set[Simplex]] = defaultdict(set)
        for i, j in product(range(n), repeat=2):
            if i != j:
                d = dist[i][j]
                dist_rev[d].update([Simplex((i, j))])

        neig: dict[int, set[int]] = defaultdict(set)

        for d in sorted(dist_rev.keys()):
            time = math.sqrt(d) / 2
            self.sc.insert(dist_rev[d], time)
            
            for simplicial in dist_rev[d]:
                u, v = simplicial
                neig[u].add(v)
                neig[v].add(u)

                self.sc.insert(
                    (
                        simpl 
                        for simpl in self._max_simplex(simplicial, neig) 
                        if simpl not in self.sc.face_set
                    ), 
                    time
                )

        return self.sc

