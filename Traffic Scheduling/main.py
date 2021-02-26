stimulation_time = 0
no_intersections = 0
no_street = 0
no_cars = 0
reward = 0

city_map_name = {}
city_map_name_reverse = {}
city_map_delay = {}
car_path = {}

no_incom_rd = {}
need_scheduling = []

# compute:
intersection_needed = 0
# schedule_data={
#     1:[2,"street1",2,"street2",1],
#     0:[2,"street1",2,"street2",1],
#     2:[2,"street1",2,"street2",1],
# }

schedule_data = {}


filename = "c.txt"


# a.txt
# b.txt
# c.txt
# d.txt
# e.txt
# f.txt

def displayData():
    print("\n")
    print("ST: ", stimulation_time)
    print("IC: ", no_intersections)
    print("SC: ", no_street)
    print("CC: ", no_cars)
    print("reward: ", reward)
    print("city map: ")
    for city in list(city_map_name.keys()):
        print(city, city_map_name[city])
    print("path delay: ")
    for path in city_map_delay:
        print(path, city_map_delay[path])
    print("car path:")
    for car in car_path:
        print(car_path[car])
    print("\n")


def readFile():
    global stimulation_time, no_intersections, no_cars, reward, no_street, no_incom_rd
    with open(filename, 'r') as fin:
        stimulation_time, no_intersections, no_street, no_cars, reward = list(
            map(int, fin.readline().split()))
        i = 0

        while(i < no_street):

            x, y, name, delay = fin.readline().split()

            city_map_name[name] = (int(x), int(y))
            city_map_name_reverse[(int(x), int(y))] = name
            city_map_delay[(int(x), int(y))] = int(delay)
            if(int(y) not in list(no_incom_rd.keys())):
                no_incom_rd[int(y)] = []
            no_incom_rd[int(y)].append(name)
            i += 1

        i = 0
        while(i < no_cars):
            car_path[i] = ([city_map_name[city]
                            for city in fin.readline().split()[1:]])
            i += 1

    print("Read file!")


def findNumOfCars(i):
    count = 0
    for path in car_path:
        for x, y in car_path[path]:
            if y == i:
                count += 1
    return count


def schedule():
    global intersection_needed
    #print(no_incom_rd)
    for node in list(no_incom_rd.keys()):
        if len(no_incom_rd[node]) == 1:
            intersection_needed += 1
            schedule_data[node] = [1]
            for road in no_incom_rd[node]:
                schedule_data[node].append(road)
                schedule_data[node].append(1)
        elif len(no_incom_rd[node]) > 1:
            intersection_needed += 1
            schedule_data[node] = [len(no_incom_rd[node])]
            numberOfcars = findNumOfCars(node)
            if(numberOfcars > 10):
                numberOfcars //= 10*(len(str(numberOfcars))-1)
            if(numberOfcars == 0):
                numberOfcars = 1            
            # print(numberOfcars)
            for road in no_incom_rd[node]:

                schedule_data[node].append(road)
                schedule_data[node].append(numberOfcars)
                if(numberOfcars > 1):
                    numberOfcars -= 1


def makeOutputFile():
    outfilename = filename[0]+"OUTPUT2.out"
    f = open(outfilename, "w")
    f.write(str(intersection_needed)+"\n")

    for i in list(schedule_data.keys()):
        f.write(str(i)+"\n")
        f.write(str(schedule_data[i][0])+"\n")

        j = 0
        while(j < schedule_data[i][0]*2):
            line = schedule_data[i][j+1]+" "+str(schedule_data[i][j+2])
            j += 2

            if(i != list(schedule_data.keys())[-1] or j <= schedule_data[i][0]):
                line += "\n"
            f.write(line)

    print('Output file ready!: ', outfilename)


readFile()
# displayData()
print("Scheduling")
schedule()
print("Scheduling over")
makeOutputFile()
