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
