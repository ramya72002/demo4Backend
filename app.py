# app.py

from flask import Flask
from flask_cors import CORS
from pymongo import MongoClient
from dotenv import load_dotenv
import os, pathlib
from routes.auth_routes import auth_bp
from routes.job_routes import job_bp

app = Flask("Google login app")
app.secret_key="CodeSecret"
CORS(app)
load_dotenv()

# Get the MongoDB URI from the environment variable
mongo_uri = os.getenv('MONGO_URI')
# MongoDB setup
client = MongoClient(mongo_uri)
app.db = client.jobwebsite

GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "client_secret.json")


# Register Blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(job_bp)

@app.route("/")
def index():
    return "Hello World <a href='/login'> <button>Login</button></a>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
