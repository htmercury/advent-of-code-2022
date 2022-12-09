input_file = open('rope-bridge/input.txt', 'r')
commands = input_file.readlines()

MAX_LENGTH_ROPE = 10

movement = {
    'U': [0, 1],
    'D': [0, -1],
    'L': [-1, 0],
    'R': [1, 0]
}

def sign(value):
    return (value > 0) - (value < 0)

class pos():
    def __init__(self, x=0, y=0) -> None:
        self.x = x
        self.y = y
    
    def __str__(self) -> str:
        return str(self.x) + '-' + str(self.y)

    def move(self, direction):
        self.x += movement[direction][0]
        self.y += movement[direction][1]

    def is_touching(self, other):
        return abs(other.x - self.x) <= 1 and abs(other.y - self.y) <= 1

    def follow(self, other):
        if not self.is_touching(other):
            self.y += sign(other.y - self.y)
            self.x += sign(other.x - self.x)

knots = []

for _ in range(10):
    knots.append(pos())

visited = []
visited.append(str(pos()))

for command in commands:
    direction = command[0]
    amount = int(command[1:].strip())

    for _ in range(amount):
        knots[0].move(direction)
        for i in range(1, MAX_LENGTH_ROPE):
            knots[i].follow(knots[i-1])

        if str(knots[MAX_LENGTH_ROPE - 1]) not in visited:
            visited.append(str(knots[MAX_LENGTH_ROPE - 1]))

print(len(visited))
