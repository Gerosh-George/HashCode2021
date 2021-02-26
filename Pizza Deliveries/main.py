# data
availablePizzas = 0
pizza_copy_list = []
pizza_list = []
team = {}

# computable
deliveries = 0
delivery_data = {
    2: [],
    3: [],
    4: []
}

total = 0
history_index = {}

filename = "e_many_teams"
# a_example
# b_little_bit_of_everything
# c_many_ingredients
# d_many_pizzas
# e_many_teams


def status():

    print("%d/%d-----%d\t(%d, %d, %d)" %
          (deliveries, total, availablePizzas, team[2], team[3], team[4]))


def readFile():
    global availablePizzas, pizza_copy_list, total
    f = open(filename+".in", "r")
    availablePizzas, team2, team3, team4 = list(map(int, f.readline().split()))

    team[2] = team2
    team[3] = team3
    team[4] = team4
    total = team2+team3+team4
    for index, x in enumerate(f):
        tp = list(x.split())
        pizza_list.append([])
        for i in range(int(tp[0])):
            pizza_list[index].append(tp[i + 1])
    pizza_copy_list = list(pizza_list)
    pizza_list.sort(reverse=True, key=len)  # sorting acc to len
    f.close()


def makeOutputFile():

    outputFilename = filename + "_Output"

    f = open(outputFilename+".in", "w")
    f.write(str(deliveries) + "\n")

    delivered_team_type = list(delivery_data.keys())

    for key in delivered_team_type:
        for pizza_set in delivery_data[key]:
            line = str(key) + " "
            line += " ".join(list(map(str, pizza_set)))
            if key != delivered_team_type[-1] or pizza_set != delivery_data[key][-1]:
                line += "\n"
            f.write(line)

    f.close()
    print("File created successfully: ", outputFilename)


def displayData():
    print("\nAvailable Pizzas: %d" % availablePizzas)
    print("Team2 to be fed: %d" % team[2])
    print("Team3 to be fed: %d" % team[3])
    print("Team4 to be fed: %d" % team[4])
    # for l in pizza_list:
    #print(len(l), end=' ')
    # print(l)
    print("\n")


def remove(forDelivery):
    for pizza in forDelivery:
        if pizza in pizza_list:
            pizza_list.remove(pizza)


def findfor2():
    umax = 0
    forDelivery = [pizza_list[0]]

    for pizza in pizza_list[1:]:
        # finding number of unique ingredients
        usize = len(set(forDelivery[0]+pizza))
        if(usize >= umax):
            umax = usize
            if len(forDelivery) == 2:
                forDelivery.pop()
            if pizza not in forDelivery or pizza_list.count(pizza) == len(pizza_list):
                forDelivery.append(pizza)

    return umax, forDelivery


def findfor3(forDelivery):
    umax = 0
    for pizza in pizza_list:
        usize = len(set(forDelivery[0]+forDelivery[1]+pizza))
        if(usize >= umax):
            umax = usize
            if len(forDelivery) == 3:
                forDelivery.pop()
            if pizza not in forDelivery or pizza_list.count(pizza) == len(pizza_list):
                forDelivery.append(pizza)

    return umax, forDelivery


def findfor4(forDelivery):
    umax = 0
    for pizza in pizza_list:
        usize = len(set(forDelivery[0]+forDelivery[1]+forDelivery[2]+pizza))
        if(usize >= umax):
            umax = usize
            if len(forDelivery) == 4:
                forDelivery.pop()
            if pizza not in forDelivery or pizza_list.count(pizza) == len(pizza_list):
                forDelivery.append(pizza)

    return umax, forDelivery


def findPreferredTeam():
    global availablePizzas

    forDelivery = []
    max_unique_size = {
        2: 0,
        3: 0,
        4: 0
    }

    if len(pizza_list) > 1 and team[2] != 0:
        max_unique_size[2], forDelivery = findfor2()

    if len(pizza_list) > 2 and len(forDelivery) == 2 and team[3] != 0:
        max_unique_size[3], forDelivery = findfor3(forDelivery)

    if len(pizza_list) > 3 and len(forDelivery) == 3 and team[4] != 0:
        max_unique_size[4], forDelivery = findfor4(forDelivery)

    #print('Team2 umax: %d'%max_unique_size[2])
    #print('Team3 umax: %d'%max_unique_size[3])
    #print('Team4 umax: %d'%max_unique_size[4])

    teamType = len(forDelivery)

    while(teamType > 1 and team[teamType] == 0):
        teamType -= 1
        if(teamType == 1):
            break
        forDelivery.pop()

    #print("Preferred Team Type: %d"%teamType)
    #print("Max unique ingredients: %d"%max_unique_size[teamType])

    if(teamType > 1):
        remove(forDelivery)
    return teamType, forDelivery


def placeOrders():
    global availablePizzas, deliveries

    while(availablePizzas > 0 and deliveries < total):

        teamType, forDelivery = findPreferredTeam()

        # team2 got over
        if(teamType <= 1 or availablePizzas == 1):
            break

        if(team[teamType] != 0):
            team[teamType] -= 1
            availablePizzas -= teamType
            deliveries += 1

            pizza_group = []
            for pizza in forDelivery:
                index = 0

                if(str(pizza) in list(history_index.keys())):
                    index = history_index[str(pizza)] + 1

                index = pizza_copy_list.index(pizza, index)
                pizza_group.append(index)
                history_index[str(pizza)] = index
            delivery_data[teamType].append(pizza_group)

            #delivery_data[teamType].append([pizza_copy_list.index(pizza) for pizza in forDelivery])
        status()

        #print("\nStats: %d %d %d\n"%(len(pizza_list),availablePizzas,deliveries))


readFile()
displayData()
placeOrders()
# displayData()
makeOutputFile()


""""
pizzas: 10

2: 0,1 ==>6
3: 0,1,3 ===>7
4: 0,1,3,4   ==> 5

maximise ingredients
if total pizzas greater than no of people go for higher member teams with higher coefficient

"""
