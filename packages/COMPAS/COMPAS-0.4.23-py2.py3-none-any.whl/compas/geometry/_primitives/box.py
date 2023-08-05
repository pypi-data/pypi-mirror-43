from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas.geometry import add_vectors


__all__ = ['Box']


class Box(object):
    """A box is a three-dimensional geometric shape with 8 vertices, 12 edges and 6 faces.

    The edges of a box meet at its vertices at 90 degree angles.
    The faces of a box are planar.
    Faces which do not share an edge are parallel.

    Parameters
    ----------
    vertices : list of point
        The XYZ coordinates of the vertices of the box.
    faces : list of list
        The faces of the box defined as lists of vertex indices.

    Examples
    --------
    .. code-block:: python

        pass

    """

    def __init__(self, vertices, faces):
        self._vertices = None
        self._faces = None
        self.vertices = vertices
        self.faces = faces

    @property
    def vertices(self):
        return self._vertices

    @vertices.setter
    def vertices(self, vertices):
        if len(vertices) != 8:
            raise Exception("A box must have exactly 8 vertices.")
        self._vertices = vertices

    @property
    def faces(self):
        return self._faces

    @faces.setter
    def faces(self, faces):
        if len(faces) != 6:
            raise Exception("A box must have exactly 6 faces.")
        if any(len(face) != 4 for face in faces):
            raise Exception("The faces of a box must all be quads.")
        self._faces = faces

    @classmethod
    def from_width_height_depth(cls, width, height, depth):
        """Construct a box from its width, height and depth.

        Parameters
        ----------
        width : float
            Width of the box.
        height : float
            Height of the box.
        depth : float
            Depth of the box.

        Returns
        -------
        Box
            The resulting box.

        Notes
        -----
        The bottom left corner of the box is positioned at the origin of the
        coordinates system. The box is axis-aligned.

        Examples
        --------
        .. code-block:: python

            box = Box.from_width_height_depth(1.0, 2.0, 3.0)

        """
        width = float(width)
        height = float(height)
        depth = float(depth)

        if width == 0.0:
            raise Exception('Width cannot be zero.')

        if height == 0.0:
            raise Exception('Height cannot be zero.')

        if depth == 0.0:
            raise Exception('Depth cannot be zero.')

        a = 0.0, 0.0, 0.0
        b = 0.0, depth, 0.0
        c = width, depth, 0.0
        d = width, 0.0, 0.0

        vector = [0.0, 0.0, height]

        e = add_vectors(a, vector)
        f = add_vectors(d, vector)
        g = add_vectors(c, vector)
        h = add_vectors(b, vector)

        vertices = [a, b, c, d, e, f, g, h]

        faces = [
            [0, 1, 2, 3],
            [0, 3, 5, 4],
            [3, 2, 6, 5],
            [2, 1, 7, 6],
            [1, 0, 4, 7],
            [4, 5, 6, 7]
        ]
        return cls(vertices, faces)

    @classmethod
    def from_bounding_box(cls, bbox):
        faces = [
            [0, 1, 2, 3],
            [0, 3, 5, 4],
            [3, 2, 6, 5],
            [2, 1, 7, 6],
            [1, 0, 4, 7],
            [4, 5, 6, 7]
        ]
        return cls(bbox, faces)

    @classmethod
    def from_corner_corner_height(cls, corner1, corner2, height):
        """Construct a box from the opposite corners of its base and its height.

        Parameters
        ----------
        corner1 : point
            The XYZ coordinates of the bottom left corner of the base of the box.
        corner2 : point
            The XYZ coordinates of the top right corner of the base of the box.
        height : float
            The height of the box.

        Returns
        -------
        Box
            The resulting box.

        Examples
        --------
        .. code-block:: python

            box = Box.from_corner_corner_height([0.0, 0.0, 0.0], [1.0, 1.0, 0.0], 1.0)

        """
        if height == 0:
            raise Exception('The box should have a height.')
        vector = [0.0, 0.0, float(height)]

        x1, y1, z1 = corner1
        x2, y2, z2 = corner2

        if z1 != z2:
            raise Exception('Corners should be in the same horizontal plane.')

        z = z1

        a = corner1
        b = x1, y2, z
        c = corner2
        d = x2, y1, z

        e = add_vectors(a, vector)
        f = add_vectors(d, vector)
        g = add_vectors(c, vector)
        h = add_vectors(b, vector)

        vertices = [a, b, c, d, e, f, g, h]

        faces = [
            [0, 1, 2, 3],
            [0, 3, 5, 4],
            [3, 2, 6, 5],
            [2, 1, 7, 6],
            [1, 0, 4, 7],
            [4, 5, 6, 7]
        ]
        return cls(vertices, faces)

    @classmethod
    def from_diagonal(cls, diagonal):
        """Construct a box from its main diagonal.

        Parameters
        ----------
        diagonal : segment
            The diagonal of the box, represented by a pair of points in space.

        Returns
        -------
        Box
            The resulting box.

        Examples
        --------
        .. code-block:: python

            box = Box.from_diagonal([0.0, 0.0, 0.0], [1.0, 1.0, 1.0])

        """
        d1, d2 = diagonal

        x1, y1, z1 = d1
        x2, y2, z2 = d2

        if z1 == z2:
            raise Exception('The box has no height.')

        a = d1
        b = x1, y2, z1
        c = x2, y2, z1
        d = x2, y1, z1

        e = x1, y1, z2
        f = x2, y1, z2
        g = d2
        h = x1, y2, z2

        vertices = [a, b, c, d, e, f, g, h]

        faces = [
            [0, 1, 2, 3],
            [0, 3, 5, 4],
            [3, 2, 6, 5],
            [2, 1, 7, 6],
            [1, 0, 4, 7],
            [4, 5, 6, 7]
        ]
        return cls(vertices, faces)


# ==============================================================================
# Main
# ==============================================================================


if __name__ == '__main__':

    from compas.geometry import Box
    from compas.datastructures import Mesh

    box = Box.from_corner_corner_height([0., 0., 0.], [1., 1., 0.], 4.0)

    mesh = Mesh.from_vertices_and_faces(box.vertices, box.faces)

    print(mesh)
