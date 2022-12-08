input_file = open('treetop-tree-house/input.txt', 'r')
tree_rows = input_file.readlines()

def get_tree_map():
    tree_map = []

    for tree_row in tree_rows:
        tree_row = map(lambda x: int(x), list(tree_row.strip('\n')))
        tree_map.append(list(tree_row))

    return tree_map

def get_row_loc(i, j):
    return str(i) + '-' + str(j)

def get_col_loc(i, j):
    return str(j) + '-' + str(i)

def get_scenic_score(tree_list, tree_height):
    score = 1
    i = 0
    
    while i < len(tree_list) - 1 and tree_height > tree_list[i]:
        i += 1
        score += 1
    
    return score

def calculate_scenic_trees(tree_map, scenic_trees, get_loc):
    x_length = len(tree_map)
    y_length = len(tree_map[0])

    for i in range(1, x_length - 1):
        curr_view = tree_map[i]
        for j in range(1, y_length - 1):
            scenic_score = 1

            tree_height = curr_view[j]
            first_view = curr_view[:j]
            second_view = curr_view[j+1:]
            # get scores for both directions
            scenic_score *= get_scenic_score(list(reversed(first_view)), tree_height)
            scenic_score *= get_scenic_score(second_view, tree_height)

            loc = get_loc(i, j)
            if loc not in scenic_trees:
                scenic_trees[loc] = scenic_score
            else:
                scenic_trees[loc] *= scenic_score

def solution():
    tree_map = get_tree_map()
    scenic_trees = {}
    calculate_scenic_trees(tree_map, scenic_trees, get_row_loc)

    # transpose the tree map to iterate by columns naturally
    tree_map_transposed = list(zip(*tree_map))

    # col by col, skip edges
    calculate_scenic_trees(tree_map_transposed, scenic_trees, get_col_loc)
    
    return max(list(scenic_trees.values()))

print(solution())
