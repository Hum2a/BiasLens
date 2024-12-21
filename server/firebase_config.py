import firebase_admin
from firebase_admin import credentials

# Path to your Firebase Admin SDK JSON key
cred = credentials.Certificate("path/to/your-firebase-key.json")
firebase_admin.initialize_app(cred)
