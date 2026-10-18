import math
import utils

from typing import Optional

import matplotlib.colors
import matplotlib.pyplot as plt

from scipy.spatial import Delaunay
from scipy.spatial import Voronoi, voronoi_plot_2d

from simplex import Simplex
from filtered_simplicial_complex import FilteredSimplicialComplex


class AlphaFiltration:
    """Factory for building the Alpha complex filtration of a planar point cloud."""

    def __init__(self, points: list[tuple[float, ...]]) -> None:
        """Initialize the factory with a point cloud."""
        self._points: list[tuple[float, ...]] = points
        self._dist_map: dict[tuple[int, int], float] = {}
        self._n = len(points)

    @staticmethod
    def plot_2d(points: list[tuple[float, ...]], fsc: FilteredSimplicialComplex, time: Optional[float] = None) -> None:
        """Plot the point cloud and the alpha complex at the given time."""
        if time is None:
            sc = fsc.sc
        else:
            sc = fsc.filtration(time)

        color = matplotlib.colors.ListedColormap("royalblue")
        voronoi = Voronoi(points)

        voronoi_plot_2d(voronoi, show_vertices=False, line_width=2, line_colors='red')

        for simplicial in sc.face_set:
            if simplicial.dim() == 0:
                u = points[simplicial[0]]
                plt.plot(u[0], u[1], 'ko')

            if simplicial.dim() == 1:
                u, v = points[simplicial[0]], points[simplicial[1]]
                plt.plot([u[0], v[0]], [u[1], v[1]], color='k', lw=2)

            if simplicial.dim() == 2:
                plt.tripcolor(
                    [points[simplicial[i]][0] for i in range(3)],
                    [points[simplicial[i]][1] for i in range(3)],
                    [simplicial[i] for i in range(3)],
                    edgecolor='k', lw=2, cmap=color
                )

        plt.show()

    def _circumradius(self, u: int, v: int, w: int) -> float:
        """Return the circumradius of the triangle through three vertices."""
        return utils.circumradius(self._points[u], self._points[v], self._points[w])

    def _sq_dist(self, u: int, v: int) -> float:
        """Return the squared distance between two vertices, cached by index pair."""
        key = (u, v)

        if key not in self._dist_map:
            self._dist_map[key] = utils.sq_distance(self._points[key[0]], self._points[key[1]])

        return self._dist_map[key]

    def _is_gabriel_edge(self, u: int, v: int, w: int) -> bool:
        """Return whether the edge is Gabriel with respect to the opposite vertex."""
        x, y, z = self._points[u], self._points[v], self._points[w]

        return 4 * utils.sq_distance(utils.midpoint(x, y), z) >= self._sq_dist(u, v)


    def build(self) -> FilteredSimplicialComplex:
        """Builds the alpha filtration of the point cloud."""
        triangle_map = {}
        edge_map = {}
        incident_min = {}
        not_gabriel = set()

        # Generate the Delaunay complex with sorted triangles
        delaunay = Delaunay(self._points)

        for simplex in delaunay.simplices:
            u, v, w = sorted(simplex)

            center = self._circumradius(u, v, w)

            # 1. The time of the triangle is it's circumradius
            triangle_map[(u, v, w)] = center

            # 2. The time of the edge has two cases
            for (a, b), opposite in (((u, v), w), ((u, w), v), ((v, w), u)):
                incident_min[(a, b)] = min(incident_min.get((a, b), math.inf), center)

                if self._is_gabriel_edge(a, b, opposite):
                    # 2b. Gabriel case: the time is the distance divided by 2
                    edge_map.setdefault((a, b), math.sqrt(self._sq_dist(a, b)) / 2)
                else:
                    not_gabriel.add((a, b))

        # 2a. Non-Gabriel case: the smallest circumradius among the incident triangles.
        for edge, smallest in incident_min.items():
            if edge in not_gabriel:
                edge_map[edge] = smallest
            else:
                edge_map[edge] = min(edge_map[edge], smallest)

        # Add the points
        sc = FilteredSimplicialComplex(Simplex((i,)) for i in range(self._n))

        # Add the edges
        for simpl, value in edge_map.items():
            sc.insert([Simplex(simpl)], value)

        # Add the triangles
        for simpl, value in triangle_map.items():
            sc.insert([Simplex(simpl)], value)

        return sc
