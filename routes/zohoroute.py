# routes/job_routes.py

import datetime
from flask import Blueprint, jsonify, request
from pymongo import MongoClient
from flask import current_app as app

zoho_bp = Blueprint('zoho_bp', __name__)

@zoho_bp.route("/zoho")
def index():
    return "Hello zoho member</a>"

@zoho_bp.route('/zoho/add', methods=['POST'])
def add_zoho_job():
    try:
        # Get job data from request JSON
        job_data = request.json
        
        # Validate required fields
        required_fields = ['Posting Title', 'Contact Name', 'Assigned Recruiter(s)', 'Target Date', 
                           'Job Opening Status', 'Industry', 'Salary', 'Client Name', 'Account Manager', 
                           'Date Opened', 'Job Type', 'Work Experience', 'Required Skills', 'Address Information', 
                           'City', 'Country', 'Province', 'Postal Code', 'Forecast Details', 
                           'Revenue per Position', 'Actual Revenue', 'Expected Revenue', 'Missed Revenue', 'Number of Positions']
        
        missing_fields = [field for field in required_fields if field not in job_data]
        if missing_fields:
            return jsonify({'error': f'Missing fields: {", ".join(missing_fields)}'}), 400

        # Convert Target Date to datetime
        job_data['Target Date'] = datetime.strptime(job_data['Target Date'], '%m/%d/%Y')
        
        # Insert job data into MongoDB
        result = app.db.jobslist.insert_one(job_data)
        
        # Return success response with inserted ID
        return jsonify({'message': 'Job added successfully', 'job_id': str(result.inserted_id)}), 201
    
    except Exception as e:
        # Return error response
        return jsonify({'error': str(e)}), 500