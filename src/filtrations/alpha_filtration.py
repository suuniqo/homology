import utils
import math

from typing import Optional

import matplotlib.pyplot as plt
import matplotlib.colors

from scipy.spatial import Voronoi, voronoi_plot_2d
from scipy.spatial import Delaunay

from simplex import Simplex
from filtered_simplicial_complex import FilteredSimplicialComplex


class AlphaFiltration:
    """Builds the Alpha complex filtration of a planar point cloud."""

    def __init__(self, points: list[tuple[float, ...]]) -> None:
        self.points: list[tuple[float, ...]] = points

    @staticmethod
    def plot_2d(points: list[tuple[float, ...]], fsc: FilteredSimplicialComplex, time: Optional[float] = None) -> None:
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
        

    def build(self) -> FilteredSimplicialComplex:
        # The FilteredSimplicialComplex doesn't support updating the filtration value
        three_dims = {}
        two_dims = {}

        n = len(self.points)

        dist = {
            i : {
                j: utils.sq_distance(self.points[i], self.points[j])
                for j in range(n)
            }
            for i in range(n)
        }

        sc = FilteredSimplicialComplex(Simplex((i,)) for i in range(n))

        # Generate the Delaunay complex
        dl = Delaunay(self.points)

        for simplex in dl.simplices:
            [u, v, w] = sorted(simplex)

            # Assume fist case for the three edges
            if (u, v) not in two_dims:
                two_dims[(u, v)] = math.sqrt(dist[u][v]) / 2

            if (u, w) not in two_dims:
                two_dims[(u, w)] = math.sqrt(dist[u][w]) / 2

            if (v, w) not in two_dims:
                two_dims[(v, w)] = math.sqrt(dist[v][w]) / 2

            x, y, z = self.points[u], self.points[v], self.points[w]

            # The triangle is added always in this time
            center = utils.distance_to_center(x, y, z)
            three_dims[(u, v, w)] = center

            # Check if the edges use the second case
            if utils.sq_distance(utils.median_point(x, y), z) < (dist[u][v] / 4):
                two_dims[(u, v)] = center

            if utils.sq_distance(utils.median_point(x, z), y) < (dist[u][w] / 4):
                two_dims[(u, w)] = center

            if utils.sq_distance(utils.median_point(y, z), x) < (dist[v][w] / 4):
                two_dims[(v, w)] = center

        for simpl, value in two_dims.items():
            sc.insert([Simplex(simpl)], value)

        for simpl, value in three_dims.items():
            sc.insert([Simplex(simpl)], value)

        return sc
