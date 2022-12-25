input_file = open('monkey-map/input.txt', 'r')
monkey_data = input_file.readlines()

directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
diagonals = [(1, 1), (1, -1), (-1, -1), (-1, 1)]

def parse_input():
    map_data = set()
    is_wall = set()

    start_position = None

    for j, line in enumerate(monkey_data, start=1):
        line = line.strip('\n')
        for i, char in enumerate(line, start=1):
            if char == '.':
                map_data.add((j, i))
                if not start_position:
                    start_position = (j, i)
            elif char == '#':
                map_data.add((j, i))
                is_wall.add((j, i))

    instructions = []
    curr_move = ''
    for char in monkey_data[-1]:
        if char.isnumeric():
            curr_move += char
        else:
            instructions.append(int(curr_move))
            instructions.append(char)
            curr_move = ''

    instructions.append(int(curr_move))

    return map_data, is_wall, instructions, start_position

def move(spot, direction):
    y, x = spot
    y_diff, x_diff = directions[direction]

    return (y + y_diff, x + x_diff)

def is_valid_move(position, is_wall):
    if position not in is_wall:
        return True
    
    return False

def is_inner_corner(spot, map_data):
    corner_idx = None
    adj_dir_out = 0
    adj_diag_out = 0

    y, x = spot
    for y_diff, x_diff in directions:
        if (y + y_diff, x + x_diff) not in map_data:
            adj_dir_out += 1
    for i, (y_diff, x_diff) in enumerate(diagonals):
        if (y + y_diff, x + x_diff) not in map_data:
            adj_diag_out += 1
            corner_idx = i
    
    # needs to either has at least one diagonal empty spot sticking out or be an edge
    if adj_diag_out != 1 or adj_dir_out != 0:
        return False, None
    else:
        # return pair of direction idxs, norm + transposed for mapping
        return True, (corner_idx, (corner_idx + 1) % 4)
    
def zip_edges_from_corner(map_data, adj_map, dir_pair, spot):
    first_dir, second_dir = dir_pair

    has_reached_end = False

    first_spot = move(spot, first_dir)
    second_spot = move(spot, second_dir)

    # while we are still on a cube edge starting at a corner, move in both directions, x and y
    while not has_reached_end:
        first_dir_outer = (first_dir + 1) % 4
        if move(first_spot, first_dir_outer) in map_data:
            first_dir_outer = (first_dir - 1) % 4

        second_dir_outer = (second_dir + 1) % 4
        if move(second_spot, second_dir_outer) in map_data:
            second_dir_outer = (second_dir - 1) % 4

        # direction going in cube is simply opposite direction of going out
        first_dir_inner = (first_dir_outer + 2) % 4
        second_dir_inner = (second_dir_outer + 2) % 4

        # create mapping for edge point for both ways, from and to
        adj_map[(first_spot, first_dir_outer)] = (second_spot, second_dir_inner)
        adj_map[(second_spot, second_dir_outer)] = (first_spot, first_dir_inner)

        # traverse the edges, moving one spot, if it's not in the map, we reached the end
        first_spot = move(first_spot, first_dir)
        second_spot = move(second_spot, second_dir)
        
        if first_spot not in map_data or second_spot not in map_data:
            # both will evaluate to false same time since cube is symmetrical
            has_reached_end = True

def create_adjacency_map(map_data):
    adj_map = {}
    for spot in map_data:
        is_corner, dir_pair = is_inner_corner(spot, map_data)
        if is_corner:
            zip_edges_from_corner(map_data, adj_map, dir_pair, spot)
    
    return adj_map
        
def solution():
    map_data, is_wall, instructions, curr_position = parse_input()
    curr_direction = 0
    adj_map = create_adjacency_map(map_data)

    for step in instructions:
        if isinstance(step, int):
            for _ in range(step):
                delta = directions[curr_direction]
                new_position = (curr_position[0] + delta[0], curr_position[1] + delta[1])
                new_direction = curr_direction
                if new_position not in map_data:
                    state = (curr_position, curr_direction)
                    new_position = adj_map[state][0]
                    new_direction = adj_map[state][1]

                if is_valid_move(new_position, is_wall):
                    # print('moving from', curr_position, 'to', new_position)
                    curr_position = new_position
                    curr_direction = new_direction
        else:
            if step == 'R':
                curr_direction = (curr_direction + 1) % len(directions)
            else:
                curr_direction = (curr_direction - 1) % len(directions)
                
    return 1000 * curr_position[0] + 4 * curr_position[1] + curr_direction

print(solution())
