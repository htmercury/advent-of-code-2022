input_file = open('blizzard-basin/input.txt', 'r')
map_data = input_file.readlines()

blizzards = {
    '^': (-1, 0),
    '>': (0, 1),
    'v': (1, 0),
    '<': (0, -1)
}

moves = [
    (-1, 0),
    (0, 1),
    (1, 0),
    (0, -1)
]

class Blizzard:
    def __init__(self, loc, char) -> None:
        self.loc = loc
        self.direction = blizzards[char]
        self.str_repr = char
    
    def move(self, map_spots):
        y, x = self.loc
        y_diff, x_diff = self.direction
        new_loc = (y + y_diff, x + x_diff)

        if new_loc not in map_spots:
            new_loc = self.get_wrapped_pos()
        
        # print(self.loc, 'moving', self.str_repr, new_loc)
        self.loc = new_loc
    
    def get_wrapped_pos(self):
        y, x = self.loc
        if self.str_repr == '^':
            return (len(map_data) - 2, x)
        elif self.str_repr == '>':
            return (y, 1)
        elif self.str_repr == 'v':
            return (1, x)
        else:
            return (y, len(map_data[0]) - 3)

def gcd(a,b):
    if a == 0:
        return b
    return gcd(b % a, a)

def lcm(a,b):
    return (a // gcd(a,b))* b

def parse_input():
    map_spots = set()
    blizzard_spots = []
    src = None

    for j, line in enumerate(map_data):
        line = line.strip('\n')
        for i, char in enumerate(line):
            if char == '.':
                map_spots.add((j, i))
                if not src:
                    src = (j, i)
                dest = (j, i)
            elif char != '#':
                map_spots.add((j, i))
                blizzard_spots.append(Blizzard((j, i), char))

    map_length = lcm(len(map_data), len(map_data[0]))
    return map_spots, map_length, (src, dest), blizzard_spots

def print_map(map_data, map_spots, blizzard_spots):
    for j in range(len(map_data)):
        row = ''
        for i in range(len(map_data[0])  - 1):
            if (j, i) in map_spots:
                curr_b = 0
                bs = ''
                for b in blizzard_spots:
                    if b.loc == (j, i):
                        curr_b += 1
                        bs = b.str_repr
                if curr_b > 1:
                    row += str(curr_b)
                elif curr_b == 1:
                    row += bs
                else:
                    row += '.'
            else:
                row += '#'
        print(row)

def solution():
    map_spots, map_length, (src, dest), blizzard_spots = parse_input()
    
    path_q = []
    path_q.append((src, 0))
    blizzard_hist = [set(map(lambda b: b.loc, blizzard_spots))]
    visited = set()

    while len(path_q) != 0:
        (y, x), curr_t = path_q.pop(0)
        if (y, x) == dest:
            return curr_t

        if (y, x, (curr_t) % map_length) in visited:
            continue
        else:
            visited.add((y, x, (curr_t) % map_length))
        
        if (y, x) in blizzard_hist[curr_t]:
            continue

        if curr_t + 1 >= len(blizzard_hist):
            # move all blizzards first
            for b in blizzard_spots:
                b.move(map_spots)
            blizzard_hist.append(set(map(lambda b: b.loc, blizzard_spots)))
            # print(curr_t)

        for m in moves:
            y_diff, x_diff = m
            new_pos = (y + y_diff, x + x_diff)

            if new_pos not in map_spots:
                continue
                
            if new_pos not in blizzard_hist[curr_t + 1]:
                path_q.append((new_pos, curr_t + 1))

        # do nothing
        path_q.append(((y, x), curr_t + 1))

print(solution())
