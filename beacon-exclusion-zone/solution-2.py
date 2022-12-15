input_file = open('beacon-exclusion-zone/input.txt', 'r')
map_lines = input_file.readlines()

MIN_SEARCH = 0
MAX_SEARCH = 4000000

def get_sensors_beacons():
    sensors = []
    beacons = []
    for map_data in map_lines:
        map_data = map_data.strip('\n').split('=')
        sensor_x = int(map_data[1].split(',')[0])
        sensor_y = int(map_data[2].split(':')[0])
        sensors.append((sensor_x, sensor_y))

        beacon_x = int(map_data[3].split(',')[0])
        beacon_y = int(map_data[4])
        beacons.append((beacon_x, beacon_y))
    
    return sensors, beacons

def get_distance(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

def solution():
    sensors, beacons = get_sensors_beacons()
    for y in range(MIN_SEARCH, MAX_SEARCH + 1):
        possibilities = []
        for sensor, beacon in zip(sensors, beacons):
            max_dist = get_distance(sensor, beacon)
            # dist where x = sensor_x
            curr_dist = abs(sensor[1] - y)
            if curr_dist > max_dist:
                continue
            
            diff = max_dist - curr_dist
            # add in zones where beacons cannot be
            possibilities.append((sensor[0] - diff, sensor[0] + diff))
        
        possibilities.sort()
        # look for overlaps in sensor areas and compress them
        compressed = []
        x_min, x_max = possibilities[0]
        for x_i, x_j in possibilities[1:]:
            if x_i - 1 <= x_max:
                x_max = max(x_max, x_j)
            else:
                # no overlap
                compressed.append((x_min, x_max))
                x_min, x_max = x_i, x_j
        compressed.append((x_min, x_max))

        # check if there are potential beacon spots
        if len(compressed) != 1:
            area_1 = compressed[0]
            area_2 = compressed[1]
            # get the in between x value that zones don't cover
            x = (area_2[0] + area_1[1]) // 2
            x = area_1[1] + 1
            return x * MAX_SEARCH + y

print(solution())
