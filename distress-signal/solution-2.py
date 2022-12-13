import functools

input_file = open('distress-signal/input.txt', 'r')
signal_lines = input_file.readlines()

TARGET_ONE = [[2]]
TARGET_TWO = [[6]]

def get_packets():
    packets = []
    for signal in signal_lines:
        signal = signal.strip('\n')
        if len(signal) != 0:
            packets.append(eval(signal))

    packets.append(TARGET_ONE)
    packets.append(TARGET_TWO)

    return packets

def compare_values(value_one, value_two):
    if isinstance(value_one, int) and isinstance(value_two, int):
        return value_one - value_two
    elif isinstance(value_one, list) and isinstance(value_two, list):
        min_length = min(len(value_one), len(value_two))
        for i in range(min_length):
            diff = compare_values(value_one[i], value_two[i])
            if diff != 0:
                return diff
        # compare list lengths if no evaluation
        return len(value_one) - len(value_two)
    elif isinstance(value_one, int) and isinstance(value_two, list):
        return compare_values([value_one], value_two)
    else:
        return compare_values(value_one, [value_two])

def solution():
    packets = get_packets()
    result = sorted(packets, key=functools.cmp_to_key(compare_values))
    return (result.index(TARGET_ONE) + 1) * (result.index(TARGET_TWO) + 1)

print(solution())
