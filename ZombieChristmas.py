import random


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


def updatePositions(rows, columns, positions):
    for index in range(len(positions)):
        positions[index][1] = updatePosition(rows, columns, positions[index][1], random.random())


def sortPositions(positions):
    scambio = True
    while scambio:
        scambio = False
        for index in range(len(positions) - 1):
            if positions[index][1] > positions[index + 1][1]:
                positions[index], positions[index + 1] = positions[index + 1], positions[index]
                scambio = True


def extractSquare(positions):
    square = [positions.pop()]
    if not positions:
        return square
    while square[0][1] == positions[-1][1]:
        square.append(positions.pop())
        if not positions:
            break
    return square


def mergeSquare(square, intermediate):
    for index in square:
        intermediate.append(index)


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


def christmasFated(positions):
    Z, H, ZH, HH = bestand(positions)
    if H == 0 and HH == 0:
        return True
    if Z == 0:
        return True
    else:
        return False


def christmasFate(positions):
    if christmasFated(positions):
        Z, H, ZH, HH = bestand(positions)
        if H == 0 and HH == 0:
            return 'Zombies ate my Christmas!'
        if Z == 0:
            return 'Ho, ho, ho, and a merry Zombie-Christmas!'


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


def randomPositions(rows, columns, population):
    limit = rows * columns
    positions = []
    index = 0
    while index < population:
        positions = 1 // random.random()
        if positions > limit:
            continue
        positions.append([random.random(), int(positions)])
        index += 1
    for index in range(len(positions)):
        if 0 <= positions[index][0] <= 0.25:
            positions[index][0] = 'H'
        elif 0.25 < positions[index][0] <= 0.5:
            positions[index][0] = 'ZH'
        elif 0.5 < positions[index][0] <= 0.6:
            positions[index][0] = 'HH'
        elif 0.6 < positions[index][0] < 1:
            positions[index][0] = 'Z'
    return positions


def zombieChristmas(rows, columns, positions):
    intermediate = []
    while not christmasFated(positions):
        updatePositions(rows, columns, positions)
        sortPositions(positions)
        while positions:
            square = extractSquare(positions)
            giftExchange(square)
            mergeSquare(square, intermediate)
            if not positions:
                positions = intermediate
                intermediate = []
                break
    return christmasFate(positions)


n = 5
m = 10
pop = 10
for i in range(100):
    pos = randomPositions(n, m, pop)
    print(zombieChristmas(n, m, pos))
