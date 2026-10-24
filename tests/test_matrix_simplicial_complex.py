import unittest

import numpy as np

from homology.matrix_simplicial_complex import MatrixSimplicialComplex
from homology.simplex import Simplex
from homology.simplicial_complex import SimplicialComplex


class TestMatrixSimplicialComplex(unittest.TestCase):
    """Tests for boundary matrices and Betti numbers over GF(2)."""

    @staticmethod
    def build(*simplices: tuple[int, ...]) -> SimplicialComplex:
        """Build a simplicial complex from its maximal simplices."""
        return SimplicialComplex(Simplex(simplex) for simplex in simplices)

    @staticmethod
    def sphere() -> SimplicialComplex:
        """Return the boundary of a tetrahedron, a triangulated 2-sphere."""
        return TestMatrixSimplicialComplex.build(
            (0, 1, 2), (0, 1, 3), (0, 2, 3), (1, 2, 3),
        )

    @staticmethod
    def annulus() -> SimplicialComplex:
        """Return a triangulation of the closed annulus on vertices 1 to 6."""
        return TestMatrixSimplicialComplex.build(
            (1, 2, 4),
            (1, 3, 6),
            (1, 4, 6),
            (2, 3, 5),
            (2, 4, 5),
            (3, 5, 6),
        )

    @staticmethod
    def torus() -> SimplicialComplex:
        """Return a triangulation of the torus on vertices 1 to 9."""
        return TestMatrixSimplicialComplex.build(
            (1, 2, 4), (2, 4, 5), (2, 3, 5), (3, 5, 6), (1, 3, 6),
            (1, 4, 6), (4, 5, 7), (5, 7, 8), (5, 6, 8), (6, 8, 9),
            (4, 6, 9), (4, 7, 9), (1, 7, 8), (1, 2, 8), (2, 8, 9),
            (2, 3, 9), (3, 7, 9), (1, 3, 7),
        )

    @staticmethod
    def projective_plane() -> SimplicialComplex:
        """Return a triangulation of the projective plane on vertices 1 to 6."""
        return TestMatrixSimplicialComplex.build(
            (1, 2, 6), (2, 3, 4), (1, 3, 4), (1, 2, 5), (2, 3, 5),
            (1, 3, 6), (2, 4, 6), (1, 4, 5), (3, 5, 6), (4, 5, 6),
        )

    @staticmethod
    def examples() -> list[tuple[str, SimplicialComplex]]:
        """Return the standard test complexes with their names."""
        return [
            ("sphere", TestMatrixSimplicialComplex.sphere()),
            ("annulus", TestMatrixSimplicialComplex.annulus()),
            ("torus", TestMatrixSimplicialComplex.torus()),
            ("projective plane", TestMatrixSimplicialComplex.projective_plane()),
        ]

    @staticmethod
    def betti_numbers(sc: SimplicialComplex) -> list[int]:
        """Return all Betti numbers of the given complex."""
        msc = MatrixSimplicialComplex(sc)
        return [msc.betti_number(k) for k in range(sc.dim + 1)]

    @staticmethod
    def gf2_rank(mat: np.ndarray) -> int:
        """Return the rank of a binary matrix over GF(2)."""
        rows, cols = mat.shape
        reduced = mat.copy() % 2
        rank = 0

        for col in range(cols):
            pivot = next(
                (row for row in range(rank, rows) if reduced[row, col]),
                None,
            )

            if pivot is None:
                continue

            reduced[[rank, pivot]] = reduced[[pivot, rank]]

            for row in range(rows):
                if row != rank and reduced[row, col]:
                    reduced[row] ^= reduced[rank]

            rank += 1

            if rank == rows:
                break

        return rank

    def test_sphere_betti_numbers(self) -> None:
        """A 2-sphere has Betti numbers 1, 0, 1."""
        self.assertEqual(self.betti_numbers(self.sphere()), [1, 0, 1])

    def test_annulus_betti_numbers(self) -> None:
        """An annulus has Betti numbers 1, 1, 0."""
        self.assertEqual(self.betti_numbers(self.annulus()), [1, 1, 0])

    def test_torus_betti_numbers(self) -> None:
        """A torus has Betti numbers 1, 2, 1."""
        self.assertEqual(self.betti_numbers(self.torus()), [1, 2, 1])

    def test_projective_plane_betti_numbers(self) -> None:
        """The projective plane has mod-2 Betti numbers 1, 1, 1."""
        self.assertEqual(
            self.betti_numbers(self.projective_plane()),
            [1, 1, 1],
        )

    def test_boundary_squared_is_zero(self) -> None:
        """The composition of consecutive boundary maps is zero mod 2."""
        for name, sc in self.examples():
            msc = MatrixSimplicialComplex(sc)

            for dim in range(1, sc.dim + 1):
                first = msc.boundary_matrix(dim).astype(np.int64)
                second = msc.boundary_matrix(dim + 1).astype(np.int64)

                with self.subTest(complex=name, dim=dim):
                    self.assertFalse(np.any((first @ second) % 2))

    def test_rank_matches_reference(self) -> None:
        """Boundary ranks agree with a direct GF(2) rank computation."""
        for name, sc in self.examples():
            msc = MatrixSimplicialComplex(sc)

            for dim in range(sc.dim + 2):
                with self.subTest(complex=name, dim=dim):
                    self.assertEqual(
                        msc.rank_boundary_matrix(dim),
                        self.gf2_rank(msc.boundary_matrix(dim)),
                    )

    def test_rank_does_not_change_boundary_matrix(self) -> None:
        """Computing a rank leaves the cached boundary matrix unchanged."""
        for name, sc in self.examples():
            msc = MatrixSimplicialComplex(sc)

            for dim in range(sc.dim + 2):
                before = msc.boundary_matrix(dim).copy()
                msc.rank_boundary_matrix(dim)

                with self.subTest(complex=name, dim=dim):
                    self.assertTrue(
                        np.array_equal(msc.boundary_matrix(dim), before),
                    )

    def test_smith_form_is_identity_plus_zero(self) -> None:
        """The GF(2) Smith form is the identity of size rank plus zeros."""
        for name, sc in self.examples():
            msc = MatrixSimplicialComplex(sc)

            for dim in range(sc.dim + 2):
                expected = np.zeros(
                    msc.boundary_matrix(dim).shape,
                    dtype=np.uint8,
                )

                for k in range(msc.rank_boundary_matrix(dim)):
                    expected[k, k] = 1

                with self.subTest(complex=name, dim=dim):
                    self.assertTrue(
                        np.array_equal(
                            msc.smith_boundary_matrix(dim),
                            expected,
                        ),
                    )

    def test_n_faces_bounds(self) -> None:
        """Only dimensions from -1 to the dimension of the complex are valid."""
        sc = self.sphere()
        msc = MatrixSimplicialComplex(sc)

        self.assertEqual(msc.n_faces(-1), [])
        self.assertEqual(msc.n_faces(sc.dim + 1), [])

        with self.assertRaises(ValueError):
            msc.n_faces(-2)

    def test_n_faces_are_sorted(self) -> None:
        """Faces of each dimension are ordered by their vertex tuples."""
        sc = self.torus()
        msc = MatrixSimplicialComplex(sc)

        for dim in range(sc.dim + 1):
            vertices = [simplex.vertices for simplex in msc.n_faces(dim)]

            with self.subTest(dim=dim):
                self.assertEqual(vertices, sorted(vertices))

    def test_negative_betti_number_raises(self) -> None:
        """Betti numbers are only defined for non-negative dimensions."""
        msc = MatrixSimplicialComplex(self.sphere())

        with self.assertRaises(ValueError):
            msc.betti_number(-1)
