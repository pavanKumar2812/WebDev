from flask import Blueprint

from .tracking import tracking_bp
from .create_ses_template import ses_template_bp
from .diagnostics import diagnostics_bp
from .email_sender_route import email_bp
from .campaigns_present import campaigns_bp
from .aws_templates import aws_templates_bp

def register_routes(app):
    app.register_blueprint(tracking_bp)
    app.register_blueprint(ses_template_bp)
    app.register_blueprint(diagnostics_bp)
    app.register_blueprint(email_bp)
    app.register_blueprint(campaigns_bp)
    app.register_blueprint(aws_templates_bp)