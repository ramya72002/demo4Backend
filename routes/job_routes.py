from flask import Blueprint, jsonify, request
from pymongo import MongoClient
from flask import current_app as app
from datetime import datetime

job_bp = Blueprint('job_bp', __name__)

 
# Route for filtering employee records
@job_bp.route('/filter', methods=['GET'])
def filter_records():
    query = {}

    # Extracting query parameters from the request
    if 'Name' in request.args:
        query['Name'] = request.args.get('Name')
    if 'Gender' in request.args:
        query['Gender'] = request.args.get('Gender')
    if 'Dob' in request.args:
        try:
            dob = datetime.strptime(request.args.get('Dob'), '%d-%b-%y')
            query['Dob'] = dob.strftime('%d-%b-%y')
        except ValueError:
            return jsonify({'error': 'Invalid Dob format. Use DD-MMM-YY format.'}), 400
    if 'Doj' in request.args:
        try:
            doj = datetime.strptime(request.args.get('Doj'), '%d-%b-%y')
            query['Doj'] = doj.strftime('%d-%b-%y')
        except ValueError:
            return jsonify({'error': 'Invalid Doj format. Use DD-MMM-YY format.'}), 400
    if 'Pan' in request.args:
        query['Pan'] = request.args.get('Pan')
    if 'Aadhar' in request.args:
        query['Aadhar'] = request.args.get('Aadhar')
    if 'Uan' in request.args:
        query['Uan'] = int(request.args.get('Uan'))
    if 'Member ID' in request.args:
        query['Member ID'] = request.args.get('Member ID')
    if "Father's/Husband's Name" in request.args:
        query["Father's/Husband's Name"] = request.args.get("Father's/Husband's Name")
    if 'Relation' in request.args:
        query['Relation'] = request.args.get('Relation')
    if 'Marital Status' in request.args:
        query['Marital Status'] = request.args.get('Marital Status')
    if 'Mobile' in request.args:
        query['Mobile'] = int(request.args.get('Mobile'))
    if 'Email ID' in request.args:
        query['Email ID'] = request.args.get('Email ID')
    if 'Bank' in request.args:
        query['Bank'] = request.args.get('Bank')
    if 'Nomination' in request.args:
        query['Nomination'] = request.args.get('Nomination')

    try:
        # Fetching records based on the query
        results = list(app.db1.employees.find(query))
        # Convert ObjectId to string for JSON serialization
        for result in results:
            result['_id'] = str(result['_id'])

        return jsonify(results), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Route to get the list of jobs
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
