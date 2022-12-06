input_file = open('tuning-trouble/input.txt', 'r')
input_list = input_file.readlines()
input_str = input_list[0]

TOKEN_SIZE = 14

def solution(input):
    i = 0
    while i+TOKEN_SIZE < len(input):
        if len(set(input[i:i+TOKEN_SIZE])) == TOKEN_SIZE:
            return i+TOKEN_SIZE
        i += 1

print(solution(input_str))

assert(solution('mjqjpqmgbljsphdztnvjfqwrcgsmlb') == 19)
assert(solution('bvwbjplbgvbhsrlpgdmjqwftvncz') == 23)
assert(solution('nppdvjthqldpwncqszvftbrmjlhg') == 23)
assert(solution('nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg') == 29)
assert(solution('zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw') == 26)
