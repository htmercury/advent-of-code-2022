input_file = open('rock-paper-scissors/input.txt', 'r')
match_lines = input_file.readlines()

PLAY_VALUES = {
    'X': 1,
    'Y': 2,
    'Z': 3
}

MATCH_WIN_POSSIBILITIES = [
    'A Y',
    'B Z',
    'C X'
]

MATCH_TIE_POSSIBILITIES = [
    'A X',
    'B Y',
    'C Z'
]

MATCH_WIN_SCORE = 6
MATCH_TIE_SCORE = 3
MATCH_LOSE_SCORE = 0

def get_match_value(match_string):
    if match_string in MATCH_WIN_POSSIBILITIES:
        return MATCH_WIN_SCORE
    elif match_string in MATCH_TIE_POSSIBILITIES:
        return MATCH_TIE_SCORE
    else:
        return MATCH_LOSE_SCORE

def solution():
    curr_score = 0
    for match in match_lines:
        match_string = match.strip('\n')
        chosen_play = match_string[2]
        curr_score += PLAY_VALUES[chosen_play] + get_match_value(match_string)
    
    return curr_score

print(solution())
