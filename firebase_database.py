import firebase_admin
from firebase_admin import credentials, db


# ----------------------------------------------------------------------------------------- code block for pushing data

def addscore(name, amount):
    # input for testing, keeping in code for maybe later uses or in case of
    # name, amount = input("name, amount: ").split()
    # conversion of datatypes to be secure / for safety
    name = str(name)
    amount = int(amount)
    # adding values to the object used for input
    values = {
        "name": name, "amount": amount
    }
    # pushing object to database, random object ID given by firebase
    reference.push(values)


# -------------------------------------------------------------------------------- code block for getting data / values
def gettingscores():
    # setup a res dictionary
    res = {}
    # put the values in a dictionary, ordening happens in ascending order
    for key, value in reference.order_by_child("amount").limit_to_last(10).get().items():
        res[key] = value
    # invert the dictionary so we have the 10 highest scores in descending order
    inv_res = dict(reversed(res.items()))
    return inv_res


# ------------------------------------------------------------------ code block for setting up reference and connection
# setting up credentials with json file
cred = credentials.Certificate("tetris-project-python-firebase-adminsdk-y0naf-04146607aa.json")
# initialising app making use of credentials and connecting with database
app = firebase_admin.initialize_app(cred, {
    "databaseURL": "https://tetris-project-python-default-rtdb.europe-west1.firebasedatabase.app"})

# getting reference of database using root collection
reference = db.reference()