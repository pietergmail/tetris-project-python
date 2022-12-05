
class Score:
    def __init__(self, name, score):
        self.name = name
        self.score = score


# returns 10 highest scores in order (currently hardcoded)
def gethighscores():
    scores = [Score("test1", 15),
              Score("Test2", 14),
              Score("Test3", 13),
              Score("Test4", 12),
              Score("Test5", 11),
              Score("Test6", 10),
              Score("Test7", 9),
              Score("Test8", 8),
              Score("Test9", 7),
              Score("Test10", 6),
              ]
    return scores


# adds high score to firebase (currently unimplemented)
def addhighscore(name, score):
    print("name: " + name + " has a score of " + str(score) + " points.")