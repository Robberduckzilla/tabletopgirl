#!/usr/bin/env python3
import numpy as np

# Assuming a square grid of this size.
GRID_SIZE = 4

# How many additional steps we look in each direction, to find extra,
#  longer solutions. Be careful with this on a larger grid.
EXTRA_STEPS = 10

# Default start, end position and desired rotation.
#  co-ordinates are 1-indexed
start_default = (3,3)
end_default = (4,4)
rotation_default = np.array([
    [0,0,1],
    [1,0,0],
    [0,1,0]
    ])

# Define squares we can't access
blocked_squares = set()
# blocked_squares.add((2,3))

# Direction names
DIRECTIONS = ('N','S','E','W')
#DIRECTIONS = ('U','D','R','L') # alternate names

# Rotation when the cube is moved north/up,
# i.e. a 90° rotation about -x axis
ROTATION_NORTH = np.array([
    [1,0,0],
    [0,0,1],
    [0,-1,0]
    ])

# Rotation when the cube is moved east/right,
# i.e. a 90° rotation about +y axis
ROTATION_EAST = np.array([
    [0,0,1],
    [0,1,0],
    [-1,0,0]
    ])

# Rotation clockwise, about -z axis. Not possible by rules.
ROTATION_CLOCKWISE = np.array([
    [0,1,0],
    [-1,0,0],
    [0,0,1]
    ])


"""
Define cube orientation, and posision of numbers.
This is defined by a mapping from numbers (1-6) to positions (x,y,z)
We assume that 1 is facing towards us (0,0,+1), and 2 is facing right (+1,0,0)

For right-handed, anti-clockwise dice (most western dice), we have
        +---+
        | 3 |
+---+---+---+---+
| 6 | 5 | 1 | 2 |
+---+---+---+---+
        | 4 |
        +---+
"""
RIGHT_HANDED_DICE = {
        1 : np.array(( 0, 0,+1)),
        2 : np.array((+1, 0, 0)),
        3 : np.array(( 0,+1, 0)),
        4 : np.array(( 0,-1, 0)),
        5 : np.array((-1, 0, 0)),
        6 : np.array(( 0, 0,-1))
        }

"""
For left-handed, clockwise dice (most eastern dice), we have
        +---+
        | 4 |
+---+---+---+---+
| 6 | 5 | 1 | 2 |
+---+---+---+---+
        | 3 |
        +---+
"""
LEFT_HANDED_DICE = {
        1 : np.array(( 0, 0,+1)),
        2 : np.array((+1, 0, 0)),
        3 : np.array(( 0,-1, 0)),
        4 : np.array(( 0,+1, 0)),
        5 : np.array((-1, 0, 0)),
        6 : np.array(( 0, 0,-1))
        }

DICE = LEFT_HANDED_DICE
DICE_CHIRALITY = 'L'

def get_dice_face(orientation, position):
    """
    Gets the face of the dice at the given position (e.g. top face at (0,1,0))
    for a dice with the orientation given by a rotation matrix.
    """
    orig_position = orientation.T @ np.array(position, dtype=int)
    for face, pos in DICE.items():
        if np.array_equal(pos, orig_position):
            return face

    # If we've reached here, something's wrong!
    raise ValueError(f"Face not found at position {orig_position}.")

def get_dice_orientation(face1, pos1, face2=0, pos2=None):
    """
    Calculates a valid orientation matrix for a dice with given face
    positions. 

    Faces should be numbers (1-6), pos should be python tuples e.g. (0,1,0)
    """
    # I should probably get this one working...
    raise NotImplementedError()

def get_dice_orientation_front(face):
    """
    Generates a dice orientation with the given face in the forward (+z)
    direction.
    """
    orig_position = DICE[face]
    front_position = np.array((0,0,1))

    orientation = np.zeros((3,3),dtype=int)
    # Now set element of orientation s.t.
    #  front_position = orientation @ orig_position
    #  det(orientation) = 1
    #  rotation is 90°

    k = orig_position.nonzero()[0][0]

    # Choose this so front face is correct
    orientation[2][k] = orig_position[k]

    # Now det(o) = o[0][i] * o[1][j] * o[2][k] * e_ijk
    i,j = [_ for _ in (0,1,2) if _ != k]
    e_ijk = (i-j)*(j-k)*(k-i)//2

    orientation[0][i] = 1
    orientation[1][j] = orig_position[k] * e_ijk

    return orientation


def calculate_path_rotation(path):
    """
    Takes a path in string form,
    e.g. 'NNENWWS'
    Returns a rotation matrix for the overall journey for the cube
    """
    ROTATION_MATRICES = [
            ROTATION_NORTH,
            ROTATION_NORTH.T,
            ROTATION_EAST,
            ROTATION_EAST.T
            ]

    rotation = np.identity(3, dtype=int)

    for step in path:
        i = DIRECTIONS.index(step)
        rotation = ROTATION_MATRICES[i] @ rotation

    return rotation

def validate_path(path, start, include_start=True):
    """
    Takes a path in string form,
    e.g. 'NNENWWS'
    and checks there are no intersections or out of bounds.
    """
    pos = start

    if include_start:
        visited = {start}
    else:
        visited = set()

    for step in path:
        i = DIRECTIONS.index(step)

        # Check bounds
        if i == 0:
            y=pos[1]+1
            if y > GRID_SIZE:
                return False
            pos = (pos[0], y)

        elif i == 1:
            y = pos[1]-1
            if y == 0:
                return False
            pos = (pos[0], y)

        elif i == 2:
            x = pos[0]+1
            if x > GRID_SIZE:
                return False
            pos = (x, pos[1])

        else:
            x = pos[0]-1
            if x == 0:
                return False
            pos = (x, pos[1])

        # Check self-intersection
        if pos in visited:
            return False

        # Check path not blocked
        if pos in blocked_squares:
            return False

        visited.add(pos)

    return True

def generate_paths(start, end):
    """
    Generate a sequence of increasing length paths from start to end.
    Returns a string of directions, e.g. 'NNENW'

    Internally, 'path' is the current route, and 'remaining' stores how many
    steps we must take still in each direction
    """

    EXTRA_NS = np.array((1,1,0,0))
    EXTRA_EW = np.array((0,0,1,1))

    def gen_paths_recursive(path, remaining):
        nonlocal start

        if sum(remaining) == 0:
            yield path
            return

        for i, d in enumerate(DIRECTIONS):
            if remaining[i] == 0:
                continue

            p = path+d
            if not validate_path(p, start):
                continue

            r = remaining.copy()
            r[i] -= 1
            yield from gen_paths_recursive(p,r)

    path = ''
    remaining = np.zeros(4,dtype=int)

    dist_north = end[1] - start[1]
    if dist_north > 0:
        remaining[0] = dist_north
    else:
        remaining[1] = -dist_north

    dist_east = end[0] - start[0]
    if dist_east > 0:
        remaining[2] = dist_east
    else:
        remaining[3] = -dist_east

    # Limit number of steps for a small grid. This significantly speeds up
    #  the program, but I'm not entirely sure why it should...
    extra = min((GRID_SIZE**2 - sum(remaining))//2 + 1, EXTRA_STEPS)

    #print(f"Searching for paths up to length {sum(remaining)+2*extra}.")
    for a in range(extra+1):
        for b in range(a+1):
            r = remaining + EXTRA_NS*(a-b) + EXTRA_EW*(b)

            yield from gen_paths_recursive(path, r)

def generate_solution_paths(start, end, rotation):
    # There should be some check in here to stop immediately if we can prove
    #  no solutions are possible via parity arguments
    return (p for p in generate_paths(start,end) if np.array_equal(calculate_path_rotation(p), rotation))

if __name__ == "__main__":
    for p in generate_paths(start_default,end_default):
        e = np.array_equal(calculate_path_rotation(p), rotation_default)
        if e:
            #print(e)
            print(p)
            #print(calculate_rotation(p))
