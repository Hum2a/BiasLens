import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase app
cred = credentials.Certificate("./firebase/biaslens-2782f-firebase-adminsdk-sfe59-ebb73541fd.json")
firebase_admin.initialize_app(cred)

# Get Firestore client
db = firestore.client()
