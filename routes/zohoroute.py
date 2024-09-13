# routes/job_routes.py

import secrets
from collections import Counter
from flask import Blueprint, jsonify, request
from flask import current_app as app
from datetime import datetime

zoho_bp = Blueprint('zoho_bp', __name__)

# Constants


# Helper Functions
def generate_unique_candidate_id():
    """Generate a unique 6-digit candidate ID."""
    while True:
        candidate_id = str(secrets.randbelow(900000) + 100000)  # Ensures a 6-digit number
        if not app.db2.candidatelist.find_one({'candidateId': candidate_id}):
            return candidate_id

def generate_unique_jobId():
    """Generate a unique 6-digit job ID."""
    while True:
        jobId = str(secrets.randbelow(900000) + 100000)  # Ensures a 6-digit number
        if not app.db2.joblist.find_one({'jobId': jobId}):
            return jobId

def generate_unique_client_id():
    """Generate a unique 6-digit client ID."""
    while True:
        clientId = str(secrets.randbelow(900000) + 100000)  # Ensures a 6-digit number
        if not app.db2.clientlist.find_one({'clientId': clientId}):
            return clientId

# Routes
@zoho_bp.route("/zoho")
def index():
    return "Hello zoho member</a>"

@zoho_bp.route('/zoho/postjob', methods=['POST'])
def add_zoho_job():
    try:
        job_data = request.json
        required_fields = ['jobOpening', 'clientName', 'targetDate', 'industry', 'numberOfPositions']
        missing_fields = [field for field in required_fields if field not in job_data]
        
        if missing_fields:
            return jsonify({'error': f'Missing fields: {", ".join(missing_fields)}'}), 400
        
        job_data['jobId'] = generate_unique_jobId()
        app.db2.joblist.insert_one(job_data)
        
        return jsonify({'message': 'Job added successfully', 'job_id': job_data['jobId']}), 201
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@zoho_bp.route('/job/update/<jobId>', methods=['PUT'])
def update_job(jobId):
    try:
        update_data = request.json
        if not update_data:
            return jsonify({'error': 'Update data must be provided'}), 400
        
        result = app.db2.joblist.update_one({'jobId': jobId}, {'$set': update_data})
        
        if result.matched_count == 0:
            return jsonify({'message': 'Job not found'}), 404
        
        return jsonify({'message': 'Job updated successfully'}), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500



@zoho_bp.route('/job/update_job_opening_status/<jobId>', methods=['PUT'])
def update_jobOpeningStatus_stage(jobId):
    try:
        jobOpeningStatus = request.json.get('jobOpeningStatus')
        if not jobOpeningStatus:
            return jsonify({'error': 'jobOpeningStatus must be provided'}), 400
        
        result = app.db2.joblist.update_one({'jobId': jobId}, {'$set': {'jobOpeningStatus': jobOpeningStatus}})
        
        if result.matched_count == 0:
            return jsonify({'message': 'Candidate not found'}), 404
        
        return jsonify({'message': 'Candidate stage updated successfully'}), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@zoho_bp.route('/zoho/getclient_id', methods=['GET'])
def get_zoho_client_name():
    try:
        clientId = request.args.get('clientId')
        if not clientId:
            return jsonify({'error': 'Client ID must be provided'}), 400
        
        clients = list(app.db2.clientlist.find({'clientId': clientId}, {'_id': False}))
            
        return jsonify(clients), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@zoho_bp.route('/zoho/postclient', methods=['POST'])
def add_zoho_client():
    try:
        client_data = request.json
        required_fields = ['clientName']
        missing_fields = [field for field in required_fields if field not in client_data]
        
        if missing_fields:
            return jsonify({'error': f'Missing fields: {", ".join(missing_fields)}'}), 400
        
        client_data['clientId'] = generate_unique_client_id()
        app.db2.clientlist.insert_one(client_data)
        
        return jsonify({'message': 'Client added successfully', 'client_id': client_data['clientId']}), 201
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@zoho_bp.route('/zoho/updatejobstatus', methods=['POST'])
def update_job_status():
    try:
        client_name = request.json.get('clientName')
        posting_title = request.json.get('jobOpening')
        new_status = request.json.get('newStatus')
        
        if not client_name or not posting_title or not new_status:
            return jsonify({'error': 'clientName, jobOpening, and newStatus are required'}), 400
        
        result = app.db2.joblist.update_one(
            {'clientName': client_name, 'jobOpening': posting_title},
            {'$set': {'Job Opening Status': new_status}}
        )
        
        if result.matched_count == 0:
            return jsonify({'error': 'Job not found'}), 404
        
        return jsonify({'message': 'Job status updated successfully'}), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@zoho_bp.route('/zoho/getjob_id', methods=['GET'])
def get_zoho_job_name():
    try:
        jobId = request.args.get('jobId')
        if not jobId:
            return jsonify({'error': 'Job ID must be provided'}), 400
        
        jobs = list(app.db2.joblist.find({'jobId': jobId},{'_id': False}))
      
        
        return jsonify(jobs), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@zoho_bp.route('/zoho/getinterviews', methods=['GET'])
def get_all_interviews():
    try:
        interviews = list(app.db2.interviewlist.find({},{'_id': False}))

        
        return jsonify({'interviews': interviews}), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
JOB_STAGE_MAPPING = {
    '1': 'new', 
    '2': 'inreview', 
    '3': 'available', 
    '4': 'engaged', 
    '5': 'offered', 
    '6': 'hired',
    '7': 'rejected'
}

@zoho_bp.route('/zoho/getclient_jobs', methods=['GET'])
def get_client_jobs():
    try:
        # Fetch all documents from the database
        candidates = list(app.db2.candidatelist.find({}, {'_id': False, 'name': True,'candidateId':True, 'clientName': True, 'jobOpening': True, 'candidateStage': True}))

        # Dictionary to hold the result
        result = {}

        for candidate in candidates:
            client_name = candidate.get('clientName', 'Unknown Client')
            job_opening = candidate.get('jobOpening', 'Unknown Job')
            candidate_info = {
                'candidateId':candidate.get('candidateId'),
                'candidateName': candidate.get('name'),
                'candidateStage': candidate.get('candidateStage')
            }
            
            # If the client name doesn't exist in result, add it
            if client_name not in result:
                result[client_name] = {}

            # Add the job opening as a nested key under client name
            if job_opening not in result[client_name]:
                result[client_name][job_opening] = []
            
            # Append the candidate information to the respective job opening
            result[client_name][job_opening].append(candidate_info)

        return jsonify(result), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
@zoho_bp.route('/jobs/getall', methods=['GET'])
def get_all_jobs():
    try:
        jobs = app.db2.joblist.find({}, {'_id': False})
        jobs_list = list(jobs)
        
        return jsonify(jobs_list), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@zoho_bp.route('/clients/getall', methods=['GET'])
def get_all_clients():
    try:
        clients = app.db2.clientlist.find({}, {'_id': False})
        clients_list = list(clients)
        
        return jsonify(clients_list), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@zoho_bp.route('/client/update/<clientId>', methods=['PUT'])
def update_client(clientId):
    try:
        update_data = request.json
        if not update_data:
            return jsonify({'error': 'Update data must be provided'}), 400
        
        result = app.db2.clientlist.update_one({'clientId': clientId}, {'$set': update_data})
        
        if result.matched_count == 0:
            return jsonify({'message': 'Client not found'}), 404
        
        return jsonify({'message': 'Client updated successfully'}), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@zoho_bp.route('/candidate/getall', methods=['GET'])
def get_all_candidates():
    try:
        candidates = app.db2.candidatelist.find({}, {'_id': False})
        candidates_list = list(candidates)
        
        return jsonify(candidates_list), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@zoho_bp.route('/candidate/post', methods=['POST'])
def post_candidate():
    try:
        candidate_data = request.json
        candidate_id = generate_unique_candidate_id()
        candidate_data['candidateId'] = candidate_id
        candidate_data['candidateStage'] = "new"
        candidate_data['addJob'] = None
        candidate_data['jobStage'] = 1
        
        result = app.db2.candidatelist.insert_one(candidate_data)
        
        return jsonify({'message': 'Candidate added successfully', 'candidate_id': candidate_id, 'db_id': str(result.inserted_id)}), 201
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@zoho_bp.route('/candidate/update/<candidateId>', methods=['PUT'])
def update_candidate(candidateId):
    try:
        update_data = request.json
        if not update_data:
            return jsonify({'error': 'Update data must be provided'}), 400
        
        result = app.db2.candidatelist.update_one({'candidateId': candidateId}, {'$set': update_data})
        
        if result.matched_count == 0:
            return jsonify({'message': 'Candidate not found'}), 404
        
        return jsonify({'message': 'Candidate updated successfully'}), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@zoho_bp.route('/candidate/update_stage/<candidateId>', methods=['PUT'])
def update_candidate_stage(candidateId):
    try:
        candidate_stage = request.json.get('candidateStage')
        if not candidate_stage:
            return jsonify({'error': 'candidateStage must be provided'}), 400
        
        result = app.db2.candidatelist.update_one({'candidateId': candidateId}, {'$set': {'candidateStage': candidate_stage}})
        
        if result.matched_count == 0:
            return jsonify({'message': 'Candidate not found'}), 404
        
        return jsonify({'message': 'Candidate stage updated successfully'}), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@zoho_bp.route('/candidate/update_job_stage/<candidateId>', methods=['PUT'])
def update_candidate_job_stage(candidateId):
    try:
        job_stage = request.json.get('jobStage')
        if not job_stage:
            return jsonify({'error': 'jobStage must be provided'}), 400
        
        result = app.db2.candidatelist.update_one({'candidateId': candidateId}, {'$set': {'jobStage': job_stage}})
        
        if result.matched_count == 0:
            return jsonify({'message': 'Candidate not found'}), 404
        
        return jsonify({'message': 'Candidate job stage updated successfully'}), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@zoho_bp.route('/zoho/getcandidate_id', methods=['GET'])
def get_zoho_candidate_id_name():
    try:
        candidateId = request.args.get('candidateId')
        if not candidateId:
            return jsonify({'error': 'candidate ID must be provided'}), 400
        
        candidates = list(app.db2.candidatelist.find({'candidateId': candidateId}))
        for candidate in candidates:
            candidate['_id'] = str(candidate['_id'])
        
        return jsonify(candidate), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500