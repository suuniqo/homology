import sys
import unittest

from collections.abc import Iterable

from homology.simplex import Simplex
from homology.simplicial_complex import SimplicialComplex


class TestSimplicialComplex(unittest.TestCase):
    """Tests for building complexes and querying their simplices and topology."""

    @staticmethod
    def vertex_tuples(simplices: Iterable[Simplex]) -> set[tuple[int, ...]]:
        """Return the vertex tuples of the given simplices."""
        return {simplex.vertices for simplex in simplices}

    @staticmethod
    def build(*simplices: tuple[int, ...]) -> SimplicialComplex:
        """Build a simplicial complex from its maximal simplices."""
        return SimplicialComplex(Simplex(simplex) for simplex in simplices)

    @staticmethod
    def tetrahedron() -> SimplicialComplex:
        """Return the 3-simplex on vertices 0 to 3."""
        return TestSimplicialComplex.build((0, 1, 2, 3))

    @staticmethod
    def tetrahedron_boundary() -> SimplicialComplex:
        """Return the boundary of the tetrahedron, a triangulated 2-sphere."""
        return SimplicialComplex(TestSimplicialComplex.tetrahedron().skeleton(2))

    @staticmethod
    def mixed_complex() -> SimplicialComplex:
        """Return a complex combining an edge, a 3-simplex, a triangle and two edges."""
        return TestSimplicialComplex.build(
            (0, 1),
            (1, 2, 3, 4),
            (4, 5),
            (5, 6),
            (4, 6),
            (6, 7, 8),
            (8, 9),
        )

    @staticmethod
    def annulus() -> SimplicialComplex:
        """Return a triangulation of the closed annulus on vertices 1 to 6."""
        return TestSimplicialComplex.build(
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
        return TestSimplicialComplex.build(
            (1, 2, 4), (2, 4, 5), (2, 3, 5), (3, 5, 6), (1, 3, 6),
            (1, 4, 6), (4, 5, 7), (5, 7, 8), (5, 6, 8), (6, 8, 9),
            (4, 6, 9), (4, 7, 9), (1, 7, 8), (1, 2, 8), (2, 8, 9),
            (2, 3, 9), (3, 7, 9), (1, 3, 7),
        )

    @staticmethod
    def projective_plane() -> SimplicialComplex:
        """Return a triangulation of the projective plane on vertices 1 to 6."""
        return TestSimplicialComplex.build(
            (1, 2, 6), (2, 3, 4), (1, 3, 4), (1, 2, 5), (2, 3, 5),
            (1, 3, 6), (2, 4, 6), (1, 4, 5), (3, 5, 6), (4, 5, 6),
        )

    @staticmethod
    def triangle_with_tail() -> SimplicialComplex:
        """Return a triangle with two edges attached at vertex 2."""
        return TestSimplicialComplex.build((0, 1, 2), (2, 3), (3, 4))

    @staticmethod
    def isolated_vertices_and_3_simplex() -> SimplicialComplex:
        """Return isolated vertices, an edge, a triangle and a 3-simplex."""
        return TestSimplicialComplex.build(
            (0,), (1,), (2, 3), (4, 5), (5, 6), (4, 6), (6, 7, 8, 9),
        )

    def test_3_simplex(self) -> None:
        """A 3-simplex contains every non-empty subset of its four vertices."""
        sc = self.tetrahedron()

        self.assertEqual(
            self.vertex_tuples(sc.face_set),
            {
                (0,), (0, 1), (0, 1, 2), (0, 1, 2, 3), (0, 1, 3),
                (0, 2), (0, 2, 3), (0, 3),
                (1,), (1, 2), (1, 2, 3), (1, 3),
                (2,), (2, 3),
                (3,),
            },
        )
        self.assertEqual(sc.dim, 3)
        self.assertEqual(sc.euler_characteristic, 1)
        self.assertEqual(sc.connected_components(), 1)

    def test_3_simplex_star_and_link(self) -> None:
        """The star of an edge is its cofaces; the link is the star without it."""
        sc = self.tetrahedron()

        self.assertEqual(
            self.vertex_tuples(sc.st(Simplex((0, 1)))),
            {(0, 1), (0, 1, 2), (0, 1, 2, 3), (0, 1, 3)},
        )
        self.assertEqual(
            self.vertex_tuples(sc.lk(Simplex((0, 1)))),
            {(2,), (2, 3), (3,)},
        )

    def test_tetrahedron_boundary(self) -> None:
        """Removing the 3-simplex leaves the boundary of the tetrahedron."""
        sc = self.tetrahedron_boundary()

        self.assertEqual(
            self.vertex_tuples(sc.face_set),
            {
                (0,), (0, 1), (0, 1, 2), (0, 1, 3),
                (0, 2), (0, 2, 3), (0, 3),
                (1,), (1, 2), (1, 2, 3), (1, 3),
                (2,), (2, 3),
                (3,),
            },
        )
        self.assertEqual(sc.dim, 2)
        self.assertEqual(sc.euler_characteristic, 2)
        self.assertEqual(sc.connected_components(), 1)

    def test_tetrahedron_boundary_star_and_link(self) -> None:
        """The star of a vertex in the tetrahedron boundary is its open cone."""
        sc = self.tetrahedron_boundary()

        self.assertEqual(
            self.vertex_tuples(sc.st(Simplex((0,)))),
            {(0,), (0, 1), (0, 1, 2), (0, 1, 3), (0, 2), (0, 2, 3), (0, 3)},
        )
        self.assertEqual(
            self.vertex_tuples(sc.lk(Simplex((0,)))),
            {(1,), (1, 2), (1, 3), (2,), (2, 3), (3,)},
        )

    def test_mixed_complex(self) -> None:
        """A complex assembled from several maximal simplices of different dimensions."""
        sc = self.mixed_complex()

        self.assertEqual(
            self.vertex_tuples(sc.face_set),
            {
                (0,), (0, 1),
                (1,), (1, 2), (1, 2, 3), (1, 2, 3, 4), (1, 2, 4),
                (1, 3), (1, 3, 4), (1, 4),
                (2,), (2, 3), (2, 3, 4), (2, 4),
                (3,), (3, 4),
                (4,), (4, 5), (4, 6),
                (5,), (5, 6),
                (6,), (6, 7), (6, 7, 8), (6, 8),
                (7,), (7, 8),
                (8,), (8, 9),
                (9,),
            },
        )
        self.assertEqual(sc.dim, 3)
        self.assertEqual(sc.euler_characteristic, 0)
        self.assertEqual(sc.connected_components(), 1)

    def test_mixed_complex_skeleton(self) -> None:
        """The 1-skeleton keeps only vertices and edges."""
        sc = self.mixed_complex()

        self.assertEqual(
            self.vertex_tuples(sc.skeleton(1)),
            {
                (0,), (0, 1),
                (1,), (1, 2), (1, 3), (1, 4),
                (2,), (2, 3), (2, 4),
                (3,), (3, 4),
                (4,), (4, 5), (4, 6),
                (5,), (5, 6),
                (6,), (6, 7), (6, 8),
                (7,), (7, 8),
                (8,), (8, 9),
                (9,),
            },
        )

    def test_mixed_complex_star_and_link(self) -> None:
        """Star and link of the shared vertex 4."""
        sc = self.mixed_complex()

        self.assertEqual(
            self.vertex_tuples(sc.st(Simplex((4,)))),
            {
                (1, 2, 3, 4), (1, 2, 4), (1, 3, 4), (1, 4),
                (2, 3, 4), (2, 4), (3, 4),
                (4,), (4, 5), (4, 6),
            },
        )
        self.assertEqual(
            self.vertex_tuples(sc.lk(Simplex((4,)))),
            {(1,), (1, 2), (1, 2, 3), (1, 3), (2,), (2, 3), (3,), (5,), (6,)},
        )

    def test_mixed_complex_skeleton_euler_characteristic(self) -> None:
        """The 1-skeleton of the mixed complex has Euler characteristic -4."""
        sc = SimplicialComplex(self.mixed_complex().skeleton(1))

        self.assertEqual(sc.euler_characteristic, -4)

    def test_triangle_with_tail(self) -> None:
        """Checks the faces, dimension, Euler characteristic and connectedness."""
        sc = self.triangle_with_tail()

        self.assertEqual(
            self.vertex_tuples(sc.face_set),
            {
                (0,), (0, 1), (0, 1, 2), (0, 2),
                (1,), (1, 2),
                (2,), (2, 3),
                (3,), (3, 4),
                (4,),
            },
        )
        self.assertEqual(sc.dim, 2)
        self.assertEqual(sc.euler_characteristic, 1)
        self.assertEqual(sc.connected_components(), 1)

    def test_triangle_with_tail_star_and_link(self) -> None:
        """Star and link of the vertex where the tail is attached."""
        sc = self.triangle_with_tail()

        self.assertEqual(
            self.vertex_tuples(sc.st(Simplex((2,)))),
            {(0, 1, 2), (0, 2), (1, 2), (2,), (2, 3)},
        )
        self.assertEqual(
            self.vertex_tuples(sc.lk(Simplex((2,)))),
            {(0,), (0, 1), (1,), (3,)},
        )

    def test_annulus(self) -> None:
        """Checks the faces, dimension, Euler characteristic and connectedness."""
        sc = self.annulus()

        self.assertEqual(
            self.vertex_tuples(sc.face_set),
            {
                (1,), (1, 2), (1, 2, 4), (1, 3), (1, 3, 6),
                (1, 4), (1, 4, 6), (1, 6),
                (2,), (2, 3), (2, 3, 5), (2, 4), (2, 4, 5), (2, 5),
                (3,), (3, 5), (3, 5, 6), (3, 6),
                (4,), (4, 5), (4, 6),
                (5,), (5, 6),
                (6,),
            },
        )
        self.assertEqual(sc.dim, 2)
        self.assertEqual(sc.euler_characteristic, 0)
        self.assertEqual(sc.connected_components(), 1)

    def test_annulus_skeleton(self) -> None:
        """The 1-skeleton of the annulus keeps only vertices and edges."""
        sc = self.annulus()

        self.assertEqual(
            self.vertex_tuples(sc.skeleton(1)),
            {
                (1,), (1, 2), (1, 3), (1, 4), (1, 6),
                (2,), (2, 3), (2, 4), (2, 5),
                (3,), (3, 5), (3, 6),
                (4,), (4, 5), (4, 6),
                (5,), (5, 6),
                (6,),
            },
        )

    def test_annulus_star_and_link(self) -> None:
        """Star and link of the interior edge (1, 4)."""
        sc = self.annulus()

        self.assertEqual(
            self.vertex_tuples(sc.st(Simplex((1, 4)))),
            {(1, 2, 4), (1, 4), (1, 4, 6)},
        )
        self.assertEqual(
            self.vertex_tuples(sc.lk(Simplex((1, 4)))),
            {(2,), (6,)},
        )

    def test_annulus_skeleton_euler_characteristic(self) -> None:
        """The 1-skeleton of the annulus has Euler characteristic -6."""
        sc = SimplicialComplex(self.annulus().skeleton(1))

        self.assertEqual(sc.euler_characteristic, -6)

    def test_torus(self) -> None:
        """Checks the dimension, vertices, edges, Euler characteristic and connectedness."""
        sc = self.torus()

        self.assertEqual(sc.dim, 2)
        self.assertEqual(
            self.vertex_tuples(sc.n_faces(0)),
            {(vertex,) for vertex in range(1, 10)},
        )
        self.assertEqual(
            self.vertex_tuples(sc.n_faces(1)),
            {
                (1, 2), (1, 3), (1, 4), (1, 6), (1, 7), (1, 8),
                (2, 3), (2, 4), (2, 5), (2, 8), (2, 9),
                (3, 5), (3, 6), (3, 7), (3, 9),
                (4, 5), (4, 6), (4, 7), (4, 9),
                (5, 6), (5, 7), (5, 8),
                (6, 8), (6, 9),
                (7, 8), (7, 9),
                (8, 9),
            },
        )
        self.assertEqual(sc.euler_characteristic, 0)
        self.assertEqual(sc.connected_components(), 1)

    def test_torus_star_and_link(self) -> None:
        """Star and link of vertex 1 in the torus."""
        sc = self.torus()

        self.assertEqual(
            self.vertex_tuples(sc.st(Simplex((1,)))),
            {
                (1,), (1, 2), (1, 2, 4), (1, 2, 8),
                (1, 3), (1, 3, 6), (1, 3, 7),
                (1, 4), (1, 4, 6),
                (1, 6), (1, 7), (1, 7, 8), (1, 8),
            },
        )
        self.assertEqual(
            self.vertex_tuples(sc.lk(Simplex((1,)))),
            {
                (2,), (2, 4), (2, 8),
                (3,), (3, 6), (3, 7),
                (4,), (4, 6),
                (6,), (7,), (7, 8), (8,),
            },
        )

    def test_torus_skeleton_euler_characteristic(self) -> None:
        """The 1-skeleton of the torus has Euler characteristic -18."""
        sc = SimplicialComplex(self.torus().skeleton(1))

        self.assertEqual(sc.euler_characteristic, -18)

    def test_projective_plane(self) -> None:
        """Checks the dimension, edges, Euler characteristic and connectedness."""
        sc = self.projective_plane()

        self.assertEqual(sc.dim, 2)
        self.assertEqual(
            self.vertex_tuples(sc.n_faces(1)),
            {
                (1, 2), (1, 3), (1, 4), (1, 5), (1, 6),
                (2, 3), (2, 4), (2, 5), (2, 6),
                (3, 4), (3, 5), (3, 6),
                (4, 5), (4, 6),
                (5, 6),
            },
        )
        self.assertEqual(sc.euler_characteristic, 1)
        self.assertEqual(sc.connected_components(), 1)

    def test_projective_plane_star_and_link(self) -> None:
        """Star and link of vertex 1 in the projective plane."""
        sc = self.projective_plane()

        self.assertEqual(
            self.vertex_tuples(sc.st(Simplex((1,)))),
            {
                (1,), (1, 2), (1, 2, 5), (1, 2, 6),
                (1, 3), (1, 3, 4), (1, 3, 6),
                (1, 4), (1, 4, 5),
                (1, 5), (1, 6),
            },
        )
        self.assertEqual(
            self.vertex_tuples(sc.lk(Simplex((1,)))),
            {
                (2,), (2, 5), (2, 6),
                (3,), (3, 4), (3, 6),
                (4,), (4, 5),
                (5,), (6,),
            },
        )

    def test_projective_plane_skeleton_euler_characteristic(self) -> None:
        """The 1-skeleton of the projective plane has Euler characteristic -9."""
        sc = SimplicialComplex(self.projective_plane().skeleton(1))

        self.assertEqual(sc.euler_characteristic, -9)

    def test_isolated_vertices_and_3_simplex(self) -> None:
        """Checks faces by dimension, Euler characteristic and four components."""
        sc = self.isolated_vertices_and_3_simplex()

        self.assertEqual(
            self.vertex_tuples(sc.face_set),
            {
                (0,), (1,),
                (2,), (2, 3), (3,),
                (4,), (4, 5), (4, 6),
                (5,), (5, 6),
                (6,), (6, 7), (6, 7, 8), (6, 7, 8, 9), (6, 7, 9),
                (6, 8), (6, 8, 9), (6, 9),
                (7,), (7, 8), (7, 8, 9), (7, 9),
                (8,), (8, 9),
                (9,),
            },
        )
        self.assertEqual(sc.dim, 3)
        self.assertEqual(
            self.vertex_tuples(sc.n_faces(0)),
            {(vertex,) for vertex in range(10)},
        )
        self.assertEqual(
            self.vertex_tuples(sc.n_faces(2)),
            {(6, 7, 8), (6, 7, 9), (6, 8, 9), (7, 8, 9)},
        )
        self.assertEqual(self.vertex_tuples(sc.n_faces(3)), {(6, 7, 8, 9)})
        self.assertEqual(sc.euler_characteristic, 3)
        self.assertEqual(sc.connected_components(), 4)

    def test_isolated_vertices_and_3_simplex_star_and_link(self) -> None:
        """Star and link of vertex 6, which belongs to the 3-simplex."""
        sc = self.isolated_vertices_and_3_simplex()

        self.assertEqual(
            self.vertex_tuples(sc.st(Simplex((6,)))),
            {
                (4, 6), (5, 6), (6,), (6, 7), (6, 7, 8), (6, 7, 8, 9),
                (6, 7, 9), (6, 8), (6, 8, 9), (6, 9),
            },
        )
        self.assertEqual(
            self.vertex_tuples(sc.lk(Simplex((6,)))),
            {
                (4,), (5,),
                (7,), (7, 8), (7, 8, 9), (7, 9),
                (8,), (8, 9),
                (9,),
            },
        )
