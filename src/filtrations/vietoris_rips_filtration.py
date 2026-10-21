import math
import utils

from collections import defaultdict
from itertools import product
from functools import reduce

from simplex import Simplex
from filtered_simplicial_complex import FilteredSimplicialComplex


class VietorisRipsFiltration:
    """Factory for building the Vietoris-Rips filtration of a point cloud."""

    def __init__(self, points: list[tuple[float, ...]]):
        """Initialize the filtration with a point cloud."""
        self.points = points
        self.sc = FilteredSimplicialComplex(Simplex((i,)) for i in range(len(points)))

    # def _max_simplex(self, u: int, v: int , neigs: dict[int, set[int]]) -> set[Simplex]:
    #     """Return the maximal simplices extending the given simplex."""

    #     res = set()

    #     for simpl in self.sc.face_set:
    #         if not v in simpl.vertices:
    #             continue

    #         if u in reduce(lambda x, y: x.intersection(y), (neigs[w] for w in simpl.vertices)):
    #             new = Simplex(tuple(list(simpl.vertices) + [u]))
    #             if new not in self.sc.face_set:
    #                 res.add(new)

    #     return res 

    def _max_simplex(self, simplex: Simplex, common_neigs: set[int], neigs: dict[int, set[int]]) -> set[Simplex]:
        """Return the maximal simplices extending the given simplex."""
        res = set()

        for w in sorted(common_neigs):
            new = Simplex(tuple(list(simplex.vertices) + [w]))
            res.add(new)

            res.update(
                self._max_simplex(
                    new,
                    {x for x in common_neigs if x > w}.intersection(neigs[w]),
                    neigs
                )
            )

        return res

    def build(self) -> FilteredSimplicialComplex:
        """Build the Vietoris-Rips filtration of the point cloud."""
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

                # self.sc.insert(self._max_simplex(u, v, neig), time)
                
                self.sc.insert(
                    self._max_simplex(simplicial, neig[u].intersection(neig[v]), neig), 
                    time
                )
            
        return self.sc
