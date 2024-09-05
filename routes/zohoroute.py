# routes/job_routes.py

import datetime
from flask import Blueprint, jsonify, request
from pymongo import MongoClient
from flask import current_app as app
from datetime import datetime


zoho_bp = Blueprint('zoho_bp', __name__)

@zoho_bp.route("/zoho")
def index():
    return "Hello zoho member</a>"

@zoho_bp.route('/zoho/postjob', methods=['POST'])
def add_zoho_job():
    try:
        # Get job data from request JSON
        job_data = request.json
        
        # Define required fields
        required_fields = ['postingTitle', 'clientName', 'targetDate', 'industry']
        
        # Validate required fields
        missing_fields = [field for field in required_fields if field not in job_data]
        if missing_fields:
            return jsonify({'error': f'Missing fields: {", ".join(missing_fields)}'}), 400

        # Convert Target Date to datetime
        job_data['targetDate'] = datetime.strptime(job_data['targetDate'], '%Y-%m-%d')        
        # Insert job data into MongoDB
        result = app.db2.joblist.insert_one(job_data)
        
        # Return success response with inserted ID
        return jsonify({'message': 'Job added successfully', 'job_id': str(result.inserted_id)}), 201
    
    except Exception as e:
        # Return error response
        return jsonify({'error': str(e)}), 500
    
@zoho_bp.route('/zoho/postclient', methods=['POST'])
def add_zoho_client():
    try:
        # Get job data from request JSON
        job_data = request.json
        
        # Define required fields
        required_fields = ['clientName']
        
        # Validate required fields
        missing_fields = [field for field in required_fields if field not in job_data]
        if missing_fields:
            return jsonify({'error': f'Missing fields: {", ".join(missing_fields)}'}), 400
 
        result = app.db2.clientlist.insert_one(job_data)
        
        # Return success response with inserted ID
        return jsonify({'message': 'client added successfully', 'client_id': str(result.inserted_id)}), 201
    
    except Exception as e:
        # Return error response
        return jsonify({'error': str(e)}), 500
    

@zoho_bp.route('/zoho/getjob', methods=['GET'])
def get_zoho_job():
    try:
        # Get query parameters
        posting_title = request.args.get('Posting Title')
        client_name = request.args.get('Client Name')
        
        # Ensure at least one query parameter is provided
        if not posting_title and not client_name:
            return jsonify({'error': 'At least one of Posting Title or Client Name must be provided'}), 400
        
        # Build the query
        query = {}
        if posting_title:
            query['Posting Title'] = posting_title
        if client_name:
            query['Client Name'] = client_name
        
        # Query the MongoDB collection
        jobs = list(app.db2.joblist.find(query))
        
        # Convert ObjectId to string for JSON serialization
        for job in jobs:
            job['_id'] = str(job['_id'])
        
        # Return the jobs in JSON format
        return jsonify(jobs), 200
    
    except Exception as e:
        # Return error response
        return jsonify({'error': str(e)}), 500


@zoho_bp.route('/candidate/post', methods=['POST'])
def post_candidate():
    try:
        # Get candidate data from request JSON
        candidate_data = request.json
        
        # Define required fields
        required_fields = ['Last Name']
        
        # Validate required fields
        missing_fields = [field for field in required_fields if field not in candidate_data or not candidate_data[field]]
        if missing_fields:
            return jsonify({'error': f'Missing required fields: {", ".join(missing_fields)}'}), 400
        
        # Insert candidate data into MongoDB
        result = app.db2.candidatelist.insert_one(candidate_data)
        
        # Return success response with inserted ID
        return jsonify({'message': 'Candidate added successfully', 'candidate_id': str(result.inserted_id)}), 201
    
    except Exception as e:
        # Return error response
        return jsonify({'error': str(e)}), 500

@zoho_bp.route('/jobs/getall', methods=['GET'])
def get_all_jobs():
    try:
        # Fetch all records from the 'jobs' collection and exclude '_id'
        jobs = app.db2.joblist.find({}, {'_id': False})
        
        # Convert the MongoDB cursor into a list
        candidates_list = list(jobs)
        
        # Return the list of candidates as JSON
        return jsonify(candidates_list), 200
    
    except Exception as e:
        # Return error response in case of failure
        return jsonify({'error': str(e)}), 500
    
@zoho_bp.route('/candidate/getall', methods=['GET'])
def get_all_candidates():
    try:
        # Fetch all records from the 'candidates' collection and exclude '_id'
        candidates = app.db2.candidatelist.find({}, {'_id': False})
        
        # Convert the MongoDB cursor into a list
        candidates_list = list(candidates)
        
        # Return the list of candidates as JSON
        return jsonify(candidates_list), 200
    
    except Exception as e:
        # Return error response in case of failure
        return jsonify({'error': str(e)}), 500