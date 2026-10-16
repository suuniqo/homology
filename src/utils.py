import math

def power_set(simplicial: tuple[int, ...]) -> list[tuple[int, ...]]:
    n = len(simplicial)

    res = []

    for i in range(1, 1 << n):
        res.append(tuple(
            simplicial[j] for j in range(n) if i & (1 << j)
        ))

    return res

def sq_distance(p: tuple[int, ...], q: tuple[int, ...]) -> float:
    if len(p) != len(q):
        raise ValueError("Points have different dimensions!")
    
    return sum((pk - qk)**2 for pk, qk in zip(p, q))

def f_sq_distance(p: tuple[float, ...], q: tuple[float, ...]) -> float:
    if len(p) != len(q):
        raise ValueError("Points have different dimensions!")
    
    return sum((pk - qk)**2 for pk, qk in zip(p, q))

def distance_to_center(p: tuple[float, ...], q: tuple[float, ...], r: tuple[float, ...]) -> float:
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
    if len(p) != len(q):
        raise ValueError("Points have different dimensions!")

    return tuple((pi + qi) / 2 for pi, qi in zip(p, q))
