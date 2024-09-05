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
    
@zoho_bp.route('/zoho/updatejobstatus', methods=['POST'])
def update_job_status():
    try:
        # Get request data
        client_name = request.json.get('clientName')
        posting_title = request.json.get('postingTitle')
        new_status = request.json.get('newStatus')

        # Validate input
        if not client_name or not posting_title or not new_status:
            return jsonify({'error': 'clientName, postingTitle, and newStatus are required'}), 400

        # Find the job and update the status
        result = app.db2.joblist.update_one(
            {'clientName': client_name, 'postingTitle': posting_title},
            {'$set': {'Job Opening Status': new_status}}
        )

        # Check if any job was updated
        if result.matched_count == 0:
            return jsonify({'error': 'Job not found'}), 404

        return jsonify({'message': 'Job status updated successfully'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@zoho_bp.route('/zoho/getjob', methods=['GET'])
def get_zoho_job():
    try:
        # Get query parameters
        posting_title = request.args.get('postingTitle')
        client_name = request.args.get('clientName')
        
        # Ensure at least one query parameter is provided
        if not posting_title and not client_name:
            return jsonify({'error': 'At least one of Posting Title or Client Name must be provided'}), 400
        
        # Build the query
        query = {}
        if posting_title:
            query['postingTitle'] = posting_title
        if client_name:
            query['clientName'] = client_name
        
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
        
        candidate_data['Candidate_Stage'] = "new"
        # Insert candidate data into MongoDB
        result = app.db2.candidatelist.insert_one(candidate_data)
        
        # Return success response with inserted ID
        return jsonify({'message': 'Candidate added successfully', 'candidate_id': str(result.inserted_id)}), 201
    
    except Exception as e:
        # Return error response
        return jsonify({'error': str(e)}), 500

@zoho_bp.route('/candidate/update_stage', methods=['POST'])
def update_candidate_stage():
    try:
        # Get data from request JSON
        update_data = request.json
        
        # Check if 'candidate_id' and 'Candidate_Stage' are provided
        if 'candidate_id' not in update_data or 'Candidate_Stage' not in update_data:
            return jsonify({'error': 'Missing required fields: candidate_id and Candidate_Stage'}), 400
        
        # Define the candidate ID and new stage
        candidate_id = update_data['candidate_id']
        new_stage = update_data['Candidate_Stage']
        
        # Update the candidate's stage in MongoDB
        result = app.db2.candidatelist.update_one(
            {'_id': pymongo.ObjectId(candidate_id)},  # Filter by candidate ID
            {'$set': {'Candidate_Stage': new_stage}}  # Update the Candidate_Stage
        )
        
        # Check if the update was successful
        if result.matched_count == 0:
            return jsonify({'error': 'Candidate not found'}), 404
        
        return jsonify({'message': 'Candidate stage updated successfully'}), 200
    
    except Exception as e:
        # Return error response
        return jsonify({'error': str(e)}), 500

@zoho_bp.route('/zoho/postinterview', methods=['POST'])
def add_interview():
    try:
        # Get interview data from request JSON
        interview_data = request.json

        # Define required fields
        required_fields = ['candidateName', 'interviewName', 'postingTitle', 'from', 'to', 'interviewers']
        
        # Validate required fields
        missing_fields = [field for field in required_fields if field not in interview_data]
        if missing_fields:
            return jsonify({'error': f'Missing fields: {", ".join(missing_fields)}'}), 400
        
        # Change the format to match the incoming date format
        interview_data['from'] = datetime.strptime(interview_data['from'], '%m/%d/%Y %I:%M %p')
        interview_data['to'] = datetime.strptime(interview_data['to'], '%m/%d/%Y %I:%M %p')


        # Insert interview data into MongoDB
        result = app.db2.interviewlist.insert_one(interview_data)

        # Return success response with inserted ID
        return jsonify({'message': 'Interview added successfully', 'interview_id': str(result.inserted_id)}), 201
    
    except Exception as e:
        # Return error response
        return jsonify({'error': str(e)}), 500
    
@zoho_bp.route('/zoho/getinterviews', methods=['GET'])
def get_all_interviews():
    try:
        # Fetch all records from the interviewlist collection
        interviews = list(app.db2.interviewlist.find())

        # Convert the MongoDB ObjectId to string for each document
        for interview in interviews:
            interview['_id'] = str(interview['_id'])

        # Return the list of interviews as a JSON response
        return jsonify({'interviews': interviews}), 200

    except Exception as e:
        # Return error response in case of any issues
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

@zoho_bp.route('/clients/getall', methods=['GET'])
def get_all_clients():
    try:
        # Fetch all records from the 'clients' collection and exclude '_id'
        clients = app.db2.clientlist.find({}, {'_id': False})
        
        # Convert the MongoDB cursor into a list
        clients_list = list(clients)
        
        # Return the list of clients as JSON
        return jsonify(clients_list), 200
    
    except Exception as e:
        # Return error response in case of failure
        return jsonify({'error': str(e)}), 500