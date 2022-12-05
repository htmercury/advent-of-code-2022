import re

input_file = open('supply-stacks/input.txt', 'r')
crate_instruction_inputs = input_file.readlines()

STACK_TOKEN_SIZE = 4

def is_crate_stack(line):
    return '[' in line and ']' in line

def is_instructions(line):
    return 'move' in line

def parse_input():
    crate_stacks = []
    stack_inputs = []
    instructions = []

    for line in crate_instruction_inputs:
        line = line.strip('\n')
        if is_crate_stack(line):
            stack_inputs.append(line)
        elif is_instructions(line):
            instructions.append(line)
        else:
            if len(line) != 0:
                # contains size of create length
                stack_length = max(map(lambda x: int(x), line.split('   ')))
                for _ in range(stack_length):
                    crate_stacks.append([])
    
    # create stacks
    for input in reversed(stack_inputs):
        curr_stack = 0
        i = 0
        while i < len(input):
            element = input[i:i+STACK_TOKEN_SIZE].strip()
            if len(element):
                crate_stacks[curr_stack].append(element[1]) # index 1 of -> [a]
            curr_stack += 1
            i += STACK_TOKEN_SIZE
    
    return crate_stacks, instructions

def perform_action(amount, src, dest, crate_stacks):
    temp_stack = []
    for _ in range(amount):
        temp_stack.append(crate_stacks[src - 1].pop())
    crate_stacks[dest - 1] += reversed(temp_stack)

def get_result(crate_stacks):
    result = ''
    for stack in crate_stacks:
        result += stack.pop()
    
    return result

def solution():
    crate_stacks, instructions = parse_input()

    for instruction in instructions:
        # gather numericals from steps
        step_values = re.split(r"\D+", instruction)
        # clean up empty strings from splitting and convert to int
        amount, src, dest = map(lambda x: int(x), ' '.join(step_values).split())
        perform_action(amount, src, dest, crate_stacks)
    
    return get_result(crate_stacks)

print(solution())
