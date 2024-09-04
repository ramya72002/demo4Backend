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
        required_fields = ['Posting Title', 'Target Date', 'Industry', 'Client Name']
        
        # Validate required fields
        missing_fields = [field for field in required_fields if field not in job_data]
        if missing_fields:
            return jsonify({'error': f'Missing fields: {", ".join(missing_fields)}'}), 400

        # Convert Target Date to datetime
        job_data['Target Date'] = datetime.strptime(job_data['Target Date'], '%m/%d/%Y')
        
        # Insert job data into MongoDB
        result = app.db2.joblist.insert_one(job_data)
        
        # Return success response with inserted ID
        return jsonify({'message': 'Job added successfully', 'job_id': str(result.inserted_id)}), 201
    
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
