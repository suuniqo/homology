class SimplicialComplex:
    @staticmethod
    def _power_set(face_set: tuple[int, ...]) -> list[tuple[int, ...]]:
        n = len(face_set)

        res = []

        for i in range(1, 1 << n):
            res.append(tuple(
                face_set[j] for j in range(n) if i & (1 << j)
            ))
        
        return res

    def __init__(self, generator: list[tuple[int, ...]]) -> None:
        self.cardinality = 0
        self.simplicials = set() 

        for simplicial in generator:
            self.simplicials.update(self._power_set(simplicial))
            if len(simplicial) > self.cardinality:
                self.cardinality = len(simplicial)

    @property
    def dimension(self):
        return self.cardinality - 1
