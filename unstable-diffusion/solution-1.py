input_file = open('unstable-diffusion/input.txt', 'r')
map_data = input_file.readlines()

def get_elves_map():
    elves_map = set()

    for j, line in enumerate(map_data):
        line = line.strip('\n')
        for i, char in enumerate(line):
            if char == '#':
                elves_map.add((j, i))
    
    return elves_map

def get_directions():
    directions = {
        'N': (-1, 0),
        'S': (1, 0),
        'W': (0, -1),
        'E': (0, 1)
    }
    diagonal_directions = ['NE', 'NW', 'SE', 'SW']
    for diagonal_direction in diagonal_directions:
        d1, d2 = diagonal_direction
        y1, x1 = directions[d1]
        y2, x2 = directions[d2]
        directions[d1 + d2] = (y2 + y1, x2 + x1)
    
    return directions

def move(position, move_diff):
    y, x = position
    y_diff, x_diff = move_diff

    return (y + y_diff, x + x_diff)

def rotate_list(lst):
    return lst[1:] + lst[:1]

def check_adjacent_areas(elf_pos, elves_map, directions):
    adjacent_areas = {}
    for d, move_diff in directions.items():
        adjacent_areas[d] = move(elf_pos, move_diff)
    return all(list(map(lambda d: adjacent_areas[d] not in elves_map, directions.keys())))

def is_decision_valid(direction_checks, elf_pos, elves_map, directions):
    adjacent_areas = {}
    for d in direction_checks:
        adjacent_areas[d] = move(elf_pos, directions[d])
    
    return all(list(map(lambda d: adjacent_areas[d] not in elves_map, direction_checks)))

def perform_diffusion(elves_map, directions, decision_choices):
    for _ in range(10):
        proposals = {}
        clashes = set()
        for elf_pos in elves_map:
            if check_adjacent_areas(elf_pos, elves_map, directions):
                continue
            
            for decision, direction_checks in decision_choices:
                if is_decision_valid(direction_checks, elf_pos, elves_map, directions):
                    next_move = move(elf_pos, directions[decision])
                    if next_move in proposals:
                        del proposals[next_move]
                        clashes.add(next_move)
                    elif next_move not in clashes:
                        proposals[next_move] = elf_pos
                    break
        
        for new_move, elf_pos in proposals.items():
            # print(new_move, elf_pos)
            elves_map.remove(elf_pos)
            elves_map.add(new_move)

        decision_choices = rotate_list(decision_choices)

def get_blank_spaces(elves_map):
    y_list = [p[0] for p in elves_map]
    x_list = [p[1] for p in elves_map]
    y_min, y_max = min(y_list), max(y_list)
    x_min, x_max = min(x_list), max(x_list)

    return ((y_max - y_min) + 1) * ((x_max - x_min) + 1) - len(elves_map)

decision_choices = [('N', ['N', 'NE', 'NW']), ('S', ['S', 'SE', 'SW']), ('W', ['W', 'NW', 'SW']), ('E', ['E', 'NE', 'SE'])]

def solution():
    elves_map = get_elves_map()
    directions = get_directions()

    perform_diffusion(elves_map, directions, decision_choices)
    return get_blank_spaces(elves_map)

print(solution())
