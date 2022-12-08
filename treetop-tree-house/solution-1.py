input_file = open('treetop-tree-house/input.txt', 'r')
tree_rows = input_file.readlines()

def get_tree_map():
    tree_map = []

    for tree_row in tree_rows:
        tree_row = map(lambda x: int(x), list(tree_row.strip('\n')))
        tree_map.append(list(tree_row))

    return tree_map

def get_edge_tree_count(tree_map):
    x_length = len(tree_map)
    y_length = len(tree_map[0])

    return (x_length - 2) * 2 + (y_length - 2) * 2 + 4 # avoid double counting corners

def get_row_loc(i, j):
    return str(i) + '-' + str(j)

def get_col_loc(i, j):
    return str(j) + '-' + str(i)

def calculate_visible_trees(tree_map, visible_trees, get_loc):
    curr_count = 0

    x_length = len(tree_map)
    y_length = len(tree_map[0])

    for i in range(1, x_length - 1):
        curr_view = tree_map[i]
        for j in range(1, y_length - 1):
            tree_height = curr_view[j]
            first_view = curr_view[:j]
            second_view = curr_view[j+1:]
            # check if trees are visible in either direction
            if tree_height > max(first_view) or tree_height > max(second_view):
                loc = get_loc(i, j)
                if loc not in visible_trees:
                    visible_trees.append(loc)
                    curr_count += 1

    return curr_count

def solution():
    tree_map = get_tree_map()
    visible_trees = []
    visible_tree_count = get_edge_tree_count(tree_map)

    visible_tree_count += calculate_visible_trees(tree_map, visible_trees, get_row_loc)

    # transpose the tree map to iterate by columns naturally
    tree_map_transposed = list(zip(*tree_map))

    # col by col, skip edges
    visible_tree_count += calculate_visible_trees(tree_map_transposed, visible_trees, get_col_loc)
    
    return visible_tree_count

print(solution())
