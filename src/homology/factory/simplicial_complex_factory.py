from homology.simplex import Simplex
from homology.simplicial_complex import SimplicialComplex
from homology.filtrations.alpha_filtration import AlphaFiltration

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

    @staticmethod
    def double_torus() -> SimplicialComplex:
        return SimplicialComplex(map(Simplex, [
                (0, 1, 3), (0, 1, 5), (0, 2, 3), (0, 2, 6), (0, 4, 5), (0, 4, 9), 
                (0, 6, 8), (0, 7, 8), (0, 7, 9), (1, 2, 4), (1, 2, 6), (1, 3, 4), 
                (1, 5, 6), (2, 3, 5), (2, 4, 5), (3, 4, 9), (3, 5, 8), (3, 6, 7), 
                (3, 6, 9), (3, 7, 8), (5, 6, 7), (5, 7, 9), (5, 8, 9), (6, 8, 9),
            ]
        ))

    @staticmethod
    def dunce_hat() -> SimplicialComplex:
        return SimplicialComplex(map(Simplex, [
                (1,3,5), (1,5,6), (1,3,6), (2,4,5), 
                (4,5,6), (4,6,8), (6,7,8), (3,6,7), 
                (3,2,7), (1,2,7), (1,7,8), (1,2,4), 
                (1,3,4), (3,4,8), (2,3,8), (1,2,8)
            ]
        ))

    @staticmethod
    def simplicial_complex_example() -> SimplicialComplex:
        return SimplicialComplex(map(Simplex, [
                (0, 1),
                (1, 2, 3, 4),
                (4, 5), (5, 6), (4, 6),
                (6, 7, 8),
                (8, 9)
            ]
        ))

    @staticmethod
    def alpha_complex_example_1() -> SimplicialComplex:
        points = [
            (0.38021546727456423, 0.46419202339598786), (0.7951628297672293, 0.49263630135869474), 
            (0.566623772375203, 0.038325621649018426), (0.3369306814864865, 0.7103735061134965), 
            (0.08272837815822842, 0.2263273314352896), (0.5180166301873989, 0.6271769943824689), 
            (0.33691411899985035, 0.8402045183219995), (0.33244488399729255, 0.4524636520475205), 
            (0.11778991601260325, 0.6657734204021165), (0.9384303415747769, 0.2313873874340855)
        ]
        r = 0.20

        alpha_filtration = AlphaFiltration(points).build()

        return alpha_filtration.filtration(r)

    @staticmethod
    def alpha_complex_example_2() -> SimplicialComplex:
        points = [
            (0.38021546727456423, 0.46419202339598786), (0.7951628297672293, 0.49263630135869474), 
            (0.566623772375203, 0.038325621649018426), (0.3369306814864865, 0.7103735061134965), 
            (0.08272837815822842, 0.2263273314352896), (0.5180166301873989, 0.6271769943824689), 
            (0.33691411899985035, 0.8402045183219995), (0.33244488399729255, 0.4524636520475205), 
            (0.11778991601260325, 0.6657734204021165), (0.9384303415747769, 0.2313873874340855)
        ]
        r = 1.00

        alpha_filtration = AlphaFiltration(points).build()

        return alpha_filtration.filtration(r)

