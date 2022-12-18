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

def get_bounds(cube_points):
    x_min = x_max = y_min = y_max = z_min = z_max = 0
    x_points = list(map(lambda p: p[0], cube_points))
    x_min = min(x_points)
    x_max = max(x_points)
    y_points = list(map(lambda p: p[1], cube_points))
    y_min = min(y_points)
    y_max = max(y_points)
    z_points = list(map(lambda p: p[2], cube_points))
    z_min = min(z_points)
    z_max = max(z_points)
    
    return x_min, x_max, y_min, y_max, z_min, z_max
    
cube_points = get_cube_points()
x_min, x_max, y_min, y_max, z_min, z_max = get_bounds(cube_points)

def is_valid(point):
        x, y, z = point
        valid_x = x >= x_min and x <= x_max
        valid_y = y >= y_min and y <= y_max
        valid_z = z >= z_min and z <= z_max
        return valid_x and valid_y and valid_z

def get_external_points(cube_points):
    external_points = set()
    point_q = []
    point_q.append((x_min, y_min, z_min))

    # find empty points in the cube points set
    while len(point_q) != 0:
        curr_point = point_q.pop(0)
        if curr_point in external_points:
            continue
        
        external_points.add(curr_point)   
        curr_x, curr_y, curr_z = curr_point
        
        for x_offset, y_offset, z_offset in adjacent_offsets:
            new_point = (curr_x + x_offset, curr_y + y_offset, curr_z + z_offset)
            if is_valid(new_point) and new_point not in cube_points:
                point_q.append(new_point)
                
    return external_points

def get_lava_points():
    external_points = get_external_points(cube_points)

    lava = set()
    for x in range(x_min, x_max + 1):
        for y in range(y_min, y_max + 1):
            for z in range(z_min, z_max + 1):
                lava.add((x, y, z))

    lava -= external_points
    
    return lava

def solution():
    lava = get_lava_points()

    total_sides = len(lava) * CUBE_SIDES
    visited_points = set()

    for x, y, z in lava:
        visited_points.add((x, y, z))
        for x_offset, y_offset, z_offset in adjacent_offsets:
            if (x + x_offset, y + y_offset, z + z_offset) in visited_points:
                # found an adj cube, remove sides
                total_sides -= 2
                
    return total_sides

print(solution())
