input_file = open('cathode-ray-tube/input.txt', 'r')
command_list = input_file.readlines()

COMMAND_ADD = 'addx'
COMMAND_LENGTH = 4

cycle_targets = [40, 80, 120, 160, 200, 240]

def get_sprite_pos(register_value):
    return [register_value -1, register_value, register_value + 1]

def perform_noop(sprite, sprite_pos, cycle, image, image_list):
    cycle += 1
    if sprite in sprite_pos:
        image += '#'
    else:
        image += '.'
    sprite += 1
    if cycle in cycle_targets:
        image_list.append(image)
        image = ''
        sprite = 0
        cycle = 0
    
    return sprite, cycle, image

def perform_addx(sprite, sprite_pos, cycle, image, image_list, register_value, add_amount):
    for _ in range(2):
        sprite, cycle, image = perform_noop(sprite, sprite_pos, cycle, image, image_list)

    register_value += add_amount
    
    return sprite, cycle, image, register_value

def solution():
    curr_cycle = 0
    curr_sprite = 0
    register_value = 1
    sprite_pos = get_sprite_pos(register_value)

    image = ''
    image_list = []

    for command in command_list:
        if command[:4] == COMMAND_ADD:
            add_param = int(command[COMMAND_LENGTH:])
            curr_sprite, curr_cycle, image, register_value = perform_addx(curr_cycle, sprite_pos, curr_cycle, image, image_list, register_value, add_param)
            sprite_pos = get_sprite_pos(register_value)
        else:
            # noop
            curr_sprite, curr_cycle, image = perform_noop(curr_sprite, sprite_pos, curr_cycle, image, image_list)

    for img in image_list:
        print(img, len(img))

solution()
