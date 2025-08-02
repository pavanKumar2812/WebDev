from flask import Blueprint, request, jsonify
from datetime import datetime
from utils.common import get_collection

campaigns_bp = Blueprint('campaigns', __name__, url_prefix='/api/campaigns')


@campaigns_bp.route('', methods=['POST'])
def create_campaign():
    data = request.get_json()

    name = data.get("name")
    subject = data.get("subject")
    content = data.get("content")

    if not all([name, content]):
        return jsonify({"error": "Missing campaign name, subject, or content"}), 400

    campaign_doc = {
        "name": name,
        "subject": subject,
        "content": content,
        "status": "draft",
        "created_at": datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")
    }

    try:
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
