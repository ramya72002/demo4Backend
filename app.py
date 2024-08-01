from flask import Flask, jsonify, request,session, abort, redirect, request
from flask_cors import CORS
from datetime import datetime
from pymongo import MongoClient
from dotenv import load_dotenv
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol
import google.auth.transport.requests
import os,requests
import pathlib

MAX_RETRIES = 3
RETRY_DELAY_SECONDS = 1

app = Flask("Google login app")
app.secret_key="CodeSecret"
CORS(app)
load_dotenv()

# Get the MongoDB URI from the environment variable
mongo_uri = os.getenv('MONGO_URI')
# MongoDB setup
client = MongoClient(mongo_uri)
db = client.jobwebsite
users_collection = db.jobslist

GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "client_secret.json")

flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],
    redirect_uri="https://demo4-rose.vercel.app"
)

@app.route("/")
def index():
    return "Hello World <a href='/login'><button>Login</button></a>"

def time_now():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')



def login_is_required(function):
    def wrapper(*args, **kwargs):
        if "google_id" not in session:
            return abort(401)  # Authorization required
        else:
            return function()

    return wrapper


@app.route("/login")
def login():
    authorization_url, state = flow.authorization_url()
    session["state"] = state
    return redirect(authorization_url)


@app.route("/callback")
def callback():
    flow.fetch_token(authorization_response=request.url)

    if not session["state"] == request.args["state"]:
        abort(500)  # State does not match!

    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)

    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=GOOGLE_CLIENT_ID
    )

    session["google_id"] = id_info.get("sub")
    session["name"] = id_info.get("name")
    return redirect("/protected_area")



@app.route("/protected_area")
@login_is_required
def protected_area():
    return f"Hello {session['name']}! <br/> <a href='/logout'><button>Logout</button></a>"

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")




@app.route('/joblist', methods=['GET'])
def get_joblist():
    try:
        # Fetch all records from the collection
        users = users_collection.find({}, {'_id': 0})  # Exclude the _id field
        # Convert MongoDB documents to a list of dictionaries
        users_list = list(users)
        return jsonify(users_list)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/joblist', methods=['POST'])
def add_joblist():
    try:
        # Get job data from request JSON
        job_data = request.json
        
        # Validate required fields
        required_fields = ['Job Title', 'Company Name', 'yrs of exp', 'location', 'skills']
        for field in required_fields:
            if field not in job_data:
                return jsonify({'error': f'Missing field: {field}'}), 400
        
        # Insert job data into MongoDB
        result = users_collection.insert_one(job_data)
        
        # Return success response with inserted ID
        return jsonify({'message': 'Job added successfully', 'job_id': str(result.inserted_id)}), 201
    
    except Exception as e:
        # Return error response
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)