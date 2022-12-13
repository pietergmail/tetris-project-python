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
    # getting 10 'last' values, ordening happens in ascending order!
    # return object is ordered dictionary
    # results = reference.order_by_child("amount").limit_to_last(10).get()
    # printing results dictionary mostly for test purpose of correct data retrievement
    # keeping in code for maybe later uses or in case of
    # print(results)
    # returning result object, possible ordered dictionary
    return reference.order_by_child("amount").limit_to_last(10).get()


# ------------------------------------------------------------------ code block for setting up reference and connection
# setting up credentials with json file
cred = credentials.Certificate("tetris-project-python-firebase-adminsdk-y0naf-04146607aa.json")
# initialising app making use of credentials and connecting with database
app = firebase_admin.initialize_app(cred, {
    "databaseURL": "https://tetris-project-python-default-rtdb.europe-west1.firebasedatabase.app"})
# getting reference of database using root collection
reference = db.reference()
