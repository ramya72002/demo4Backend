# routes/job_routes.py
import secrets
from pymongo.errors import DuplicateKeyError
import datetime
# import io
from flask import Blueprint, jsonify, request
from pymongo import MongoClient
from flask import current_app as app
from datetime import datetime
# from pyresparser import ResumeParser
# from docx import Document
import uuid
# import tempfile
# from PyPDF2 import PdfReader

zoho_bp = Blueprint('zoho_bp', __name__)
JOB_STAGE_MAPPING = {
    '1': 'screening',
    '2': 'submissions',
    '3': 'interview',
    '4': 'offered',
    '5': 'hired',
    '6': 'rejected',
    '7': 'archived'
}
# def sanitize_text(text):
#     # Sanitize the text to ensure it does not contain invalid characters
#     return ''.join(c if c.isprintable() else ' ' for c in text)

# @zoho_bp.route('/res', methods=['POST'])
# def upload_resume():
#     if 'file' not in request.files:
#         return jsonify({'error': 'No file part in the request'}), 400

#     file = request.files['file']

#     if file.filename == '':
#         return jsonify({'error': 'No selected file'}), 400

#     if file and file.filename.lower().endswith('.pdf'):
#         try:
#             # Step 1: Extract text from the PDF file using PyPDF2
#             def convert_pdf_to_text(file_stream):
#                 reader = PdfReader(file_stream)
#                 text = ''
#                 for page in reader.pages:
#                     text += page.extract_text() or ''
#                 return text

#             pdf_text = sanitize_text(convert_pdf_to_text(file))

#             # Step 2: Save the extracted text into a .docx file (in-memory)
#             doc = Document()
#             doc.add_paragraph(pdf_text)
            
#             # Create a temporary file
#             with tempfile.NamedTemporaryFile(delete=False, suffix='.docx') as temp_file:
#                 temp_file_name = temp_file.name
#                 doc.save(temp_file_name)

#             # Step 3: Parse the newly created .docx file using pyresparser
#             try:
#                 data = ResumeParser(temp_file_name).get_extracted_data()
#                 # skills = data.get('skills', 'No skills found')
#                 return jsonify({'data': data}), 200
#             except Exception as e:
#                 return jsonify({'error': 'Error while parsing the .docx file: ' + str(e)}), 500
#             finally:
#                 # Clean up the temporary file
#                 os.remove(temp_file_name)

#         except Exception as e:
#             return jsonify({'error': 'Error while processing the PDF file: ' + str(e)}), 500

#     return jsonify({'error': 'Invalid file format'}), 400
def generate_unique_candidate_id():
    """Generate a unique 6-digit candidate ID."""
    while True:
        # Generate a 6-digit random number
        candidate_id = str(secrets.randbelow(900000) + 100000)  # Ensures a 6-digit number
        
        # Check if the ID already exists in the database
        if not app.db2.candidatelist.find_one({'candidateId': candidate_id}):

            return candidate_id

@zoho_bp.route("/zoho")
def index():
    return "Hello zoho member</a>"

def generate_unique_jobId():
    """Generate a unique 6-digit job ID."""
    while True:
        # Generate a 6-digit random number
        jobId = str(secrets.randbelow(900000) + 100000)  # Ensures a 6-digit number
        
        # Check if the ID already exists in the database
        if not app.db2.joblist.find_one({'jobId': jobId}):
            return jobId



@zoho_bp.route('/zoho/postjob', methods=['POST'])
def add_zoho_jobt():
    try:
        # Get job data from request JSON
        job_data = request.json
        
        # Define required fields
        required_fields = ['postingTitle','clientName','targetDate','industry','numberOfPositions']
        
        # Validate required fields
        missing_fields = [field for field in required_fields if field not in job_data]
        if missing_fields:
            return jsonify({'error': f'Missing fields: {", ".join(missing_fields)}'}), 400
        
        # Generate a unique clientId
        job_data['jobId'] = generate_unique_jobId()
        
        # Insert the client data into the database
        result = app.db2.joblist.insert_one(job_data)
        
        # Return success response with inserted ID
        return jsonify({'message': 'jobs added successfully', 'job_id': job_data['jobId']}), 201
    
    except Exception as e:
        # Return error response
        return jsonify({'error': str(e)}), 500

@zoho_bp.route('/job/update/<jobId>', methods=['PUT'])
def update_jobid(jobId):
    try:
        # Get the data to update from the request JSON
        update_data = request.json

        if not update_data:
            return jsonify({'error': 'updateData must be provided'}), 400

        # Build the query filter
        query = {'jobId': jobId}
        
        # Update the candidate data in MongoDB
        result = app.db2.joblist.update_one(query, {'$set': update_data})

        if result.matched_count == 0:
            return jsonify({'message': 'job not found'}), 404
        
        # Return success response
        return jsonify({'message': 'job updated successfully'}), 200
    
    except Exception as e:
        # Return error response
        return jsonify({'error': str(e)}), 500


@zoho_bp.route('/zoho/getclient_id', methods=['GET'])
def get_zoho_client_name():
    try:
        # Get query parameters
        clientId = request.args.get('clientId')
        
        if not clientId :
            return jsonify({'error': 'name must be provided'}), 400
        
        # Build the query
        query = {}
        if clientId:
            query['clientId'] = clientId
        
        # Query the MongoDB collection
        clients = list(app.db2.clientlist.find(query))
        
        # Convert ObjectId to string for JSON serialization
        for candidate in clients:
            candidate['_id'] = str(candidate['_id'])
        
        # Return the candidates in JSON format
        return jsonify(clients), 200
    
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
        
        # Generate a unique clientId
        job_data['clientId'] = generate_unique_client_id()
        
        # Insert the client data into the database
        result = app.db2.clientlist.insert_one(job_data)
        
        # Return success response with inserted ID
        return jsonify({'message': 'Client added successfully', 'client_id': job_data['clientId']}), 201
    
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
    

@zoho_bp.route('/zoho/getjob_id', methods=['GET'])
def get_zoho_job_name():
    try:
        # Get query parameters
        jobId = request.args.get('jobId')
        
        if not jobId :
            return jsonify({'error': 'name must be provided'}), 400
        
        # Build the query
        query = {}
        if jobId:
            query['jobId'] = jobId
        
        # Query the MongoDB collection
        jobs = list(app.db2.joblist.find(query))
        
        # Convert ObjectId to string for JSON serialization
        for job in jobs:
            job['_id'] = str(job['_id'])
        
        # Return the candidates in JSON format
        return jsonify(jobs), 200
    
    except Exception as e:
        # Return error response
        return jsonify({'error': str(e)}), 500


@zoho_bp.route('/job/update/<jobId>', methods=['PUT'])
def update_jobsid(jobId):
    try:
        # Get the data to update from the request JSON
        update_data = request.json

        if not update_data:
            return jsonify({'error': 'updateData must be provided'}), 400

        # Build the query filter
        query = {'jobId': jobId}
        
        # Update the candidate data in MongoDB
        result = app.db2.joblist.update_one(query, {'$set': update_data})

        if result.matched_count == 0:
            return jsonify({'message': 'job not found'}), 404
        
        # Return success response
        return jsonify({'message': 'job updated successfully'}), 200
    
    except Exception as e:
        # Return error response
        return jsonify({'error': str(e)}), 500





@zoho_bp.route('/zoho/getcandidate_id', methods=['GET'])
def get_zoho_candidate_name():
    try:
        # Get query parameters
        candidateId = request.args.get('candidateId')
        
        if not candidateId :
            return jsonify({'error': 'name must be provided'}), 400
        
        # Build the query
        query = {}
        if candidateId:
            query['candidateId'] = candidateId
        
        # Query the MongoDB collection
        candidates = list(app.db2.candidatelist.find(query))
        
        # Convert ObjectId to string for JSON serialization
        for candidate in candidates:
            candidate['_id'] = str(candidate['_id'])
        
        # Return the candidates in JSON format
        return jsonify(candidates), 200
    
    except Exception as e:
        # Return error response
        return jsonify({'error': str(e)}), 500

@zoho_bp.route('/candidate/post', methods=['POST'])
def post_candidate():
    try:
        # Get candidate data from request JSON
        candidate_data = request.json

        # Generate a unique 6-digit candidateId
        candidate_id = generate_unique_candidate_id()

        # Add candidateId to candidate data
        candidate_data['candidateId'] = candidate_id
        
        # Set other default values
        candidate_data['candidateStage'] = "new"
        candidate_data['addJob'] = None
        candidate_data['jobStage'] = 1

        # Insert candidate data into MongoDB
        result = app.db2.candidatelist.insert_one(candidate_data)
        
        # Return success response with inserted ID and candidateId
        return jsonify({'message': 'Candidate added successfully', 'candidate_id': candidate_id, 'db_id': str(result.inserted_id)}), 201
    
    except Exception as e:
        # Return error response
        return jsonify({'error': str(e)}), 500

@zoho_bp.route('/candidate/update/<candidateId>', methods=['PUT'])
def update_candidate(candidateId):
    try:
        # Get the data to update from the request JSON
        update_data = request.json

        if not update_data:
            return jsonify({'error': 'updateData must be provided'}), 400

        # Build the query filter
        query = {'candidateId': candidateId}
        
        # Update the candidate data in MongoDB
        result = app.db2.candidatelist.update_one(query, {'$set': update_data})

        if result.matched_count == 0:
            return jsonify({'message': 'Candidate not found'}), 404
        
        # Return success response
        return jsonify({'message': 'Candidate updated successfully'}), 200
    
    except Exception as e:
        # Return error response
        return jsonify({'error': str(e)}), 500



@zoho_bp.route('/candidate/update_stage/<candidateId>', methods=['PUT'])
def update_candidate_stage(candidateId):
    try:
        # Get the candidateStage from the request JSON
        update_data = request.json.get('candidateStage')

        if not update_data:
            return jsonify({'error': 'candidateStage must be provided'}), 400

        # Build the query filter
        query = {'candidateId': candidateId}
        
        # Update the candidateStage in MongoDB
        result = app.db2.candidatelist.update_one(query, {'$set': {'candidateStage': update_data}})

        if result.matched_count == 0:
            return jsonify({'message': 'Candidate not found'}), 404
        
        # Return success response
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


@zoho_bp.route('/client/update/<clientId>', methods=['PUT'])
def update_client(clientId):
    try:
        # Get the data to update from the request JSON
        update_data = request.json

        if not update_data:
            return jsonify({'error': 'updateData must be provided'}), 400

        # Build the query filter
        query = {'clientId': clientId}
        
        # Update the client data in MongoDB
        result = app.db2.clientlist.update_one(query, {'$set': update_data})

        if result.matched_count == 0:
            return jsonify({'message': 'client not found'}), 404
        
        # Return success response
        return jsonify({'message': 'client  updated successfully'}), 200
    
    except Exception as e:
        # Return error response
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
    

@zoho_bp.route('/hiringpipeline/details', methods=['GET'])
def get_all_details():
    try:
        # Fetch all records where Add_Job is not null
        candidates = app.db2.candidatelist.find({"Add_Job": {"$ne": None}}, {'_id': False})
        
        # Convert the MongoDB cursor into a list
        candidates_list = list(candidates)
        
        # Create a dictionary where Add_Job is the key and a list of records is the value
        candidates_dict = {}
        for candidate in candidates_list:
            add_job = candidate.get('Add_Job')
            if add_job:
                if add_job in candidates_dict:
                    candidates_dict[add_job].append(candidate)
                else:
                    candidates_dict[add_job] = [candidate]
        
        # Return the dictionary as JSON
        return jsonify(candidates_dict), 200
    
    except Exception as e:
        # Return error response in case of failure
        return jsonify({'error': str(e)}), 500
    

@zoho_bp.route('/update-job-stage', methods=['PUT'])
def update_job_stage():
    try:
        # Get the JSON data from the request
        data_list = request.json

        if not isinstance(data_list, list):
            return jsonify({'error': 'Request data must be a list'}), 400

        # Process each item in the list
        update_results = []
        for data in data_list:
            # Extract the details from the JSON request
            first_name = data.get('First Name')
            last_name = data.get('Last Name')
            email = data.get('Email')
            new_job_stage = data.get('job_stage')

            # Check for required fields
            if not all([first_name, last_name, email, new_job_stage]):
                update_results.append({
                    'status': 'error',
                    'details': 'Missing required fields',
                    'record': data
                })
                continue

            # Ensure job_stage is an integer
            if not isinstance(new_job_stage, int):
                update_results.append({
                    'status': 'error',
                    'details': 'job_stage must be an integer',
                    'record': data
                })
                continue

            # Convert job_stage to string for dictionary key lookup
            job_stage_key = str(new_job_stage)
            if job_stage_key not in JOB_STAGE_MAPPING:
                update_results.append({
                    'status': 'error',
                    'details': 'Invalid job_stage value',
                    'record': data
                })
                continue

            # Find and update the record
            result = app.db2.candidatelist.update_one(
                {
                    'First Name': first_name,
                    'Last Name': last_name,
                    'Email': email
                },
                {
                    '$set': {'job_stage': new_job_stage}
                }
            )
            
            # Check if any document was modified
            if result.modified_count == 0:
                update_results.append({
                    'status': 'error',
                    'details': 'No record found or job_stage already up-to-date',
                    'record': data
                })
            else:
                update_results.append({
                    'status': 'success',
                    'record': data
                })

        return jsonify({'results': update_results}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500