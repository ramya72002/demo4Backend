# app.py

from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient
from dotenv import load_dotenv
import os, pathlib
from routes.auth_routes import auth_bp
from routes.job_routes import job_bp
from routes.zohoroute import zoho_bp


app = Flask("Google login app")
app.secret_key="CodeSecret"
CORS(app)
load_dotenv()

# Get the MongoDB URI from the environment variable
mongo_uri = os.getenv('MONGO_URI')
# MongoDB setup
client = MongoClient(mongo_uri)
app.db = client.jobwebsite
app.db1 = client.company_db
app.db2 = client.zoho_db

GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "client_secret.json")


# Register Blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(job_bp)
app.register_blueprint(zoho_bp)

@app.route("/")
def index():
    return "Hello World <a href='/login'> <button>Login</button></a>"

    
if __name__ == '__main__':
    app.run()
