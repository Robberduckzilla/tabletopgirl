#!/usr/bin/env python3
import numpy as np
from random import randint, choice

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

"""
Mapping from a face, to the face above when viewed such that the text
is upright.
"""
DICE_FACES_ABOVE = {
    1 : 5,
    2 : 1,
    3 : 1,
    4 : 1,
    5 : 1,
    6 : 2
    }

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
    raise ValueError(f"Face not found at position {orig_position}. This shouldn't happen.")

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
    #front_position = np.array((0,0,1))

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

def calc_rotation_parity(rotation):
    """
    Calculates the parity (0 or 1) of the given rotation permutation.
    """
    # Initial position of numbers 1-6
    start = list(RIGHT_HANDED_DICE.values())

    end = list((rotation @ np.array(start).T).T)

    permutation = np.array([[np.array_equal(s,e) for s in start] for e in end],dtype=int)
    sign = int(np.linalg.det(permutation))

    return (1-sign)//2

class ParityError(Exception):
    pass

def generate_solution_paths(start_pos, end_pos, start_rot, end_rot):
    """
    Returns valid paths, including matching rotations, for given start and
    end positions. For paths with bad parity, immediately return.
    Returns as a generator.
    """
    rotation = end_rot @ start_rot.T

    #Check valid rotation
    valid = (True
        and (np.array_equal(rotation.T @ rotation, np.identity(3,dtype=int)))
        and (rotation.dtype is np.dtype(int))
        and (int(np.linalg.det(rotation)) == 1)
        )

    if not valid:
        raise ValueError("Invalid rotation given")

    rot_parity = calc_rotation_parity(rotation)
    dist_parity = (sum(start_pos) + sum(end_pos)) % 2

    if rot_parity != dist_parity:
        raise ParityError("Bad parity")

    return (p for p in generate_paths(start_pos,end_pos) if np.array_equal(calculate_path_rotation(p), rotation))


def generate_random_dice():
    face = choice(tuple(DICE.keys()))
    orientation = np.linalg.matrix_power(ROTATION_CLOCKWISE,randint(0,3)) @ get_dice_orientation_front(face)

    x = randint(1,GRID_SIZE)
    y = randint(1,GRID_SIZE)
    position = (x,y)

    return position, orientation
    

def generate_multiple_random_dice(n):
    """:("""

    positions = set()
    dices = []

    if n > (GRID_SIZE**2):
        # Trying to generate more dice than grid spaces...
        raise ValueError(f"Not enough space for {n} dice in a {GRID_SIZE}x{GRID_SIZE} grid.")
    while len(dices) < n:
        p,o = generate_random_dice()
        if p not in positions:
            positions.add(p)
            dices.append((p,o))
    
    return dices


def calculate_face_rotation(orientation):

    # Get face facing towards us (that we can see)
    face = get_dice_face(orientation, (0,0,1))
    # The face directly above our chosen face (when the text is upright)
    face_above = DICE_FACES_ABOVE[face]

    face_above_position = orientation @ DICE[face_above]
    # face_above_position can only be one of: (1,0,0), (0,1,0), (-1,0,0), (0,-1,0)
    x, y, _ = face_above_position
    angle = np.degrees(np.arctan2(x,y))

    return face, angle
    

def get_path_coordinates(start_pos, path):
    """
    Converts a start position (2,3), and path NWSSS to a list of squares
    [(2,3),(2,4),(1,4),(1,3),(1,2),(1,1)]
    """

    pos = start_pos
    coords = [start_pos]

    for step in path:
        i = DIRECTIONS.index(step)
        
        if i == 0:
            y=pos[1]+1
            pos = (pos[0], y)
        elif i == 1:
            y = pos[1]-1
            pos = (pos[0], y)
        elif i == 2:
            x = pos[0]+1
            pos = (x, pos[1])
        else:
            x = pos[0]-1
            pos = (x, pos[1])

        coords.append(pos)
    
    return coords


def generate_map(pair_count, blocks=0, retry_count=100, min_length=3, strict_impossible=True):
    """
    Generates plans for a full grid. Output format:
    {
        "pairs": [
            (
                {pos: (3,3), face: 3, angle: 90}, # start
                {pos: (4,4), face: 5, angle: 0} # end
            ),
            ...
            # more starts+ends
        ],
        "solutions": [
            (3,3),(2,3),(2,4),(3,4),(4,4)
            ...
            # more paths, False if no possible path
        ],
        "blocks" {
            (2,2),
            ...
        }
    }
    
    If strict_impossible is set to true, then we reject pairs where we cannot
    find solutions, nor prove there are no solutions.
    """
    global blocked_squares

    class InvalidMapError(Exception):
        """
        Raised whenever a map has violated design constraints.
        """
        pass


    def solve_pairs():
        """
        Solve pairs, find shortest solution.
        Returns True/False on success/failure
        """
        # Solve, find shortest solutions
        nonlocal pairs
        nonlocal strict_impossible
        nonlocal solutions
        solutions = []

        for start,end in pairs:
            try:
                paths = generate_solution_paths(start[0], end[0], start[1], end[1])
                shortest_path = next(paths)
                solutions.append(shortest_path)

            except ParityError:
                # Bad parity, we know no solutions exist
                solutions.append(False)

            except StopIteration:
                # Parity is correct, but no solutions have been found.
                if strict_impossible:
                    # Reject map, start again.
                    solutions = False
                    raise InvalidMapError("strict_impossible condition violated.")
                else:
                    solutions.append(False)

    def add_block():
        """
        Attempts to add a blocker to the current map.
        If there are possible solution paths, the block will be placed on
        the shortest path if possible. Else, the block will be placed randomly.

        Returns True if successful, False if unsuccessful.
        """
        nonlocal solutions
        nonlocal dice
        global blocked_squares

        if solutions is False:
            raise InvalidMapError("No solutions to work from.")

        shortest_path = find_shortest_path()[0]
        dice_coords = {d[0] for d in dice}

        if shortest_path is not None:
            # At least one route is valid

            # Attempt to find a space to place a block, on the shortest
            # path, but not on another dice.
            path_coords = get_path_coordinates(pairs[shortest_path][0][0], solutions[shortest_path])

            possible_blocks = [p for p in path_coords if p not in dice_coords]
        else:
            # All routes blocked
            empty_coords = ((x+1,y+1) for x in range(GRID_SIZE) for y in range(GRID_SIZE))
            possible_blocks = [p for p in empty_coords if p not in dice_coords]
                
        if len(possible_blocks) > 0:
            block_pos = choice(possible_blocks)
            blocked_squares.add(block_pos)
        else:
            # No valid positions, to place blocks, emergency abort!
            raise InvalidMapError("No space to add blocks.")

    def find_shortest_path():
        """
        Returns the index and length of the shortest path.
        If there are no solutions, returns (None, np.inf)
        """
        nonlocal solutions

        if solutions is False:
            raise InvalidMapError("No solutions to work from.")

        # Find shortest path, for map validation and adding blockers
        shortest_path = None
        shortest_length = np.inf

        for i, solution in enumerate(solutions):
            if (solution != False) and (len(solution) < shortest_length):
                shortest_path = i
                shortest_length = len(solution)

        return shortest_path, shortest_length
        

    for i in range(retry_count):
        # After so many failed attempts, we give up. This should help prevent
        #  accidental infinite loops for bad configurations.

        try:
            # Generate some pairs
            dice = generate_multiple_random_dice(2*pair_count)
            pairs = list(zip(dice[0::2],dice[1::2]))
            solutions = []

            solve_pairs()

            if find_shortest_path()[1] < min_length:
                raise InvalidMapError("Solution path too short.")

            blocked_squares = set()

            for _ in range(blocks):
                add_block()
                solve_pairs()

        except InvalidMapError:
            # Reject map, retry.
            continue
        
        # Assuming we reach here, a valid map has been acheived!
        print(f"Succeded making map after {i+1} attempt(s).")
        break

    else:
        print(f"ERR: No valid map found after {retry_count} tries, aborting.")
        return False
    
    # Now, convert to correct output format.
    solutions = [
            get_path_coordinates(pairs[i][0][0], solutions[i]) 
            if (solutions[i] != False) else False 
            for i in range(pair_count)
            ]

    def dice_to_dict(dice):
        # (pos, rot) -> {pos: ..., face: ..., angle: ...}
        pos, rot = dice
        face, angle = calculate_face_rotation(rot)
        return {"pos": pos, "face": face, "angle": angle}
    
    dice = [dice_to_dict(d) for d in dice]
    pairs = list(zip(dice[0::2],dice[1::2]))

    return {"pairs": pairs, "solutions": solutions, "blocks": tuple(blocked_squares)}


if __name__ == "__main__":
    blocked_squares.add((2,3))
    for p in generate_paths(start_default,end_default):
        e = np.array_equal(calculate_path_rotation(p), rotation_default)
        if e:
            print(p)
