from collections import namedtuple

Shape = namedtuple("Shape", ["Name", "Path"])

square = Shape("Square", "M -1 1 L 1 1 L 1 -1 L -1 -1 Z")
up_pointing_triangle = Shape("Up-Pointing Triangle", "M 0 -1 L -1 1 L 1 1 Z")
