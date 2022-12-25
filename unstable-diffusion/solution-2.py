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
    return all(list(map(lambda move_diff: move(elf_pos, move_diff) not in elves_map, directions.values())))

def is_decision_valid(direction_checks, elf_pos, elves_map, directions):    
    return all(list(map(lambda d: move(elf_pos, directions[d]) not in elves_map, direction_checks)))

def perform_diffusion(elves_map, directions, decision_choices):
    curr_round = 0
    while True:
        curr_round += 1
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
        
        if len(proposals) != 0:
            for new_move, elf_pos in proposals.items():
                # print(new_move, elf_pos)
                elves_map.remove(elf_pos)
                elves_map.add(new_move)
            
            decision_choices = rotate_list(decision_choices)
        else:
            break

    
    return curr_round

decision_choices = [('N', ['N', 'NE', 'NW']), ('S', ['S', 'SE', 'SW']), ('W', ['W', 'NW', 'SW']), ('E', ['E', 'NE', 'SE'])]

def solution():
    elves_map = get_elves_map()
    directions = get_directions()

    return perform_diffusion(elves_map, directions, decision_choices)

print(solution())
