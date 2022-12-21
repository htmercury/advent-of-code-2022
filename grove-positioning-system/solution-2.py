input_file = open('grove-positioning-system/input.txt', 'r')
encrypted_lines = input_file.readlines()

DECRYPTION_KEY = 811589153

class Node:
    def __init__(self, value):
        self.prev = None
        self.next = None
        self.value = value

    def move(self, num_nodes):
        shift_amount = self.value % (num_nodes - 1)
        self.prev.next = self.next
        self.next.prev = self.prev

        curr_n = self.next
        for _ in range(shift_amount):
            # move up
            curr_n = curr_n.next

        self.next = curr_n
        self.prev = curr_n.prev

        self.next.prev = self
        self.prev.next = self

def create_node_list():
    node_list = []
    prev_node = None
    for line in encrypted_lines:
        value = int(line.strip('\n')) * DECRYPTION_KEY
        curr_node = Node(value)
        if value == 0:
            target_node = curr_node
        if prev_node:
            curr_node.prev = prev_node
            prev_node.next = curr_node
        node_list.append(curr_node)
        prev_node = curr_node

    # circular linked
    node_list[0].prev = node_list[-1]
    node_list[-1].next = node_list[0]

    # print(list(map(lambda n: n.value, node_list)))

    return node_list, target_node

def solution():
    node_list, target_node = create_node_list()
    num_nodes = len(node_list)
    results = []

    for _ in range(10):
        for n in node_list:
            n.move(num_nodes)
            # print(n.value, 'moves between', n.prev.value, 'and', n.next.value)

    for _ in range(3):
        for _ in range(1000):
            target_node = target_node.next
        results.append(target_node.value)
    
    return sum(results)

print(solution())
