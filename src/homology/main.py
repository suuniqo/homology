import random
import time

from homology.factory.simplicial_complex_factory import SimplicialComplexFactory
from homology.filtrations.alpha_filtration import AlphaFiltration
from homology.filtrations.vietoris_rips_filtration import VietorisRipsFiltration
from homology.matrix_simplicial_complex import MatrixSimplicialComplex
from homology.simplex import Simplex
from homology.simplicial_complex import SimplicialComplex

def main():
    alpha1 = SimplicialComplexFactory.alpha_complex_example(0.00)
    alpha2 = SimplicialComplexFactory.alpha_complex_example(0.14)

    mat1 = MatrixSimplicialComplex(alpha1)
    mat2 = MatrixSimplicialComplex(alpha2)

    print(f"[incremental] alpha1: {alpha1.betti_planar()}")
    print(f"[boundarymat] alpha1: {(mat1.betti_number(0), mat1.betti_number(1))}")

    print(f"[incremental] alpha2: {alpha2.betti_planar()}")
    print(f"[boundarymat] alpha2: {(mat2.betti_number(0), mat2.betti_number(1))}")

if __name__ == "__main__":
    main()
