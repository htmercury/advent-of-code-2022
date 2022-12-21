input_file = open('not-enough-minerals/input.txt', 'r')
blueprint_lines = input_file.readlines()

blueprints = []

for line in blueprint_lines:
    resources = list(map(lambda s: int(s), filter(lambda s: s.isnumeric(), line.split(' '))))
    blueprints.append(
        {
            'geode': {
                'ore': resources[4],
                'obsidian': resources[5]
            },
            'obsidian': {
                'ore': resources[2],
                'clay': resources[3]
            },
            'clay': {
                'ore': resources[1]
            },
            'ore': {
                'ore': resources[0]
            },
        }
    )

def can_build(inventory, robot_blueprint):
    items_needed = robot_blueprint.keys()
    return all(map(lambda item: inventory[item] >= robot_blueprint[item], items_needed))

def could_build(generator, robot_blueprint):
    items_needed = robot_blueprint.keys()
    return all(map(lambda item: generator[item] > 0, items_needed))

def get_max_craft_robots(blueprint):
    return {
        'ore': max(blueprint['ore']['ore'], blueprint['geode']['ore'], blueprint['obsidian']['ore'], blueprint['clay']['ore']),
        'clay': blueprint['obsidian']['clay'],
        'obsidian': blueprint['geode']['obsidian'],
        'geode': 99
    }

MAX_TIME = 24

cache = {}

def get_state(inventory, generator, t):
    return (inventory['ore'], inventory['clay'], inventory['obsidian'], inventory['geode'], generator['ore'], generator['clay'], generator['obsidian'], generator['geode'], t)

def find_plan_geode_max(chosen_blueprint):
    robot_q = []
    robot_q.append(({ 'ore': 0, 'clay': 0, 'obsidian': 0, 'geode': 0 }, { 'ore': 1, 'clay': 0, 'obsidian': 0, 'geode': 0 }, 0))
    results = []

    visited = set()

    max_geodes_history = {}
    max_craft_robots = get_max_craft_robots(chosen_blueprint)
    print(max_craft_robots)
    while len(robot_q) != 0:
        inventory, generator, t = robot_q.pop()

        if t > 24:
            continue

        state = get_state   (inventory, generator, t)

        if state in visited:
            continue
        else:
            visited.add(state)

        if t not in max_geodes_history or inventory['geode'] >= max_geodes_history[t]:
            max_geodes_history[t] = inventory['geode']
        else:
            continue

        if t == 24:
            # print('time reached', inventory, generator)
            results.append(inventory)

        new_inventory = inventory.copy()
        for item in generator.keys():
            new_inventory[item] += generator[item]
        

        for i, robot in enumerate(chosen_blueprint.keys()):
            if max_craft_robots[robot] > generator[robot]:
                if can_build(inventory, chosen_blueprint[robot]):
                    # print('crafting ', robot, t, inventory)
                    # create robot
                    modded_inventory = new_inventory.copy()
                    for item in chosen_blueprint[robot].keys():
                        modded_inventory[item] -= chosen_blueprint[robot][item]
                    # update generator
                    new_generator = generator.copy()
                    new_generator[robot] += 1
                    
                    robot_q.append((modded_inventory, new_generator, t + 1))
                    if robot == 'obsidian':
                        break
                elif could_build(generator, chosen_blueprint[robot]):
                    waiting_time = 0
                    modded_inventory = new_inventory.copy()
                    while not can_build(modded_inventory, chosen_blueprint[robot]):
                        waiting_time += 1
                        for item in generator.keys():
                            modded_inventory[item] += generator[item]
                    robot_q.append((modded_inventory, generator, t + 1 + waiting_time))
            

    print(max(list(map(lambda r: r['geode'], results))))
    return max(list(map(lambda r: r['geode'], results)))

result = 0
for i, chosen_blueprint in enumerate(blueprints, start=1):
    print('plan', i)
    result += i * find_plan_geode_max(chosen_blueprint)

print(result)