import random

bag = []
# makes a simple 7-bag randomizer, makes tetris always solvable
def randomgenerator():
    global bag

    if len(bag) == 0:
        bag = [0, 1, 2, 3, 4, 5, 6]
        random.shuffle(bag)
    print(bag)
    return bag.pop()

