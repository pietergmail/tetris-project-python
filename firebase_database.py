import firebase_admin
from firebase_admin import credentials, db
import uuid


def functionSetId(Id=None):
    try:
        Id += 1
    except AttributeError:
        userId = 1


# setting up credentials with json file
cred = credentials.Certificate("tetris-project-python-firebase-adminsdk-y0naf-04146607aa.json")
# initialising app making use of credentials and connecting with database
app = firebase_admin.initialize_app(cred, {
    "databaseURL": "https://tetris-project-python-default-rtdb.europe-west1.firebasedatabase.app"})
# getting reference of database using root collection
reference_database_root = db.reference("/scores")
# --------------------------------------------------
# code block for pushing data
name, amount = input("Name, amount -> ").split()
# conversion of datatypes to be secure / for safety
name = str(name)
amount = int(amount)
# adding values to the object used for input
values = {
    "Name": name, "Amount": amount
}
reference_database_root.child(name.lower()).push(values)
