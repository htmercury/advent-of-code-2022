input_file = open('camp-cleanup/input.txt', 'r')
assignment_lines = input_file.readlines()

# calculate overlapping between a and b
def overlaps(a, b):
    a_low, a_high = map(lambda x: int(x), a.split('-'))
    b_low, b_high = map(lambda x: int(x), b.split('-'))

    overlap_a = max(a_low, b_low)
    overlap_b = min(a_high, b_high)

    return overlap_b >= overlap_a 


def solution():
    overlap_value_total = 0
    for assignment_line in assignment_lines:
        assignment_line = assignment_line.strip('\n')
        assignment_one, assignment_two = assignment_line.split(',')
        if overlaps(assignment_one, assignment_two):
            overlap_value_total += 1

    return overlap_value_total


print(solution())

assert(overlaps('5-7', '7-9') == 1)
