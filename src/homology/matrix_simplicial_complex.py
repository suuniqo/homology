from __future__ import annotations

import numpy as np

from homology.simplex import Simplex
from homology.simplicial_complex import SimplicialComplex


class MatrixSimplicialComplex:
    """Compute boundary matrices and Betti numbers over GF(2)."""

    def __init__(self, sc: SimplicialComplex) -> None:
        """Initialize the complex and its caches."""
        self._sc: SimplicialComplex = sc

        # The wrapped complex is assumed not to change after construction.
        self._n_faces: dict[int, list[Simplex]] = {}
        self._n_delta: dict[int, np.ndarray] = {}
        self._n_rank: dict[int, int] = {}

    def n_faces(self, dim: int) -> list[Simplex]:
        """Return the simplices of the given dimension."""
        if dim < -1:
            raise ValueError("Dimension must be at least -1")
        if dim == -1 or dim > self._sc.dim:
            return []

        if dim not in self._n_faces:
            self._n_faces[dim] = sorted(
                self._sc.n_faces(dim),
                key=lambda simplex: simplex.vertices,
            )

        return self._n_faces[dim]

    def boundary_matrix(self, dim: int) -> np.ndarray:
        """Return the mod-2 boundary matrix from dimension dim to dim - 1."""
        if dim not in self._n_delta:
            row_faces = self.n_faces(dim - 1)
            col_faces = self.n_faces(dim)

            mat = np.zeros((len(row_faces), len(col_faces)), dtype=np.uint8)

            # Rows are (dim - 1)-faces and columns are dim-faces.
            for i, row_face in enumerate(row_faces):
                for j, col_face in enumerate(col_faces):
                    if row_face.is_face(col_face):
                        mat[i, j] = 1

            self._n_delta[dim] = mat

        return self._n_delta[dim]

    def rank_boundary_matrix(self, dim: int) -> int:
        """Return the rank of the boundary matrix over GF(2)."""
        if dim not in self._n_rank:
            mat = self.boundary_matrix(dim).copy()
            rows, cols = mat.shape

            rank = min(rows, cols)

            for k in range(min(rows, cols)):
                # Find a pivot in the remaining submatrix.
                nz = np.argwhere(mat[k:, k:] != 0)

                if nz.size == 0:
                    rank = k
                    break

                # Move the pivot to (k, k).
                i, j = nz[0] + k

                mat[[k, i], :] = mat[[i, k], :]
                mat[:, [k, j]] = mat[:, [j, k]]

                # Clear the rest of the pivot row and column.
                for nzcol in np.flatnonzero(mat[k, k+1:]) + k+1:
                    mat[:, nzcol] ^= mat[:, k]

                for nzrow in np.flatnonzero(mat[k+1:, k]) + k+1:
                    mat[nzrow, :] ^= mat[k, :]

            self._n_rank[dim] = rank

        return self._n_rank[dim]

    def smith_boundary_matrix(self, dim: int) -> np.ndarray:
        """Return the Smith normal form over GF(2)."""
        rank = self.rank_boundary_matrix(dim)
        mat = np.zeros(self.boundary_matrix(dim).shape, dtype=np.uint8)

        for k in range(rank):
            mat[k, k] = 1

        return mat

    def boundary_space_dim(self, k: int) -> int:
        """Return the dimension of the boundary space B_k."""
        return self.rank_boundary_matrix(k + 1)

    def cycle_space_dim(self, k: int) -> int:
        """Return the dimension of the cycle space Z_k."""
        return len(self.n_faces(k)) - self.rank_boundary_matrix(k)

    def betti_number(self, k: int) -> int:
        """Return the k-th Betti number over GF(2)."""
        if k < 0:
            raise ValueError("Betti numbers are only defined for k >= 0")

        return self.cycle_space_dim(k) - self.boundary_space_dim(k)
