input_file = open('rucksack-reorganization/input.txt', 'r')
rucksack_list = input_file.readlines()

UPPER_CASE_ALPHABET_CAP = 90
UPPER_CASE_ALPHABET_DIFFERENCE = 38
LOWER_CASE_ALPHABET_DIFFERENCE = 96

def get_item_priority(char):
    if ord(char) <= UPPER_CASE_ALPHABET_CAP:
        diff = UPPER_CASE_ALPHABET_DIFFERENCE
    else:
        diff = LOWER_CASE_ALPHABET_DIFFERENCE
    
    return ord(char) - diff

def get_common_item(rucksack_one, rucksack_two):
    for item in rucksack_one:
        if item in rucksack_two:
            return item

def solution():
    total_priority = 0
    for rucksack_item in rucksack_list:
        rucksack_item = rucksack_item.strip('\n')
        rucksack_size = int(len(rucksack_item) / 2)
        # split rucksack into two
        rucksack_one = rucksack_item[:rucksack_size]
        rucksack_two = rucksack_item[rucksack_size:]
        # find first common item
        item = get_common_item(rucksack_one, rucksack_two)
        total_priority += get_item_priority(item)
    
    return total_priority

print(solution())