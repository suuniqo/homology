def power_set(simplicial: tuple[int, ...]) -> list[tuple[int, ...]]:
    n = len(simplicial)

    res = []

    for i in range(1, 1 << n):
        res.append(tuple(
            simplicial[j] for j in range(n) if i & (1 << j)
        ))

    return res

