input_file = open('regolith-reservoir/input.txt', 'r')
rock_traces = input_file.readlines()

FLOOR_DIST = 2

def get_paths():
    paths = []
    for rock_path in rock_traces:
        rock_path = rock_path.strip('\n').split(' -> ')
        rock_list = map(lambda p: p.split(','), rock_path)
        paths.append(list(map(lambda p: [int(p[0]), int(p[1])], rock_list)))
    return paths

def get_scan_bounds(paths):
    all_points = []
    for path in paths:
        all_points += path
    min_width = min(map(lambda p: p[0], all_points))
    max_width = max(map(lambda p: p[0], all_points)) + 1
    max_height = max(map(lambda p: p[1], all_points)) + 1

    return min_width, max_width, max_height

def print_map(map):
    for row in map:
        # print('\n')
        print(''.join(row))

def direction(v1, v2):
    if v1 > v2:
        return -1
    else:
        return 1

def insert_path(path, rock_map, x_offset, padding):
    prev_point = path[0]
    for i in range(1, len(path)):
        curr_point = path[i]
        if prev_point[0] == curr_point[0]:
            while prev_point[1] != curr_point[1]:
                rock_map[prev_point[1]][prev_point[0] - x_offset + padding] = '#'
                prev_point[1] += direction(prev_point[1], curr_point[1])
        else:
            while prev_point[0] != curr_point[0]:
                rock_map[prev_point[1]][prev_point[0] - x_offset + padding] = '#'
                prev_point[0] += direction(prev_point[0], curr_point[0])
        # insert remaining curr_point match
        rock_map[prev_point[1]][prev_point[0] - x_offset + padding] = '#'


def create_map(paths):
    min_width, max_width, max_height = get_scan_bounds(paths)
    width_length = max_width - min_width
    padding = min_width // 3
    rock_map = []
    for _ in range(max_height + FLOOR_DIST):
        rock_map_row = []
        for _ in range(width_length + 2*padding):
            rock_map_row.append('.')
        rock_map.append(rock_map_row)

    for p in paths:
        insert_path(p, rock_map, min_width, padding)
    
    # add in the sand spawner
    sand_start = [0, 500 - min_width + padding]
    rock_map[sand_start[0]][sand_start[1]] = '+'

    # add in floor
    for i in range(width_length + 2*padding):
        rock_map[max_height + FLOOR_DIST - 1][i] = '#'

    return sand_start, rock_map

def is_valid(y, x, rock_map):
    max_y, max_x = len(rock_map), len(rock_map[0])
    return x >= 0 and y >= 0 and x < max_x and y < max_y

def drop_sand(sand_start, rock_map, moves):
    sand_y, sand_x = sand_start
    if rock_map[sand_y][sand_x] == 'o':
        return True
    while True:
        moved = False
        for move in moves:
            new_y, new_x = sand_y + move[0], sand_x + move[1]
            if is_valid(new_y, new_x, rock_map) and rock_map[new_y][new_x] == '.':
                sand_y, sand_x = new_y, new_x
                moved = True
                break
        
        if not moved:
            rock_map[sand_y][sand_x] = 'o'
            return False

def print_map(map):
    for row in map:
        print(' '.join(row))

def solution():
    paths = get_paths()
    sand_start, rock_map = create_map(paths)

    moves = [[1, 0], [1, -1], [1, 1]]
    sand_dropped = 0

    while not drop_sand(sand_start, rock_map, moves):
        sand_dropped += 1

    # print_map(rock_map)
    return sand_dropped

print(solution())
