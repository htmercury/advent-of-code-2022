input_file = open('rock-paper-scissors/input.txt', 'r')
match_lines = input_file.readlines()

PLAY_VALUES = {
    'X': 1,
    'Y': 2,
    'Z': 3
}

MATCH_WIN_OPTIONS = {
    'A': 'Y',
    'B': 'Z',
    'C': 'X'
}

MATCH_TIE_OPTIONS = {
    'A': 'X',
    'B': 'Y',
    'C': 'Z'
}

MATCH_LOSE_OPTIONS = {
    'A': 'Z',
    'B': 'X',
    'C': 'Y'
}

MATCH_WIN_SCORE = 6
MATCH_TIE_SCORE = 3
MATCH_LOSE_SCORE = 0

MATCH_VALUES = {
    'X': MATCH_LOSE_SCORE,
    'Y': MATCH_TIE_SCORE,
    'Z': MATCH_WIN_SCORE
}

def get_total_match_value(chosen_strat, opponent_play):
    match_score = MATCH_VALUES[chosen_strat]

    if match_score is MATCH_WIN_SCORE:
        chosen_play = MATCH_WIN_OPTIONS[opponent_play]
    elif match_score is MATCH_TIE_SCORE:
        chosen_play = MATCH_TIE_OPTIONS[opponent_play]
    else:
        chosen_play = MATCH_LOSE_OPTIONS[opponent_play]

    match_score += PLAY_VALUES[chosen_play]
    return match_score

def solution():
    curr_score = 0
    for match in match_lines:
        match_string = match.strip('\n')
        opponent_play = match_string[0]
        chosen_strat = match_string[2]
        curr_score += get_total_match_value(chosen_strat, opponent_play)
    
    return curr_score

print(solution())
