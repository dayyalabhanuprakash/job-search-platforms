"""
Job Finder Platform - Flask Backend
A job search aggregator web application
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import json
import math
from job_aggregator import JobAggregator

# Custom JSON encoder to handle NaN, inf, and other non-serializable values
class SafeJSONEncoder(json.JSONEncoder):
    def encode(self, o):
        if isinstance(o, float):
            if math.isnan(o) or math.isinf(o):
                return 'null'
        return super().encode(o)
    
    def iterencode(self, o, _one_shot=False):
        for chunk in super().iterencode(o, _one_shot):
            yield chunk.replace('NaN', 'null').replace('Infinity', 'null').replace('-Infinity', 'null')

app = Flask(__name__, static_folder='static', static_url_path='')
app.json_encoder = SafeJSONEncoder
CORS(app)

# Initialize job aggregator
job_aggregator = JobAggregator()

# ===================================
# API Routes - Job Search
# ===================================

@app.route('/api/jobs', methods=['GET'])
def get_jobs():
    """Get jobs with filters"""
    try:
        query = request.args.get('query', '')
        location = request.args.get('location', '')
        company = request.args.get('company', '')
        remote = request.args.get('remote', 'false').lower() == 'true'
        job_type = request.args.get('job_type', 'all')
        experience_level = request.args.get('experience_level', 'all')
        salary_min = int(request.args.get('salary_min', 0))
        date_posted = request.args.get('date_posted', 'all')  # This is the hours filter
        posted_after = request.args.get('posted_after', '')
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))
        use_real_jobs = request.args.get('real_jobs', 'false').lower() == 'true'
        
        result = job_aggregator.get_jobs(
            query=query,
            location=location,
            company=company,
            remote=remote,
            job_type=job_type,
            experience_level=experience_level,
            salary_min=salary_min,
            date_posted=date_posted,
            posted_after=posted_after,
            page=page,
            per_page=per_page,
            use_real_jobs=use_real_jobs
        )
        
        return jsonify(result)
    except Exception as e:
        print(f"Error fetching jobs: {e}")
        return jsonify({'error': str(e), 'jobs': [], 'total': 0}), 500

@app.route('/api/jobs/scrape', methods=['POST'])
def scrape_jobs():
    """Manually trigger job scraping from real sources"""
    try:
        data = request.get_json()
        query = data.get('query', 'software engineer')
        location = data.get('location', '')
        
        real_jobs = job_aggregator._get_real_jobs(query, location)
        
        return jsonify({
            'success': True,
            'jobs_found': len(real_jobs),
            'message': f'Successfully scraped {len(real_jobs)} jobs'
        })
    except Exception as e:
        print(f"Error scraping jobs: {e}")
        return jsonify({'error': str(e), 'success': False}), 500

@app.route('/api/jobs/<job_id>', methods=['GET'])
def get_job(job_id):
    """Get a specific job by ID"""
    try:
        job = job_aggregator.get_job_by_id(job_id)
        if job:
            return jsonify(job)
        else:
            return jsonify({'error': 'Job not found'}), 404
    except Exception as e:
        print(f"Error fetching job: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/statistics', methods=['GET'])
def get_statistics():
    """Get job statistics"""
    try:
        stats = job_aggregator.get_statistics()
        return jsonify(stats)
    except Exception as e:
        print(f"Error fetching statistics: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'Job Finder Platform',
        'version': '1.0.0'
    })

@app.route('/')
def index():
    """Serve the main application page"""
    return send_from_directory('static', 'jobs.html')

@app.route('/dashboard')
def dashboard():
    """Serve the dashboard page (alias for main page)"""
    return send_from_directory('static', 'jobs.html')

@app.route('/<path:path>')
def serve_static(path):
    """Serve static files"""
    try:
        return send_from_directory('static', path)
    except:
        return send_from_directory('static', 'jobs.html')


# Serve apply page for job details (client-side will fetch job data from API)
@app.route('/apply/<job_id>')
def apply_page(job_id):
    """Serve the apply page which loads job details via JS"""
    return send_from_directory('static', 'apply.html')

# ===================================
# Main
# ===================================

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print("=" * 50)
    print("Starting Job Finder Platform API...")
    print(f"Running on http://localhost:{port}")
    print("=" * 50)
    app.run(host='0.0.0.0', port=port, debug=True)
