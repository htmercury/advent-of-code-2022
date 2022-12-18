input_file = open('boiling-boulders/input.txt', 'r')
points = input_file.readlines()

CUBE_SIDES = 6

adjacent_offsets = [
    (1, 0, 0),
    (-1, 0, 0),
    (0, 1, 0),
    (0, -1, 0),
    (0, 0, 1),
    (0, 0, -1)
]

def get_cube_points():
    cube_points = set()

    for pt in points:
        pt = tuple(map(lambda p: int(p), pt.strip('\n').split(',')))
        cube_points.add(pt)
        
    return cube_points

def solution():
    cube_points = get_cube_points()
    total_sides = len(cube_points) * CUBE_SIDES
    visited_points = set()
    
    for x, y, z in cube_points:
        visited_points.add((x, y, z))
        for x_offset, y_offset, z_offset in adjacent_offsets:
            if (x + x_offset, y + y_offset, z + z_offset) in visited_points:
                # found an adj cube, remove sides
                total_sides -= 2

    return total_sides

print(solution())
