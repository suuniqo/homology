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

def circumradius(p: tuple[float, ...], q: tuple[float, ...], r: tuple[float, ...]) -> float:
    """Return the circumradius of the triangle through three points."""
    ax, ay = p[0] - r[0], p[1] - r[1]
    bx, by = q[0] - r[0], q[1] - r[1]

    cross = ax * by - ay * bx

    if cross == 0.0:
        raise ValueError("Points are collinear!")

    la  = math.hypot(ax, ay)
    lb  = math.hypot(bx, by)
    lab = math.hypot(ax - bx, ay - by)

    return la * lb * lab / (2.0 * abs(cross))

def midpoint(p: tuple[float, ...], q: tuple[float, ...]) -> tuple[float, ...]:
    """Return the midpoint between two points."""
    if len(p) != len(q):
        raise ValueError("Points have different dimensions!")

    return tuple((pi + qi) / 2 for pi, qi in zip(p, q))
