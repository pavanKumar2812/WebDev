from flask import Blueprint, request, jsonify, current_app
from datetime import datetime
from utils.common import get_collection
import os
import base64
from werkzeug.utils import secure_filename

campaigns_bp = Blueprint('campaigns', __name__, url_prefix='/api/campaigns')

ALLOWED_EXTENSIONS = {'pdf'}
UPLOAD_FOLDER = 'uploads'

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Ensure upload directory exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@campaigns_bp.route('/with-attachment', methods=['POST'])
def create_campaign_with_attachment():
    """Handle campaign creation with file upload using multipart/form-data"""
    try:
        # Get form data
        name = request.form.get("name")
        subject = request.form.get("subject")
        content = request.form.get("content")
        
        if not all([name, subject, content]):
            return jsonify({"error": "Missing campaign name, subject, or content"}), 400

        campaign_doc = {
            "name": name,
            "subject": subject,
            "content": content,
            "status": "draft",
            "created_at": datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT"),
            "attachment": None
        }

        # Handle file upload if present
        if 'pdf_file' in request.files:
            file = request.files['pdf_file']
            if file and file.filename != '' and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                # Read file content and encode as base64 for storage
                file_content = file.read()
                file_base64 = base64.b64encode(file_content).decode('utf-8')
                
                campaign_doc["attachment"] = {
                    "filename": filename,
                    "content": file_base64,
                    "content_type": "application/pdf"
                }

        # Save to database
        campaigns_col = get_collection("campaigns")
        result = campaigns_col.insert_one(campaign_doc)
        
        return jsonify({
            "message": "Campaign created successfully",
            "campaign_id": str(result.inserted_id),
            "has_attachment": campaign_doc["attachment"] is not None
        }), 201
        
    except Exception as e:
        return jsonify({"error": f"Failed to create campaign: {str(e)}"}), 500
    
@campaigns_bp.route('', methods=['POST'])
def create_campaign():
    """Handle campaign creation with JSON data (no file upload)"""
    try:
        data = request.get_json(silent=True)
        if data is None:
            # Use current_app.logger instead of app.logger
            current_app.logger.error(f"Failed to parse JSON. Content-Type: {request.headers.get('Content-Type')}. Raw data: {request.data.decode('utf-8')}")
            return jsonify({"error": "No valid JSON data provided or Content-Type header is incorrect. Please ensure Content-Type is application/json."}), 400

        # ... rest of your code
        name = data.get("name")
        subject = data.get("subject")
        content = data.get("content")

        if not all([name, subject, content]):
            return jsonify({"error": "Missing campaign name, subject, or content"}), 400

        campaign_doc = {
            "name": name,
            "subject": subject,
            "content": content,
            "status": "draft",
            "created_at": datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT"),
            "attachment": None
        }

        campaigns_col = get_collection("campaigns")
        result = campaigns_col.insert_one(campaign_doc)
        return jsonify({
            "message": "Campaign created successfully",
            "campaign_id": str(result.inserted_id)
        }), 201
    except Exception as e:
        return jsonify({"error": f"Failed to create campaign: {str(e)}"}), 500


@campaigns_bp.route('', methods=['GET'])
def get_campaigns():
    try:
        campaigns_col = get_collection("campaigns")
        campaigns = list(campaigns_col.find())

        # If empty, insert a default campaign
        if not campaigns:
            default_campaign = {
                "name": "Welcome Campaign",
                "subject": "Welcome to our service!",
                "content": "<h1>Welcome</h1><p>We're glad you're here!</p>",
                "status": "draft",
                "created_at": datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")
            }
            result = campaigns_col.insert_one(default_campaign)
            default_campaign["_id"] = str(result.inserted_id)
            return jsonify([default_campaign])

        for c in campaigns:
            c["_id"] = str(c["_id"])  # Convert ObjectId to string
        return jsonify(campaigns)

    except Exception as e:
        return jsonify({"error": f"Failed to fetch campaigns: {str(e)}"}), 500
