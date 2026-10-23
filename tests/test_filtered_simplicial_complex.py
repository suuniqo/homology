import unittest

from collections.abc import Iterable

from homology.filtered_simplicial_complex import FilteredSimplicialComplex
from homology.simplex import Simplex


class TestFilteredSimplicialComplex(unittest.TestCase):
    """Tests for inserting simplices with timestamps and reading filtrations."""

    @staticmethod
    def vertex_tuples(simplices: Iterable[Simplex]) -> set[tuple[int, ...]]:
        """Return the vertex tuples of the given simplices."""
        return {simplex.vertices for simplex in simplices}

    @staticmethod
    def filtered_complex() -> FilteredSimplicialComplex:
        """Return a filtered complex growing from an edge to a filled triangle."""
        sc = FilteredSimplicialComplex([])
        sc.insert([Simplex((0, 1))], 1.0)
        sc.insert([Simplex((1, 2)), Simplex((2, 3)), Simplex((2, 4))], 2.0)
        sc.insert([Simplex((3, 4))], 3.0)
        sc.insert([Simplex((2, 3, 4))], 4.0)
        return sc

    def test_face_set(self) -> None:
        """Every inserted simplex appears together with all of its faces."""
        sc = self.filtered_complex()

        self.assertEqual(
            self.vertex_tuples(sc.face_set),
            {
                (0,), (0, 1),
                (1,), (1, 2),
                (2,), (2, 3), (2, 3, 4), (2, 4),
                (3,), (3, 4),
                (4,),
            },
        )

    def test_threshold(self) -> None:
        """A simplex appears at the timestamp of the insertion that added it."""
        sc = self.filtered_complex()

        self.assertEqual(sc.threshold(Simplex((0, 1))), 1.0)
        self.assertEqual(sc.threshold(Simplex((3,))), 2.0)
        self.assertEqual(sc.threshold(Simplex((3, 4))), 3.0)
        self.assertEqual(sc.threshold(Simplex((2, 3, 4))), 4.0)
        self.assertIsNone(sc.threshold(Simplex((0, 4))))

    def test_threshold_values(self) -> None:
        """The threshold values are the insertion timestamps in increasing order."""
        sc = self.filtered_complex()

        self.assertEqual(sc.threshold_values(), [1.0, 2.0, 3.0, 4.0])

    def test_filtration(self) -> None:
        """Each filtration holds the simplices whose threshold is at most its time."""
        sc = self.filtered_complex()

        expected = {
            1.0: {(0,), (0, 1), (1,)},
            2.0: {
                (0,), (0, 1),
                (1,), (1, 2),
                (2,), (2, 3), (2, 4),
                (3,), (4,),
            },
            3.0: {
                (0,), (0, 1),
                (1,), (1, 2),
                (2,), (2, 3), (2, 4),
                (3,), (3, 4),
                (4,),
            },
            4.0: {
                (0,), (0, 1),
                (1,), (1, 2),
                (2,), (2, 3), (2, 3, 4), (2, 4),
                (3,), (3, 4),
                (4,),
            },
        }

        for time, faces in expected.items():
            with self.subTest(time=time):
                self.assertEqual(
                    self.vertex_tuples(sc.filtration(time).face_set),
                    faces,
                )

    def test_filtration_between_thresholds(self) -> None:
        """A time between two insertions returns the previous stage."""
        sc = self.filtered_complex()

        self.assertEqual(sc.filtration(0.0).face_set, set())
        self.assertEqual(
            self.vertex_tuples(sc.filtration(2.5).face_set),
            self.vertex_tuples(sc.filtration(2.0).face_set),
        )

    def test_filtration_order(self) -> None:
        """Simplices are ordered by timestamp, then by dimension and vertices."""
        sc = self.filtered_complex()

        self.assertEqual(
            [simplex.vertices for simplex in sc.filtration_order],
            [
                (0,), (1,), (0, 1),
                (2,), (3,), (4,), (1, 2), (2, 3), (2, 4),
                (3, 4),
                (2, 3, 4),
            ],
        )
