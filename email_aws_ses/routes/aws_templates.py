import os
import boto3
from flask import Blueprint, jsonify, request
from dotenv import load_dotenv

load_dotenv()

aws_templates_bp = Blueprint('aws_templates', __name__)

ses_client = boto3.client('ses', region_name=os.getenv("AWS_SES_REGION"))

@aws_templates_bp.route('/aws/templates', methods=['GET'])
def list_templates():
    """List all AWS SES email templates."""
    try:
        response = ses_client.list_templates()
        templates = response.get('TemplatesMetadata', [])
        return jsonify({"templates": templates})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@aws_templates_bp.route('/aws/templates/<template_name>', methods=['GET'])
def get_template(template_name):
    """Get a specific AWS SES email template by name."""
    try:
        response = ses_client.get_template(TemplateName=template_name)
        return jsonify(response.get('Template', {}))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@aws_templates_bp.route('/aws/templates/<template_name>', methods=['PUT'])
def update_template(template_name):
    """Update an AWS SES email template."""
    data = request.json
    try:
        response = ses_client.update_template(
            Template={
                'TemplateName': template_name,
                'SubjectPart': data.get('SubjectPart', ''),
                'TextPart': data.get('TextPart', ''),
                'HtmlPart': data.get('HtmlPart', '')
            }
        )
        return jsonify({"message": "Template updated", "response": str(response)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@aws_templates_bp.route('/aws/templates/<template_name>', methods=['DELETE'])
def delete_template(template_name):
    """Delete an AWS SES email template."""
    try:
        response = ses_client.delete_template(TemplateName=template_name)
        return jsonify({"message": "Template deleted", "response": str(response)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
