import firebase_database


class Score:
    def __init__(self, name, score):
        self.name = name
        self.score = score


# gets the values from the database and makes them easier to work with for the pygame frontend
def gethighscores():
    # get the firebse values in dict form
    scores_raw = firebase_database.gettingscores()

    # setup list with scores
    scores = []
    for key in scores_raw:
        scores.append(Score(scores_raw[key]["name"], scores_raw[key]["amount"]))

    return scores


# adds high score to firebase (currently unimplemented)
def addhighscore(name, score):
    firebase_database.addscore(name, score)