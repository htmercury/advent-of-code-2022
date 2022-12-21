input_file = open('not-enough-minerals/input.txt', 'r')
blueprint_lines = input_file.readlines()

MAX_TIME = 32

def create_resource_object(ore_n = -1, clay_n = -1, obsidian_n = -1, geode_n = -1):
    obj =  { 'ore': ore_n, 'clay': clay_n, 'obsidian': obsidian_n, 'geode': geode_n }

    return { key:value for key,value in obj.items() if value != -1 }
    
def get_blueprints():
    blueprints = []
    for line in blueprint_lines:
        resources = list(map(lambda s: int(s), filter(lambda s: s.isnumeric(), line.split(' '))))
        blueprints.append(
            {
                'geode': create_resource_object(ore_n=resources[4], obsidian_n=resources[5]),
                'obsidian': create_resource_object(ore_n=resources[2], clay_n=resources[3]),
                'clay': create_resource_object(ore_n=resources[1]),
                'ore': create_resource_object(ore_n=resources[0]),
            }
        )
    
    return blueprints

def can_build(inventory, robot_blueprint):
    items_needed = robot_blueprint.keys()
    return all(map(lambda item: inventory[item] >= robot_blueprint[item], items_needed))

def could_build(generator, robot_blueprint):
    items_needed = robot_blueprint.keys()
    return all(map(lambda item: robot_blueprint[item] == 0 or generator[item] > 0, items_needed))

def get_max_craft_robots(blueprint):
    return {
        'ore': max(blueprint['ore']['ore'], blueprint['geode']['ore'], blueprint['obsidian']['ore'], blueprint['clay']['ore']),
        'clay': blueprint['obsidian']['clay'],
        'obsidian': blueprint['geode']['obsidian'],
        'geode': 99
    }

def get_state(inventory, generator, t):
    return (*inventory.values(), *generator.values(), t)

def find_plan_geode_max(chosen_blueprint):
    robot_q = []
    robot_q.append((create_resource_object(0, 0, 0, 0), create_resource_object(1, 0, 0, 0), 0))

    visited = set()

    max_geodes_history = {}
    max_craft_robots = get_max_craft_robots(chosen_blueprint)
    while len(robot_q) != 0:
        inventory, generator, t = robot_q.pop()

        if t > MAX_TIME:
            continue

        state = get_state(inventory, generator, t)
        if state in visited:
            continue
        else:
            visited.add(state)


        if t not in max_geodes_history or inventory['geode'] >= max_geodes_history[t]:
            max_geodes_history[t] = inventory['geode']
        else:
            continue

        new_inventory = inventory.copy()
        for item in generator.keys():
            new_inventory[item] += generator[item]

        for robot in chosen_blueprint.keys():
            if max_craft_robots[robot] > generator[robot]:
                if can_build(inventory, chosen_blueprint[robot]):

                    modded_inventory = new_inventory.copy()
                    for item in chosen_blueprint[robot].keys():
                        modded_inventory[item] -= chosen_blueprint[robot][item]
                    
                    # update generator
                    new_generator = generator.copy()
                    new_generator[robot] += 1
                    
                    robot_q.append((modded_inventory, new_generator, t + 1))

                    if robot == 'obsidian':
                        # if we can build geode or obsidian bot, don't do anything else
                        break
                elif could_build(generator, chosen_blueprint[robot]):
                    waiting_time = 0
                    modded_inventory = new_inventory.copy()
                    while not can_build(modded_inventory, chosen_blueprint[robot]):
                        waiting_time += 1
                        for item in generator.keys():
                            modded_inventory[item] += generator[item]
                    robot_q.append((modded_inventory, generator, t + 1 + waiting_time))
            
    return max_geodes_history[MAX_TIME]

def solution():
    blueprints = get_blueprints()
    result = 1
    for i in range(3):
        # print('plan', i)
        result *= find_plan_geode_max(blueprints[i])

    return result

print(solution())
