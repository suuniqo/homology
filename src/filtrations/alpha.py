import utils
import math

import matplotlib.pyplot as plt
import matplotlib.colors

from scipy.spatial import Voronoi, voronoi_plot_2d
from typing import Optional

from scipy.spatial import Delaunay

from filtered_simplicial_complex import FilteredSimplicialComplex


class AlphaFiltration():
    def __init__(self, points: list[tuple[float, ...]]) -> None:
        self.points = points

    @staticmethod
    def draw(points: list[tuple[float, ...]], fsc: FilteredSimplicialComplex, time: Optional[float] = None) -> None:
        if time is None:
            sc = fsc.sc
        else:
            sc = fsc.filtration(time)

        color = matplotlib.colors.ListedColormap("royalblue")
        voronoi = Voronoi(points)

        voronoi_plot_2d(voronoi, show_vertices=False, line_width=2, line_colors='red')

        for simplicial in sc.face_set:
            if len(simplicial) == 1:
                u = points[simplicial[0]]
                plt.plot(u[0], u[1], 'ko')

            if len(simplicial) == 2:
                u, v = points[simplicial[0]], points[simplicial[1]]
                plt.plot([u[0], v[0]], [u[1], v[1]], color='k', lw=2)

            if len(simplicial) == 3:
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
                j: utils.f_sq_distance(self.points[i], self.points[j])
                for j in range(n)
            }
            for i in range(n)
        }

        sc = FilteredSimplicialComplex((i,) for i in range(n))

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
            if utils.f_sq_distance(utils.median_point(x, y), z) < (dist[u][v] / 4):
                two_dims[(u, v)] = center

            if utils.f_sq_distance(utils.median_point(x, z), y) < (dist[u][w] / 4):
                two_dims[(u, w)] = center

            if utils.f_sq_distance(utils.median_point(y, z), x) < (dist[v][w] / 4):
                two_dims[(v, w)] = center

        for simpl, value in two_dims.items():
            sc.insert([simpl], value)

        for simpl, value in three_dims.items():
            sc.insert([simpl], value)

        return sc
