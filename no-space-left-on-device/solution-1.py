input_file = open('no-space-left-on-device/input.txt', 'r')
console_output = input_file.readlines()

COMMAND_CD = 'cd'
CD_ROOT = '/'
CD_PREVIOUS = '..'
OUTPUT_DIR = 'dir'
DIR_MAX_SIZE = 100000

def is_command(console_line):
    return console_line[0] == '$'

def add_directory(dir_name, fs_path, fs_tree):
    curr_spot = fs_tree
    for folder in fs_path:
        curr_spot = curr_spot[folder]
    if dir_name not in curr_spot:
        curr_spot[dir_name] = {}

def add_file(file_name, file_size, fs_path, fs_tree):
    curr_spot = fs_tree
    for folder in fs_path:
        curr_spot = curr_spot[folder]
    curr_spot[file_name] = int(file_size)

def perform_command(console_line, fs_path, fs_tree):
    if COMMAND_CD in console_line:
        target_loc = console_line.split(COMMAND_CD)[1].strip()
        if target_loc == CD_ROOT:
            fs_path = []
        elif target_loc == CD_PREVIOUS:
            fs_path.pop()
        else:
            add_directory(target_loc, fs_path, fs_tree)
            # update curr path
            fs_path.append(target_loc)    

def parse_output(console_line, fs_path, fs_tree):
    if OUTPUT_DIR in console_line:
        target_loc = console_line.split(OUTPUT_DIR)[1].strip()
        add_directory(target_loc, fs_path, fs_tree)
    else:
        # add file value
        file_size, file_name = map(lambda x: x.strip(), console_line.split(' '))
        add_file(file_name, file_size, fs_path, fs_tree)

def create_fs_tree():
    fs_path = []
    fs_tree = {}
    for console_line in console_output:
        if is_command(console_line):
            perform_command(console_line, fs_path, fs_tree)
        else:
            parse_output(console_line, fs_path, fs_tree)
    return fs_tree

def sum_of_dir(fs_obj):
    if isinstance(fs_obj, int):
        return fs_obj
    else:
        sum = 0
        for dir in fs_obj:
            sum += sum_of_dir(fs_obj[dir])
        return sum

def traverse_fs_tree(fs_obj, result):
    total_dir_size = sum_of_dir(fs_obj)
    if not isinstance(fs_obj, int):
        if total_dir_size < DIR_MAX_SIZE:
            result.append(total_dir_size)
        
        for dir in fs_obj:
            traverse_fs_tree(fs_obj[dir], result)
    
def solution():
    answer = []
    fs_tree = create_fs_tree()
    traverse_fs_tree(fs_tree, answer)
    return sum(answer)

print(solution())
