from scipy.spatial import Delaunay
from filtered_simplicial_complex import FilteredSimplicialComplex
import utils
import math

def alpha_filtration(points: list[tuple[float, ...]]) -> FilteredSimplicialComplex:
    # The FilteredSimplicialComplex doesn't support updating the filtration value
    three_dims = {}
    two_dims = {}

    n = len(points)
    dist = {
        i : {
            j: utils.f_sq_distance(points[i], points[j])
            for j in range(n)
        }
        for i in range(n)
    }

    sc = FilteredSimplicialComplex((i,) for i in range(n))

    # Generate the Delaunay complex
    dl = Delaunay(points)

    for [u, v, w] in dl.simplices:
        # Assume fist case for the three edges
        if (u, v) not in two_dims:
            two_dims[(u, v)] = math.sqrt(dist[u][v]) / 2
        if (u, w) not in two_dims:
            two_dims[(u, w)] = math.sqrt(dist[u][w]) / 2
        if (v, w) not in two_dims:
            two_dims[(v, w)] = math.sqrt(dist[v][w]) / 2

        x, y, z = points[u], points[v], points[w]

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
