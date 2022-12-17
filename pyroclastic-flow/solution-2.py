block_lines = open('pyroclastic-flow/blocks.txt', 'r').readlines()

input_file = open('pyroclastic-flow/input.txt', 'r')
cave_pattern = input_file.readlines()[0]

CHAMBER_WIDTH = 7
LEFT_SPAWN = 2
BOTTOM_SPAWN = 3
BLOCK_COUNT = 1000000000000

def get_blocks():
    blocks = []
    curr_block = []
    y_offset = 0
    # blocks are sorted this way this the lowest height points at the beginning
    for j, line in enumerate(reversed(block_lines)):
        line = line.strip('\n')
        for i, char in enumerate(line):
            if char == '#':
                curr_block = curr_block + [(j - y_offset, i)]
        
        if len(line) == 0:
            blocks = [curr_block] + blocks
            y_offset = j + 1
            curr_block = []
    blocks = [curr_block] + blocks # append backwards since we are parsing input file in reverse

    return blocks

def move_block(block, vertical_chamber, direction):
    can_move = True
    new_block = []
    for j, i in block:
        new_pos = i + direction
        if new_pos >= CHAMBER_WIDTH or new_pos < 0 or (j, new_pos) in vertical_chamber:
            can_move = False
        new_block.append((j, new_pos))
    if can_move:
        return new_block
    else:
        return block

def check_and_move_block_down(block, vertical_chamber):
    new_block = []
    can_move = True
    for j, i in block:
        if j == 0 or (j - 1, i) in vertical_chamber:
            can_move = False
        new_block.append((j - 1, i))
    if can_move:
        return can_move, new_block
    else:
        return can_move, block

def find_cycles(blocks, vertical_chamber):
    curr_move = 0
    max_height = 0

    # sliding window to keep track of changes for last 10 blocks
    changes = []
    sliding_window = []
    history = {}

    for block_idx in range(BLOCK_COUNT):
        curr_block = block_idx % len(blocks)
        spawned_block = []

        for j, i in blocks[curr_block]:
            spawned_block.append((j + max_height + BOTTOM_SPAWN, i + LEFT_SPAWN))

        is_done = False
        while not is_done:
            curr_move = curr_move % len(cave_pattern)

            if cave_pattern[curr_move] == '>':
                spawned_block = move_block(spawned_block, vertical_chamber, 1)
            else:
                spawned_block = move_block(spawned_block, vertical_chamber, -1)

            did_move, spawned_block = check_and_move_block_down(spawned_block, vertical_chamber)

            if not did_move:
                # block is fixed
                is_done = True
            
            curr_move += 1
       
        diff = max(spawned_block[-1][0] + 1 - max_height, 0)
        state = (curr_block, curr_move, diff)

        if state in history:
            # find how many blocks has been added since the last matched state
            cycle_length = block_idx - history[state]

            # check if last 10 blocks of the last cycle matches the current cycle
            if sliding_window == changes[-cycle_length - 10:-cycle_length]:
                return changes, cycle_length

        history[state] = block_idx
        changes.append(diff)

        if len(sliding_window) >= 10:
            sliding_window.pop(0)
        sliding_window.append(diff)

        # get the max placed height and update
        max_height = max(max_height, spawned_block[-1][0] + 1)
        for (j, i) in spawned_block:
            vertical_chamber.add((j, i))


def render_board(vertical_chamber, max_height):
    board = []
    for _ in range(max_height + 1):
        board.append(['🟩'] * CHAMBER_WIDTH)

    for (j, i) in vertical_chamber:
        board[j][i] = '🟥'

    board.reverse()
    for row in board:
        print(''.join(row))

def solution():
    blocks = get_blocks()
    vertical_chamber = set()
    changes, cycle_length = find_cycles(blocks, vertical_chamber)

    cycle_start = len(changes) - cycle_length
    before_cycle_changes = changes[:cycle_start]

    cycles_left = (BLOCK_COUNT - cycle_start) // cycle_length
    remaining_blocks = BLOCK_COUNT - cycles_left * cycle_length - cycle_start

    return sum(before_cycle_changes) + sum(changes[cycle_start:]) * cycles_left + sum(changes[cycle_start:][:remaining_blocks])

print(solution())
