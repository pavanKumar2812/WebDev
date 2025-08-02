from flask import Blueprint, request, jsonify
from services.email_sender import send_bulk_email  
from utils.common import get_collection, get_object_id
from bson.objectid import ObjectId
from bson.json_util import dumps
import os
from dotenv import load_dotenv
load_dotenv()

email_bp = Blueprint('email', __name__, url_prefix='/api')

@email_bp.route('/collections/<collection_name>/send/<campaign_id>/<int:batch_size>', methods=['POST'])
def send_emails(collection_name, campaign_id, batch_size):
    try:
        campaigns_collection = get_collection("campaigns")
        campaign = campaigns_collection.find_one({"_id": ObjectId(campaign_id)})
        if not campaign:
            return jsonify({"error": "Campaign not found"}), 404

        html_content = campaign.get("content", "No content available")
        # print(html_content)

        collection = get_collection(collection_name)
        if not collection:
            return jsonify({"error": "Collection not found"}), 404

        recipients = list(collection.find(
            {"isSubscribed": True},
            {"_id": 0, "email": 1, "name": 1}
        ).limit(batch_size))

        if not recipients:
            return jsonify({"error": "No recipients found"}), 400

        sender = os.getenv("SES_SENDER_EMAIL")
        template_name = os.getenv("AWS_EMAIL_TEMPLATE")

        subject = campaign.get("subject", "French with Kunal Newsletter")
        attachment = campaign.get("attachment", None)
        
        response = send_bulk_email(
            sender=sender,
            template_name=template_name,
            recipients=recipients,
            campaign_id=campaign_id,
            content=html_content,
            subject=subject,
            attachment=attachment
        )

        return jsonify({
            "status": "success",
            "message": f"Emails sent to {len(recipients)} recipients",
            "ses_response": response
        }), 200

    except Exception as e:
        # Do not reference variables like `campaign` here unless they're initialized earlier
        return jsonify({"error": str(e)}), 500
