input_file = open('monkey-match/input.txt', 'r')
monkey_lines = input_file.readlines()

class Node:
    def __init__(self, value = None) -> None:
        self.value = value
        self.left = None
        self.right = None
        self.operation = None

operations = {
    '+': lambda a: lambda b: a + b,
    '-': lambda a: lambda b: a - b,
    '*': lambda a: lambda b: a * b,
    '/': lambda a: lambda b: a // b
}

reverse_operations = {
    '+': operations['-'],
    '-': operations['+'],
    '/': operations['*'],
    '*': operations['/'],
}

def create_binary_tree():
    nodes = {}
    children = []
    for monkey in monkey_lines:
        data = monkey.strip('\n').split(' ')
        name = data[0][:-1]
        if len(data) == 2:
            new_node = Node(int(data[1]))
            nodes[name] = new_node
        else:
            operation = data[2]
            children.append((name, data[1], data[3], operation))
            nodes[name] = Node()

    for name, child_one, child_two, operation in children:
        nodes[name].left = nodes[child_one]
        nodes[name].right = nodes[child_two]
        nodes[name].operation = operation

    return nodes

def compute_node(node):
    if node.value:
        return node.value
    else:
        return operations[node.operation](compute_node(node.left))(compute_node(node.right))

def contains_humn(node):
    if node.value:
        return True if node.value == 'x' else False
    else:
        return contains_humn(node.left) or contains_humn(node.right)

def reverse_calculate(node, target_value):
    if node.value == 'x':
        return target_value
    
    if contains_humn(node.right):
        if node.operation == '+' or node.operation == '*':
            return reverse_calculate(node.right, reverse_operations[node.operation](target_value)(compute_node(node.left)))
        else:
            return reverse_calculate(node.right, operations[node.operation](compute_node(node.left))(target_value))
    else:
        return reverse_calculate(node.left, reverse_operations[node.operation](target_value)(compute_node(node.right)))

def solution():
    nodes = create_binary_tree()
    nodes['humn'].value = 'x'

    rootl_node = nodes['root'].left
    rootr_node = nodes['root'].right

    if contains_humn(rootl_node):
        target_value = compute_node(rootr_node)
        humn_root = rootl_node
    else:
        target_value = compute_node(rootl_node)
        humn_root = rootr_node

    # solve for x in order for both subtrees to be equal
    nodes['humn'].value = reverse_calculate(humn_root, target_value)
    assert compute_node(rootl_node) == compute_node(rootr_node)

    return nodes['humn'].value

print(solution())
