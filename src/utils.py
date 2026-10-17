import math

def power_set(elems: tuple[int, ...]) -> list[tuple[int, ...]]:
    """Return a list of all subsets as tuples."""
    n = len(elems)

    res = []

    for i in range(1, 1 << n):
        res.append(tuple(
            elems[j] for j in range(n) if i & (1 << j)
        ))

    return res

def sq_distance(p: tuple[float, ...], q: tuple[float, ...]) -> float:
    """Return the squared Euclidean distance between two points."""
    if len(p) != len(q):
        raise ValueError("Points have different dimensions!")
    
    return sum((pk - qk)**2 for pk, qk in zip(p, q))

def distance_to_center(p: tuple[float, ...], q: tuple[float, ...], r: tuple[float, ...]) -> float:
    """Return the circumradius from three points using Heron's formula."""
    if len(p) != len(q) or len(q) != len(r):
        raise ValueError("Points have different dimensions!")

    # Lengths of sides
    a = math.dist(p, q)
    b = math.dist(q, r)
    c = math.dist(r, p)
    
    # Semi-perimeter
    s = (a + b + c) / 2
    
    # Area using Heron's Formula
    area_sq = s * (s - a) * (s - b) * (s - c)

    if area_sq <= 0:
        raise ValueError("Points are collinear.")

    area = math.sqrt(area_sq)
    
    # Circumradius
    radius = (a * b * c) / (4 * area)
    return radius

def median_point(p: tuple[float, ...], q: tuple[float, ...]) -> tuple[float, ...]:
    """Return the midpoint between two points."""
    if len(p) != len(q):
        raise ValueError("Points have different dimensions!")

    return tuple((pi + qi) / 2 for pi, qi in zip(p, q))
