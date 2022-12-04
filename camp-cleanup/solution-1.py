input_file = open('camp-cleanup/input.txt', 'r')
assignment_lines = input_file.readlines()

# does a fully contain b
def contains(a, b):
    a_low, a_high = map(lambda x: int(x), a.split('-'))
    b_low, b_high = map(lambda x: int(x), b.split('-'))

    if a_low <= b_low and a_high >= b_high:
        return True
    else:
        return False


def solution():
    fully_contained_pairs = 0
    for assignment_line in assignment_lines:
        assignment_line = assignment_line.strip('\n')
        assignment_one, assignment_two = assignment_line.split(',')
        if contains(assignment_one, assignment_two) or contains(assignment_two, assignment_one):
            fully_contained_pairs += 1

    return fully_contained_pairs


print(solution())

assert(contains('4-6', '6-6') == True)
assert(contains('2-8', '3-7') == True)
