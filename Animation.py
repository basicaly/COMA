import ZombieChristmas as xrm


def zombieChristmas(n, m, pos):
    intermediate = []
    while xrm.christmasFate:
        xrm.updatePositions(n, m, pos)
        square = xrm.extractSquare(pos)
        xrm.giftExchange(square)
        xrm.mergeSquare(square, intermediate)
        if not pos:
            pos = intermediate
            intermediate = []
    print(xrm.christmasFate(pos))


n = 20
m = 30
population = 10
pos = xrm.randomPositions(n, m, population)
zombieChristmas(n, m, pos)
