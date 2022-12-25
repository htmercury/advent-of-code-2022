input_file = open('full-of-hot-air/input.txt', 'r')
snafu_data = input_file.readlines()

BASE_VALUE = 5

snafu_vars = {
    '2': 2,
    '1': 1,
    '0': 0,
    '-': -1,
    '=': -2
}

def get_total():
    total = 0
    for snafu in snafu_data:
        snafu = snafu.strip('\n')
        decimal = 0
        curr_pow = 0
        for char in reversed(snafu):
            curr_spot = BASE_VALUE**curr_pow
            decimal += snafu_vars[char] * curr_spot
            curr_pow += 1
        
        total += decimal
    
    return total

def get_snafu(decimal):
    if decimal == 0:
        return ''

    remainder = decimal % BASE_VALUE

    if remainder == 0:
        return get_snafu(decimal // BASE_VALUE) + '0'
    elif remainder == 1:
        return get_snafu(decimal // BASE_VALUE) + '1'
    elif remainder == 2:
        return get_snafu(decimal // BASE_VALUE) + '2'
    elif remainder == 3:
        # use = (-2) value e.g., 5 - 2 = 3
        return get_snafu((decimal + 2) // BASE_VALUE) + '='
    elif remainder == 4:
        return get_snafu((decimal + 1) // BASE_VALUE) + '-'

def solution():
    total_value = get_total()

    return get_snafu(total_value)

print(solution())
