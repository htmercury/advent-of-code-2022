input_file = open('beacon-exclusion-zone/input.txt', 'r')
map_lines = input_file.readlines()

TARGET_Y = 2000000

def get_distance(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

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

def solution():
    sensors, beacons = get_sensors_beacons()
    extras = set()
    blanks = set()
    moves = [-1, 1]
    for sensor, beacon in zip(sensors, beacons):
        if beacon[1] == TARGET_Y:
            extras.add(beacon)
        
        max_dist = get_distance(sensor, beacon)

        for direction in moves:
            # start at sensor x and expand out
            mid_dist = abs(sensor[1] - TARGET_Y)
            mid_x = sensor[0]
            while mid_dist <= max_dist:
                blanks.add((mid_x, TARGET_Y))
                mid_x += direction
                mid_dist += 1
    
    return len(blanks - extras)

print(solution())
