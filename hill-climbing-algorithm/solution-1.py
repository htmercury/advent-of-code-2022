input_file = open('hill-climbing-algorithm/input.txt', 'r')
hill_lines = input_file.readlines()

moves = [[0, 1], [0, -1], [1, 0], [-1, 0]]

class Climber:
    def __init__(self, i, j, steps = 0) -> None:
        self.y = i
        self.x = j
        self.steps = steps

def get_num_elevation(char):
    return ord(char) - 96

def find_src_dest_and_format(hill_data):
    for i, row in enumerate(hill_data):
        for j, area in enumerate(row):
            if area == 'S':
                src = [i, j]
                hill_data[i][j] = get_num_elevation('a')
            elif area == 'E':
                dest = [i, j]
                hill_data[i][j] = get_num_elevation('z')
            else:
                hill_data[i][j] = get_num_elevation(hill_data[i][j])

    return src, dest

def is_valid_move(move, elevation, hill_data):
    i, j = move
    max_Y = len(hill_data)
    max_X = len(hill_data[0])
    if i >= max_Y or j >= max_X or i < 0 or j < 0:
        return False
    next_elevation = hill_data[i][j]

    if next_elevation - elevation > 1:
        return False
    
    return True

def solution():
    hill_data = []
    for line in hill_lines:
        line = line.strip('\n')
        hill_data.append(list(line))

    src, dest = find_src_dest_and_format(hill_data)

    path_queue = []
    visited = []
    init_climber = Climber(src[0], src[1])
    path_queue.append(init_climber)
    visited.append(src)

    while len(path_queue) != 0:
        curr_climber = path_queue.pop(0)
        curr_elevation = hill_data[curr_climber.y][curr_climber.x]

        if curr_climber.y == dest[0] and curr_climber.x == dest[1]:
            return curr_climber.steps
        
        for move in moves:
            new_move = [curr_climber.y + move[0], curr_climber.x + move[1]]
            if new_move not in visited and is_valid_move(new_move, curr_elevation, hill_data):
                new_climber = Climber(new_move[0], new_move[1], curr_climber.steps + 1)
                path_queue.append(new_climber)
                visited.append(new_move)

print(solution())
