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

def solution():
    nodes = create_binary_tree()

    return compute_node(nodes['root'])

print(solution())
