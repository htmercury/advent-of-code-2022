input_file = open('cathode-ray-tube/input.txt', 'r')
command_list = input_file.readlines()

COMMAND_ADD = 'addx'
COMMAND_LENGTH = 4

cycle_targets = [20, 60, 100, 140, 180, 220]

def calc_signal(register_value, cycle):
    return register_value * cycle

def perform_noop(total_signal, register_value, cycle):
    cycle += 1
    if cycle in cycle_targets:
        total_signal += calc_signal(register_value, cycle)
    
    return total_signal, cycle

def perform_addx(total_signal, register_value, cycle, add_amount):
    for _ in range(2):
        total_signal, cycle = perform_noop(total_signal, register_value, cycle)
    register_value += add_amount
    
    return total_signal, cycle, register_value

def solution():
    total_signal = 0
    curr_cycle = 0
    register_value = 1

    for command in command_list:
        if command[:4] == COMMAND_ADD:
            add_param = int(command[COMMAND_LENGTH:])
            total_signal, curr_cycle, register_value = perform_addx(total_signal, register_value, curr_cycle, add_param)
        else:
            # noop
            total_signal, curr_cycle = perform_noop(total_signal, register_value, curr_cycle)
    
    return total_signal

print(solution())
