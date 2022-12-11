input_file = open('monkey-in-the-middle/input.txt', 'r')
monkey_data = input_file.readlines()

ROUNDS = 20

def create_monkeys():
    monkeys = []
    new_monkey = {}
    test_steps = []
    for data in monkey_data:
        if 'Starting items' in data:
            items = data.strip().split(',')
            items[0] = items[0].split(':')[1]
            items = map(lambda x: int(x), items)
            new_monkey['starting_items'] = list(items)
        if 'Operation' in data:
            if '+' in data:
                delta = data.split('+')[1]
                if 'old' in delta:
                    new_monkey['operation'] = lambda x: x + x
                else:
                    new_monkey['operation'] = (lambda delta: lambda x: x + delta)(int(delta))
            else:
                delta = data.split('*')[1]
                if 'old' in delta:
                    new_monkey['operation'] = lambda x: x * x
                else:
                    new_monkey['operation'] = (lambda delta: lambda x: x * delta)(int(delta))
        if 'Test' in data or 'If' in data:
            test_steps.append(data)

        if len(test_steps) == 3:
            delta = int(test_steps[0].split(' ')[-1])
            monkey_one = int(test_steps[1].split(' ')[-1])
            monkey_two = int(test_steps[2].split(' ')[-1])
            new_monkey['test'] = (lambda delta: lambda monkey_one: lambda monkey_two: lambda x: monkey_one if x % delta == 0 else monkey_two)(delta)(monkey_one)(monkey_two)
            new_monkey['inspection_count'] = 0
            monkeys.append(new_monkey)
            new_monkey = {}
            test_steps = []
    
    return monkeys

def solution():
    monkeys = create_monkeys()
    for _ in range(ROUNDS):
        for monkey in monkeys:
            while len(monkey['starting_items']) != 0:
                monkey['inspection_count'] += 1
                item = monkey['starting_items'].pop(0)
                item = monkey['operation'](item)
                item = int(item / 3)
                target = monkey['test'](item)
                monkeys[target]['starting_items'].append(item)
    inspection_list = list(map(lambda x: x['inspection_count'], monkeys))
    inspection_list.sort(reverse=True)

    return inspection_list[0] * inspection_list[1]

print(solution())
