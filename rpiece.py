import random


# makes a simple 7-bag randomizer, makes tetris always solvable
def randomgenerator():
    bag = []

    while True:
        if len(bag) == 0:
            bag = [0, 1, 2, 3, 4, 5, 6]
            random.shuffle(bag)

        return bag.pop()

