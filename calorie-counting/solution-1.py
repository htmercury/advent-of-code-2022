input_file = open('calorie-counting/input.txt', 'r')
calorie_lines = input_file.readlines()

def parse_inputs(lines):
    elf_inventory = []
    curr_amount = 0
    for line in lines:
        if line != '\n':
            curr_amount += int(line)
        else:
            elf_inventory.append(curr_amount)
            curr_amount = 0

    return elf_inventory


def solution():
    elf_inventory = parse_inputs(calorie_lines)
    return max(elf_inventory)

print(solution())