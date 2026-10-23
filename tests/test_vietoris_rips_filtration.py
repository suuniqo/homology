import itertools
import math
import unittest

from collections.abc import Iterable

import pytest

from homology.filtered_simplicial_complex import FilteredSimplicialComplex
from homology.filtrations.vietoris_rips_filtration import VietorisRipsFiltration
from homology.simplex import Simplex


class TestVietorisRipsFiltration(unittest.TestCase):
    """Tests for building Vietoris-Rips filtrations from planar point clouds."""

    @staticmethod
    def vertices(simplices: Iterable[Simplex]) -> list[tuple[int, ...]]:
        """Return the vertex tuples of the given simplices, in order."""
        return [
            tuple(int(vertex) for vertex in simplex.vertices)
            for simplex in simplices
        ]

    @staticmethod
    def vertex_tuples(simplices: Iterable[Simplex]) -> set[tuple[int, ...]]:
        """Return the vertex tuples of the given simplices."""
        return {
            tuple(int(vertex) for vertex in simplex.vertices)
            for simplex in simplices
        }

    @staticmethod
    def build(points: list[tuple[float, float]]) -> FilteredSimplicialComplex:
        """Build the Vietoris-Rips filtration of the given point cloud."""
        return VietorisRipsFiltration(points).build()

    @staticmethod
    def threshold(built: FilteredSimplicialComplex, simplex: Simplex) -> float:
        """Return the threshold of a simplex, failing if it is missing."""
        value = built.threshold(simplex)

        if value is None:
            raise AssertionError(f"missing threshold for {simplex.vertices}")

        return value

    @staticmethod
    def points() -> list[tuple[float, float]]:
        """Return the point cloud."""
        return [
            (0.38021546727456423, 0.46419202339598786),
            (0.7951628297672293, 0.49263630135869474),
            (0.566623772375203, 0.038325621649018426),
            (0.3369306814864865, 0.7103735061134965),
            (0.08272837815822842, 0.2263273314352896),
            (0.5180166301873989, 0.6271769943824689),
            (0.33691411899985035, 0.8402045183219995),
            (0.33244488399729255, 0.4524636520475205),
            (0.11778991601260325, 0.6657734204021165),
            (0.9384303415747769, 0.2313873874340855),
        ]

    def test_threshold_values(self) -> None:
        """Checks the thresholds at which new simplices appear."""
        built = self.build(self.points())

        self.assertEqual(
            built.threshold_values(),
            pytest.approx([
                0.0, 0.024594630110749274, 0.06491550663246884, 0.09964158316325628,
                0.1067160499498478, 0.11181663867459748, 0.12497889333174499,
                0.12743785247513206, 0.12897443080262758, 0.13980240119025444,
                0.14003715958303004, 0.14897699064479192, 0.151309131049649,
                0.15403831830169779, 0.16545560550649724, 0.16844581383081997,
                0.1892487801168689, 0.19044564833074332, 0.19388331119567223,
                0.20104172877828352, 0.20796056752930286, 0.20947134070559964,
                0.22042128784724613, 0.23222927199764715, 0.23243829737556373,
                0.23788130442736796, 0.2536662137792591, 0.25427755231828075,
                0.259566655903143, 0.2733676600468666, 0.2875741410328021,
                0.2887027457831261, 0.2954270609819514, 0.29587003677268414,
                0.3024077728892547, 0.32252639022676216, 0.3322106227332085,
                0.34957492983589655, 0.35510817894523095, 0.3802904532397188,
                0.38445726127031843, 0.3857274202002728, 0.41706602888011096,
                0.4278584620998067, 0.4279252460662376, 0.4642579923126173,
            ]),
        )

    def test_filtration_order(self) -> None:
        """Simplices are ordered by threshold, then dimension and vertices."""
        built = self.build(self.points())
        order = built.filtration_order

        self.assertEqual(len(order), 1023)
        self.assertEqual(len(set(order)), 1023)
        expected_prefix = [
            (0,), (1,), (2,), (3,), (4,), (5,), (6,), (7,), (8,), (9,), (0, 7), (3, 6),
            (3, 5), (0, 5), (3, 8), (0, 3), (0, 3, 5), (5, 7), (0, 5, 7), (3, 7),
            (0, 3, 7), (3, 5, 7), (0, 3, 5, 7), (5, 6), (3, 5, 6),
        ]
        for actual_simplex, expected_simplex in zip(
            self.vertices(order), expected_prefix
        ):
            self.assertEqual(actual_simplex, expected_simplex)
        self.assertEqual(
            self.vertices(order[-1:]),
            [(0, 1, 2, 3, 4, 5, 6, 7, 8, 9)],
        )

        keys = [
            (
                self.threshold(built, simplex),
                simplex.dim(),
                tuple(int(vertex) for vertex in simplex.vertices),
            )
            for simplex in order
        ]
        self.assertEqual(keys, sorted(keys))

    def test_threshold_is_half_the_diameter(self) -> None:
        """Each simplex appears at half the diameter of its vertices."""
        points = self.points()
        built = self.build(points)

        for simplex in built.filtration_order:
            diameter = max(
                (
                    math.dist(points[u], points[v])
                    for u, v in itertools.combinations(simplex.vertices, 2)
                ),
                default=0.0,
            )
            with self.subTest(simplex=simplex.vertices):
                self.assertAlmostEqual(
                    self.threshold(built, simplex),
                    diameter / 2,
                )

    def test_initial_filtration_contains_only_vertices(self) -> None:
        """At time zero the filtration contains the ten isolated points."""
        built = self.build(self.points())

        self.assertEqual(
            self.vertex_tuples(built.filtration(0.0).face_set),
            {(vertex,) for vertex in range(10)},
        )

    def test_final_filtration_is_a_full_simplex(self) -> None:
        """At the last threshold every non-empty subset of the points is present."""
        built = self.build(self.points())
        final = built.filtration(built.threshold_values()[-1])

        self.assertEqual(final.dim, 9)
        self.assertEqual(
            self.vertex_tuples(final.face_set),
            {
                vertices
                for size in range(1, 11)
                for vertices in itertools.combinations(range(10), size)
            },
        )
