from homology.simplex import Simplex
from homology.simplicial_complex import SimplicialComplex


class SimplicialComplexFactory:
    @staticmethod
    def n_simplicial(n: int) -> SimplicialComplex:
        return SimplicialComplex([Simplex(tuple(range(n)))])

    @staticmethod
    def torus() -> SimplicialComplex:
        return SimplicialComplex(map(Simplex, [
                (1,2,4), (2,4,5), (2,3,5), (3,5,6), (1,3,6), (1,4,6),
                (4,5,7), (5,7,8), (5,6,8), (6,8,9), (4,6,9), (4,7,9), 
                (1,7,8), (1,2,8), (2,8,9), (2,3,9), (3,7,9), (1,3,7) 
            ]
        ))

    @staticmethod
    def torus_minimal() -> SimplicialComplex:
        return SimplicialComplex(map(Simplex, [
                (1,3,7), (1,2,3), (2,3,6), (3,4,6), (4,6,7), (1,6,7), (2,5,6), 
                (1,5,6), (2,5,7), (3,5,7), (1,4,5), (3,4,5), (1,2,4), (2,4,7) 
            ]
        ))

    @staticmethod
    def klein_bottle() -> SimplicialComplex:
        return SimplicialComplex(map(Simplex, [
                (1,2,4), (2,4,5), (2,3,5), (3,5,6), (1,3,6), (1,7,6),
                (4,5,7), (5,7,8), (5,6,8), (6,8,9), (4,6,9), (4,7,9), 
                (1,7,8), (1,2,8), (2,8,9), (2,3,9), (3,7,9), (1,4,3) 
            ]
        ))

    @staticmethod
    def ring() -> SimplicialComplex:
        return SimplicialComplex(map(Simplex, [
                (1,2,4),(1,3,6),(1,4,6),
                (2,3,5),(2,4,5),(3,5,6)
            ]
        ))

    @staticmethod
    def projective_plane() -> SimplicialComplex:
        return SimplicialComplex(map(Simplex, [
                (1,2,6), (2,3,4), (1,3,4), (1,2,5), (2,3,5), 
                (1,3,6), (2,4,6), (1,4,5), (3,5,6), (4,5,6)
            ]
        ))

    # @staticmethod
    # def double_torus() -> SimplicialComplex:
    #     return SimplicialComplex(map(Simplex, [
    #             ()
    #         ]
    #     ))

    @staticmethod
    def transparency_four() -> SimplicialComplex:
        return SimplicialComplex(map(Simplex, [
                (0, 1),
                (1, 2, 3, 4),
                (4, 5), (5, 6), (4, 6),
                (6, 7, 8),
                (8, 9)
            ]
        ))

