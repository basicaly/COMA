import random
import matplotlib.pyplot as plt
from celluloid import Camera
#the list positions contains the characters and on which square they are: positions = [["HH", 17], ["Z", 2] ...]
#each position identifies a unique square on a column of given rows and columns, as you see in the function updatePosition. 
#so the grid has the appearance as follows:
# if it has 3 columns and 2 rows: 0 1 2
#                                 3 4 5
#identifying each square with a number.

def splitup(positions):
    Z = []
    ZH = []
    H = []
    HH = []
    for i in positions:
        if i[0] == "Z":
            Z.append(i)
        if i[0] == "ZH":
            ZH.append(i)
        if i[0] == "H":
            H.append(i)
        if i[0] == "HH":
            HH.append(i)
    return Z, ZH, H, HH


def getcoordinates(positions, rows, columns):
    Z, ZH, H, HH = splitup(positions)
    coordinate = [[] for i in range(4)]
    rows, columns = rows - 1, columns - 1
    for z in Z:
        coordinate[0].append(((z[1] % columns), (z[1] // columns)))
    for zh in ZH:
        coordinate[1].append(((zh[1] % columns), (zh[1] // columns)))
    for h in H:
        coordinate[2].append(((h[1] % columns), (h[1] // columns)))
    for hh in HH:
        coordinate[3].append(((hh[1] % columns), (hh[1] // columns)))
    return coordinate

def splitter(precoordinates):
    Zc, ZHc, Hc, HHc = [[], []], [[], []], [[], []], [[], []]
    for i in range(len(precoordinates)):
        for l in precoordinates[i]:
            if i == 0:
                Zc[0].append(l[0])
                Zc[1].append(l[1])
            elif i == 1:
                ZHc[0].append(l[0])
                ZHc[1].append(l[1])
            elif i == 2:
                Hc[0].append(l[0])
                Hc[1].append(l[1])
            elif i == 3:
                HHc[0].append(l[0])
                HHc[1].append(l[1])
    return Zc, ZHc, Hc, HHc


#the function updatePosition updates for every entry in the list positions, the square number, randomly, one step either up or down, left or right.  
#At the edges there is a snake thing going on where they reappear on the other end.
def updatePosition(rows, columns, position, rnd):
    position = position + 1
    if 0 <= rnd < 0.25:  # Right
        if (position % columns) == 0:
            return position - columns
        else:
            return position
    if 0.25 <= rnd < 0.5:  # Left
        if (position % columns) == 1:
            return position + columns - 2
        else:
            return position - 2
    if 0.5 <= rnd < 0.75:  # Down
        if (columns * (rows - 1) + 1) <= position <= rows * columns:
            return position - 1 - (columns * (rows - 1))
        else:
            return position - 1 + columns
    if 0.75 <= rnd < 1:  # Up
        if 1 <= position <= columns:
            return position - 1 + (columns * (rows - 1))
        else:
            return position - 1 - columns


def updatePositions(rows, columns, positions): #updates the position for every character in the list of positions
    for index in range(len(positions)):
        positions[index][1] = updatePosition(rows, columns, positions[index][1], random.random())


def sortPositions(positions): #sorts the positions list in ascending order depending on the square number in the list positions
    scambio = True
    while scambio:
        scambio = False
        for index in range(len(positions) - 1):
            if positions[index][1] > positions[index + 1][1]:
                positions[index], positions[index + 1] = positions[index + 1], positions[index]
                scambio = True


def extractSquare(positions): #it returns all the characters form the list position that are on the same square. 
    square = [positions.pop()]
    if not positions:
        return square
    while square[0][1] == positions[-1][1]:
        square.append(positions.pop())
        if not positions:
            break
    return square


def mergeSquare(square, intermediate): # this functions appends the extracted squares from the previous function to an intermediary list, so as no to lose the positions
    for index in square:
        intermediate.append(index)

# this function defines the rules of the game. once one square is extracted through the function at line 49, it gets passed to ths function
#and the characters get modified depending on some rules.
def giftExchange(square): 
    Z, H, ZH, HH = bestand(square)
    if ZH >= 1 and H >= 1:
        for index in range(len(square)):
            if square[index][0] == 'H':
                square[index][0] = 'HH'
    if Z >= 1 and (H >= 1 or HH >= 1):
        for index in range(len(square)):
            if Z >= HH * 2 and (square[index][0] == 'H' or square[index][0] == 'HH'):
                square[index][0] = 'Z'
            elif Z < HH * 2 and square[index][0] == 'Z':
                square[index][0] = 'ZH'

#this function is used to run the loop of the simulation which is contained in the function at line 118. it returns False basically all the time until some conditions are met
# at which point the Simulation stops and the list positionss gets passed to christmas fate, where the game ends either good or bad for the humans
def christmasFated(positions):
    Z, H, ZH, HH = bestand(positions)
    if H == 0 and HH == 0:
        return True
    if Z == 0:
        return True
    else:
        return False

# this function determines if the the zombies Took over christmas or if they got defeated 
def christmasFate(positions):
    if christmasFated(positions):
        Z, H, ZH, HH = bestand(positions)
        if H == 0 and HH == 0:
            return 'Zombies ate my Christmas!'
        if Z == 0:
            return 'Ho, ho, ho, and a merry Zombie-Christmas!'

#this function just counts how many of each character is on the whole grid. Important for function at line 81
def bestand(positions):
    Z = 0
    H = 0
    ZH = 0
    HH = 0
    for index in positions:
        if index[0] == 'Z':
            Z = Z + 1
        if index[0] == 'H':
            H = H + 1
        if index[0] == 'ZH':
            ZH = ZH + 1
        if index[0] == 'HH':
            HH = HH + 1
    return Z, H, ZH, HH

# this is a function to test the code. i can set the world grid. number of rows and columns, and how many characters i want on my grid, then return a list positions
# which is the one used throughout the whole simulation
def randomPositions(rows, columns, population):
    positions = []
    index = 0
    for i in range(population):
        positions.append([random.random(), int(random.uniform(0, rows * columns))])
    for index in range(len(positions)):
        if 0 <= positions[index][0] <= 0.25:
            positions[index][0] = 'H'
        elif 0.25 < positions[index][0] <= 0.5:
            positions[index][0] = 'ZH'
        elif 0.5 < positions[index][0] <= 0.51:
            positions[index][0] = 'HH'
        elif 0.51 < positions[index][0] < 1:
            positions[index][0] = 'Z'
    return positions

# this is the heart of the simulation, the game loop. while the function at line 81 is returning False, the game is running. once the christmas fate is True it exits the loop
# and prints out the christmas fate. now it has also the animation funciton which creates a gif with the animation.
def zombieChristmas(rows, columns, positions):
    intermediate = []
    fig = plt.figure()
    camera = Camera(fig)
    counter = 0
    while not christmasFated(positions):
        counter += 1
        precoordinates = getcoordinates(positions, rows, columns)
        Zc, ZHc, Hc, HHc = splitter(precoordinates)
        plt.scatter(Zc[0], Zc[1], c = 'r')
        plt.scatter(ZHc[0], ZHc[1], c = 'b')
        plt.scatter(Hc[0], Hc[1], c = 'g')
        plt.scatter(HHc[0], HHc[1], c = '#1f77b4')
        camera.snap()
        updatePositions(rows, columns, positions)
        sortPositions(positions)
        if counter > 1000:
            break
        while positions:
            square = extractSquare(positions)
            giftExchange(square)
            mergeSquare(square, intermediate)
            if not positions:
                positions = intermediate
                intermediate = []
                break
    print('making animation', counter, 'frames')
    animation = camera.animate()
    animation.save('animation.gif', writer = 'pillow')
    return christmasFate(positions)


#number of rows and columns on the world grid
rows, columns = 5, 5
#how many characters there are on the grid
population = 10
#creating a random list of characters wiht associated positions
positions = randomPositions(rows, columns, population)
#running the game loop
zombieChristmas(rows, columns, positions)

