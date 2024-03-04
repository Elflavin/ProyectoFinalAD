import firebase_admin
from firebase_admin import credentials

def init():
    cred = credentials.Certificate("proyectofinalad-af58a-firebase-adminsdk-czuzh-49f852045b.json")
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://proyectofinalad-af58a-default-rtdb.europe-west1.firebasedatabase.app/'
    })