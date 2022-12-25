input_file = open('monkey-map/input.txt', 'r')
monkey_data = input_file.readlines()

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

def get_row_points(j, map_data):
    row_points = [p for p in map_data if p[0] == j]
    row_points.sort(key = lambda p: p[1])
    return row_points

def get_col_points(i, map_data):
    col_points = [p for p in map_data if p[1] == i]
    col_points.sort(key = lambda p: p[0])
    return col_points

def get_wrapped_position(position, curr_direction, map_data):
    if curr_direction == 0:
        return get_row_points(position[0], map_data)[0]
    elif curr_direction == 1:
        return get_col_points(position[1], map_data)[0]
    elif curr_direction == 2:
        return get_row_points(position[0], map_data)[-1]
    else:
        return get_col_points(position[1], map_data)[-1]

def is_valid_move(position, is_wall):
    if position not in is_wall:
        return True
    
    return False

def solution():
    map_data, is_wall, instructions, curr_position = parse_input()
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    curr_direction = 0

    for step in instructions:
        if isinstance(step, int):
            for _ in range(step):
                delta = directions[curr_direction]
                new_position = (curr_position[0] + delta[0], curr_position[1] + delta[1])
                if new_position not in map_data:
                    new_position = get_wrapped_position(new_position, curr_direction, map_data)

                if is_valid_move(new_position, is_wall):
                    # print('moving from', curr_position, 'to', new_position)
                    curr_position = new_position
        else:
            if step == 'R':
                curr_direction = (curr_direction + 1) % len(directions)
            else:
                curr_direction = (curr_direction - 1) % len(directions)
                      
    return 1000 * curr_position[0] + 4 * curr_position[1] + curr_direction

print(solution())
