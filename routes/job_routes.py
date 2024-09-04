# routes/job_routes.py

from flask import Blueprint, jsonify, request
from pymongo import MongoClient
from flask import current_app as app

job_bp = Blueprint('job_bp', __name__)

@job_bp.route('/joblist', methods=['GET'])
def get_joblist():
    try:
        # Fetch all records from the collection
        users = app.db.jobslist.find({}, {'_id': 0})  # Exclude the _id field
        # Convert MongoDB documents to a list of dictionaries
        users_list = list(users)
        return jsonify(users_list)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@job_bp.route('/joblist', methods=['POST'])
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
        result = app.db.jobslist.insert_one(job_data)
        
        # Return success response with inserted ID
        return jsonify({'message': 'Job added successfully', 'job_id': str(result.inserted_id)}), 201
    
    except Exception as e:
        # Return error response
        return jsonify({'error': str(e)}), 500
