from flask import Blueprint, request, jsonify

ses_template_bp = Blueprint("ses_template", __name__) 
# To Create a new SES template, you can use the following route
@ses_template_bp.route("/api/create-template", methods=["POST"])
def create_template_api():
    try:
        from services.email_sender import create_ses_template
        create_ses_template()
        return jsonify({"message": "Template created (or already exists)"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500