input_file = open('rucksack-reorganization/input.txt', 'r')
rucksack_list = input_file.readlines()

UPPER_CASE_ALPHABET_CAP = 90
UPPER_CASE_ALPHABET_DIFFERENCE = 38
LOWER_CASE_ALPHABET_DIFFERENCE = 96

GROUP_SIZE = 3

def get_item_priority(char):
    if ord(char) <= UPPER_CASE_ALPHABET_CAP:
        diff = UPPER_CASE_ALPHABET_DIFFERENCE
    else:
        diff = LOWER_CASE_ALPHABET_DIFFERENCE
    
    return ord(char) - diff

def get_group_badge(rucksack_one, rucksack_two, rucksack_three):
    for item in rucksack_one:
        if item in rucksack_two and item in rucksack_three:
            return item

def solution():
    total_priority = 0
    for i in range(0, len(rucksack_list), GROUP_SIZE):
        # split rucksack into two
        rucksack_one = rucksack_list[i].strip('\n')
        rucksack_two = rucksack_list[i + 1].strip('\n')
        rucksack_three = rucksack_list[i + 2].strip('\n')
        # find first common item
        item = get_group_badge(rucksack_one, rucksack_two, rucksack_three)
        total_priority += get_item_priority(item)
    
    return total_priority

print(solution())