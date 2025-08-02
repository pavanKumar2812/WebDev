import boto3
import json
from botocore.exceptions import ClientError
import os
from dotenv import load_dotenv
import urllib.parse
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

redirect_url = urllib.parse.quote_plus("https://frenchwithkunal.ca/unsubscribe.html")
encoded_redirect = urllib.parse.quote_plus(redirect_url)

load_dotenv()

if not os.getenv("AWS_ACCESS_KEY_ID") or not os.getenv("AWS_SECRET_ACCESS_KEY"):
    # print("❌ AWS credentials are not set in environment variables.")
    # print(os.getenv("AWS_ACCESS_KEY_ID"))
    exit(1)

ses_client = boto3.client('ses', region_name=os.getenv("AWS_SES_REGION"))

def validate_aws_credentials():
    ses_client.get_send_quota()
    # print("✅ AWS credentials are valid.")

# ✅ Only run once to create template
def create_ses_template():
    response = ses_client.create_template(
        Template={
            'TemplateName': os.getenv("AWS_EMAIL_TEMPLATE"),
            'SubjectPart': '{{subject}}',
            'TextPart': 'Hello {{name}},\nThanks for subscribing to Kunal\'s newsletter.',
            'HtmlPart': """
                        <!DOCTYPE html>
                        <html lang="en">
                        <head>
                            <meta charset="UTF-8">
                            <meta name="viewport" content="width=device-width, initial-scale=1.0">
                            <title>French with Kunal - Your Daily Dose of French!</title>
                            <style>
                                /* Global Styles */
                                body {
                                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                                    margin: 0;
                                    padding: 0;
                                    background-color: #f4f7f6; /* Light gray background for the whole email */
                                    color: #333333;
                                    line-height: 1.6;
                                    -webkit-text-size-adjust: 100%;
                                    -ms-text-size-adjust: 100%;
                                }

                                table {
                                    border-collapse: collapse;
                                    mso-table-lspace: 0pt;
                                    mso-table-rspace: 0pt;
                                }

                                img {
                                    -ms-interpolation-mode: bicubic;
                                }

                                a {
                                    text-decoration: none;
                                    color: #4f46e5;
                                }

                                /* Email Container */
                                .email-container {
                                    max-width: 600px;
                                    margin: 20px auto;
                                    background: #ffffff;
                                    border-radius: 8px; /* Slightly rounded corners for the main container */
                                    overflow: hidden;
                                    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08); /* Soft shadow */
                                }

                                /* Header */
                                .email-header {
                                    background-color: #343a40; /* Changed to a dark gray for a neutral, modern look */
                                    padding: 15px 20px; /* Reduced padding for a smaller header */
                                    text-align: center;
                                    color: #ffffff;
                                    border-top-left-radius: 8px;
                                    border-top-right-radius: 8px;
                                }

                                .header-title {
                                    font-size: 22px; /* Smaller font size for the title */
                                    font-weight: 600; /* Slightly less bold */
                                    margin: 0;
                                    letter-spacing: 0.3px;
                                }

                                /* Body Content */
                                .email-body {
                                    padding: 30px;
                                }

                                .email-body p {
                                    margin-bottom: 15px;
                                    font-size: 16px;
                                }

                                /* Footer */
                                .footer {
                                    padding: 10px 15px; /* Further reduced padding for a much smaller footer */
                                    text-align: center;
                                    font-size: 11px; /* Even smaller font size for the footer text */
                                    color: #aaaaaa; /* Even lighter gray color for the text */
                                    border-top: 1px solid #e8e8e8; /* Even lighter border */
                                    background-color: #f8f8f8; /* Even lighter background for footer */
                                    border-bottom-left-radius: 8px;
                                    border-bottom-right-radius: 8px;
                                }

                                .footer p {
                                    margin: 0 0 4px 0; /* Further reduced margin */
                                }

                                .footer-link {
                                    color: #888888; /* More subtle link color */
                                    text-decoration: none;
                                }

                                .footer-link:hover {
                                    text-decoration: underline;
                                    color: #4f46e5; /* Retain brand color on hover */
                                }

                                .address {
                                    font-style: normal;
                                    margin: 2px 0; /* Further reduced margin */
                                    line-height: 1.2; /* Even tighter line height */
                                }

                                .contact-info {
                                    margin: 6px 0; /* Further reduced margin */
                                }

                                .contact-info a {
                                    color: #888888; /* Keep contact info links subtle */
                                }

                                .contact-info a:hover {
                                    color: #4f46e5;
                                }

                                .unsubscribe {
                                    color: #888888;
                                    text-decoration: underline;
                                }

                                .unsubscribe:hover {
                                    color: #4f46e5;
                                }

                                /* Responsive Styles */
                                @media only screen and (max-width: 620px) {
                                    .email-container {
                                        margin: 0 !important;
                                        border-radius: 0 !important;
                                        box-shadow: none !important;
                                    }
                                    .email-header, .footer {
                                        border-radius: 0 !important;
                                    }
                                    .email-body {
                                        padding: 20px !important;
                                    }
                                    .header-title {
                                        font-size: 20px !important; /* Adjusted for mobile */
                                    }
                                    .footer {
                                        padding: 8px 10px !important; /* Even further reduced for mobile */
                                        font-size: 10px !important; /* Smallest text for mobile */
                                    }
                                }
                            </style>
                        </head>
                        <body>
                            <div class="email-container">
                                <div class="email-header">
                                    <h1 class="header-title">French with Kunal</h1>
                                </div>
                                <div class="email-body">
                                    <!-- Dynamic Content Area -->
                                    {{ content }}
                                    <!-- End Dynamic Content Area -->
                                </div>
                                <div class="footer">
                                    <p>© 2025 French with Kunal. All rights reserved.</p>
                                    <div class="address">
                                        <strong>Mississauga Branch:</strong><br>
                                        4740 Colombo Cres, Mississauga, ON L5M 7R4
                                    </div>
                                    <div class="address">
                                        <strong>Pincourt Branch:</strong><br>
                                        63 5e Avenue, Pincourt, QC J7W 5K8
                                    </div>
                                    <div class="contact-info">
                                        <strong>Phone:</strong> <a href="tel:+15813989477" class="footer-link">+1 (581) 398-9477</a><br>
                                        <strong>Email:</strong> <a href="mailto:info@frenchwithkunal.ca" class="footer-link">info@frenchwithkunal.ca</a>
                                    </div>
                                    <p>
                                        <!-- Placeholder for tracking pixel for preview purposes -->
                                        <img src="https://placehold.co/1x1/ffffff/ffffff?text=" width="1" height="1" alt="" style="display:none;" />
                                        <a href="https://frenchwithkunal.ca/" class="footer-link">Website</a> |
                                        <!-- Placeholder for unsubscribe link for preview purposes -->
                                        <a href="https://marketing-python-app-d83476355f55.herokuapp.com/api/track/click/{{campaign_id}}/{{email}}?redirect={{redirect_url}}" class="unsubscribe">Unsubscribe</a>
                                    </p>
                                </div>
                            </div>
                        </body>
                        </html>


                    """
        }
    )

# def send_bulk_email(sender: str, template_name: str, recipients: list, campaign_id: str, content: str, subject: str, attachment=None):
#     """
#     Send bulk emails with optional PDF attachment.
#     If attachment is provided, individual emails are sent instead of bulk templated emails.
#     """
#     if attachment:
#         # Send individual emails with attachment
#         return send_individual_emails_with_attachment(sender, recipients, campaign_id, content, subject, attachment)
#     else:
#         # Use bulk templated email (no attachments)
#         destinations = []
#         for r in recipients:
#             template_data = {
#                 "name": r.get("name", "Subscriber"),
#                 "campaign_id": campaign_id,
#                 "email": r['email'],
#                 "redirect_url": encoded_redirect,
#                 "subject": subject
#             }
#             destinations.append({
#                 "Destination": {
#                     "ToAddresses": [r['email']]
#                 },
#                 "ReplacementTemplateData": json.dumps(template_data)
#             })

#         response = ses_client.send_bulk_templated_email(
#             Source=sender,
#             Template=template_name,
#             DefaultTemplateData=json.dumps({
#                 "content": content,
#                 "redirect_url": encoded_redirect,
#                 "subject": subject
#             }),
#             Destinations=destinations
#         )
#         return response

def send_bulk_email(sender: str, template_name: str, recipients: list, campaign_id: str, content: str, subject: str, attachment=None):
    """
    Send bulk emails with optional PDF attachment.
    If attachment is provided, individual emails are sent instead of bulk templated emails.
    """
    from services.header_footer import wrap_with_template
    def replace_placeholders(text, recipient, campaign_id):
        # Replace {{name}}, {{email}}, {{campaign_id}} and other placeholders
        name = recipient.get('name', 'Subscriber')
        email = recipient.get('email', '')
        replaced = text.replace('{{name}}', name)
        replaced = replaced.replace('{{email}}', email)
        replaced = replaced.replace('{{campaign_id}}', str(campaign_id))
        replaced = replaced.replace('{{subject}}', subject)
        replaced = replaced.replace('{{content}}', content)
        
        # Handle tracking pixel and unsubscribe links in content
        email_encoded = urllib.parse.quote(email, safe='')
        tracking_pixel = f'<img src="https://marketing-python-app-d83476355f55.herokuapp.com/api/track/open/{{campaign_id}}/{{email_encoded}}" width="1" height="1" alt="" style="display:none;" />'
        unsubscribe_link = f'https://marketing-python-app-d83476355f55.herokuapp.com/api/track/click/{{campaign_id}}/{{email_encoded}}?redirect=https://frenchwithkunal.ca/unsubscribe.html'
        replaced = replaced.replace('{{tracking_pixel}}', tracking_pixel)
        replaced = replaced.replace('{{unsubscribe_link}}', unsubscribe_link)
        return replaced

    sent_count = 0
    failed_count = 0
    errors = []

    if attachment:
        return send_individual_emails_with_attachment(sender, recipients, campaign_id, content, subject, attachment)
    else:
        # Send bulk emails using local template for each recipient
        for recipient in recipients:
            try:
                personalized_content = replace_placeholders(content, recipient, campaign_id)

                # Generate dynamic tracking links
                email = recipient.get('email', '')
                # tracking_pixel = f'<img src="https://marketing-python-app-d83476355f55.herokuapp.com/api/track/open/{campaign_id}/{email}" width="1" height="1" alt="" style="display:none;" />'
                # unsubscribe_link = f'https://frenchwithkunal.ca/unsubscribe.html'

                # Pass the dynamic links to the template wrapper
                html_body = wrap_with_template(personalized_content, campaign_id, email)
                
                msg = MIMEMultipart()
                msg['From'] = sender
                msg['To'] = recipient['email']
                msg['Subject'] = subject
                msg.attach(MIMEText(html_body, 'html'))
                response = ses_client.send_raw_email(
                    Source=sender,
                    Destinations=[recipient['email']],
                    RawMessage={'Data': msg.as_string()}
                )
                sent_count += 1
            except Exception as e:
                failed_count += 1
                errors.append(f"Failed to send to {recipient['email']}: {str(e)}")
        return {
            'sent_count': sent_count,
            'failed_count': failed_count,
            'errors': errors
        }

def send_individual_emails_with_attachment(sender: str, recipients: list, campaign_id: str, content: str, subject: str, attachment: dict):
    """
    Send individual emails with PDF attachment using raw email.
    """
    sent_count = 0
    failed_count = 0
    errors = []
    
    from services.header_footer import wrap_with_template
    def replace_placeholders(text, recipient, campaign_id):
        name = recipient.get('name', 'Subscriber')
        email = recipient.get('email', '')
        replaced = text.replace('{{name}}', name)
        replaced = replaced.replace('{{email}}', email)
        replaced = replaced.replace('{{campaign_id}}', str(campaign_id))
        replaced = replaced.replace('{{subject}}', subject)
        replaced = replaced.replace('{{content}}', content)
        
        # Handle tracking pixel and unsubscribe links in content
        email_encoded = urllib.parse.quote(email, safe='')
        tracking_pixel = f'<img src="https://marketing-python-app-d83476355f55.herokuapp.com/api/track/open/{{campaign_id}}/{{email_encoded}}" width="1" height="1" alt="" style="display:none;" />'
        unsubscribe_link = f'https://marketing-python-app-d83476355f55.herokuapp.com/api/track/click/{{campaign_id}}/{{email_encoded}}?redirect=https://frenchwithkunal.ca/unsubscribe.html'
        replaced = replaced.replace('{{tracking_pixel}}', tracking_pixel)
        replaced = replaced.replace('{{unsubscribe_link}}', unsubscribe_link)
        return replaced

    # This is the corrected for loop
    for recipient in recipients:
        try:
            personalized_content = replace_placeholders(content, recipient, campaign_id)
            
            # Generate dynamic tracking links
            email = recipient.get('email', '')
            tracking_pixel = f'<img src="https://marketing-python-app-d83476355f55.herokuapp.com/api/track/open/{{campaign_id}}/{{email}}" width="1" height="1" alt="" style="display:none;" />'
            unsubscribe_link = f'https://marketing-python-app-d83476355f55.herokuapp.com/api/track/click/{{campaign_id}}/{{email}}?redirect=https://frenchwithkunal.ca/unsubscribe.html'

            # Use the updated wrap_with_template function
            html_body = wrap_with_template(personalized_content, campaign_id, email)
            
            msg = MIMEMultipart()
            msg['From'] = sender
            msg['To'] = recipient['email']
            msg['Subject'] = subject
            msg.attach(MIMEText(html_body, 'html'))
            if attachment and attachment.get('content'):
                pdf_data = base64.b64decode(attachment['content'])
                pdf_attachment = MIMEApplication(pdf_data, _subtype='pdf')
                pdf_attachment.add_header('Content-Disposition', 'attachment', filename=attachment['filename'])
                msg.attach(pdf_attachment)
                
            response = ses_client.send_raw_email(
                Source=sender,
                Destinations=[recipient['email']],
                RawMessage={'Data': msg.as_string()}
            )
            sent_count += 1
        except Exception as e:
            failed_count += 1
            errors.append(f"Failed to send to {recipient['email']}: {str(e)}")
    return {
        'sent_count': sent_count,
        'failed_count': failed_count,
        'errors': errors
    }