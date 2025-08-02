# header_footer.py

HEADER = """
<div class="email-header">
    <h1 class="header-title">French with Kunal</h1>
</div>
"""

FOOTER = """
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
        {{tracking_pixel}}
        <a href="{{website_link}}" class="footer-link">Website</a> |  
        <a href="{{unsubscribe_link}}" class="unsubscribe">Unsubscribe</a>
    </p>
</div>
"""

# STYLE = """
# <style>
#     body {
#         font-family: Arial, sans-serif;
#         margin: 0;
#         padding: 0;
#         color: #333333;
#         line-height: 1.5;
#     }
#     .email-container {
#         max-width: 600px;
#         margin: 0 auto;
#         background: #ffffff;
#     }
#     .email-header {
#         background-color: #4f46e5;
#         padding: 20px;
#         text-align: center;
#     }
#     .header-title {
#         color: #ffffff;
#         font-size: 20px;
#         margin: 0;
#     }
#     .email-body {
#         padding: 30px 20px;
#     }
#     .footer {
#         padding: 15px;
#         text-align: center;
#         font-size: 12px;
#         color: #777777;
#         border-top: 1px solid #eeeeee;
#     }
#     .footer-link {
#         color: #4f46e5;
#         text-decoration: none;
#     }
#     .unsubscribe {
#         color: #777777;
#         text-decoration: underline;
#     }
#     .contact-info {
#         margin: 8px 0;
#         line-height: 1.4;
#     }
#     .address {
#         font-style: normal;
#         margin: 5px 0;
#     }
# </style>
# """

STYLE = """
<style>
    body {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        margin: 0;
        padding: 0;
        background-color: #f4f7f6;
        color: #333333;
        line-height: 1.6;
        -webkit-text-size-adjust: 100%;
        -ms-text-size-adjust: 100%;
    }
    .email-container {
        max-width: 600px;
        margin: 20px auto;
        background: #ffffff;
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 4px 16px rgba(0,0,0,0.10);
    }
    .email-header {
        background-color: #343a40;
        padding: 18px 24px;
        text-align: center;
        color: #ffffff;
        border-top-left-radius: 10px;
        border-top-right-radius: 10px;
    }
    .header-title {
        font-size: 24px;
        font-weight: 700;
        margin: 0;
        letter-spacing: 0.5px;
    }
    .email-body {
        padding: 32px 24px;
        font-size: 16px;
    }
    .footer {
        padding: 12px 18px;
        text-align: center;
        font-size: 12px;
        color: #aaaaaa;
        border-top: 1px solid #e8e8e8;
        background-color: #f8f8f8;
        border-bottom-left-radius: 10px;
        border-bottom-right-radius: 10px;
    }
    .footer-link {
        color: #4f46e5;
        text-decoration: none;
        font-weight: 500;
    }
    .footer-link:hover {
        text-decoration: underline;
        color: #343a40;
    }
    .unsubscribe {
        color: #888888;
        text-decoration: underline;
        font-weight: 500;
    }
    .unsubscribe:hover {
        color: #4f46e5;
    }
    .contact-info {
        margin: 8px 0;
        line-height: 1.4;
    }
    .address {
        font-style: normal;
        margin: 4px 0;
        line-height: 1.2;
    }
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
            padding: 18px !important;
            font-size: 15px !important;
        }
        .header-title {
            font-size: 20px !important;
        }
        .footer {
            padding: 8px 10px !important;
            font-size: 10px !important;
        }
    }
</style>
"""

def wrap_with_template(html_content: str, campaign_id: str = None, recipient_email: str = None) -> str:
    # Generate tracking links
    if campaign_id and recipient_email:
        import urllib.parse
        email_encoded = urllib.parse.quote(recipient_email, safe='')
        website_link = f'https://marketing-python-app-d83476355f55.herokuapp.com/api/track/click/{{campaign_id}}/{{email_encoded}}?redirect=https://frenchwithkunal.ca/'
        unsubscribe_link = f'https://marketing-python-app-d83476355f55.herokuapp.com/api/track/click/{{campaign_id}}/{{email_encoded}}?redirect=https://frenchwithkunal.ca/unsubscribe.html'
        tracking_pixel = f'<img src="https://marketing-python-app-d83476355f55.herokuapp.com/api/track/open/{{campaign_id}}/{{email_encoded}}" width="1" height="1" alt="" style="display:none;" />'
    else:
        # Fallback to direct links if tracking info not provided
        website_link = 'https://frenchwithkunal.ca/'
        unsubscribe_link = 'https://frenchwithkunal.ca/unsubscribe.html'
        tracking_pixel = ''
    
    # Replace placeholders in footer
    footer_with_links = FOOTER.replace('{{website_link}}', website_link).replace('{{unsubscribe_link}}', unsubscribe_link).replace('{{tracking_pixel}}', tracking_pixel)
    
    return f"""<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>French with Kunal</title>
    {STYLE}
</head>
<body>
    <div class="email-container">
        {HEADER}
        <div class="email-body">
            {html_content}
        </div>
        {footer_with_links}
    </div>
</body>
</html>
"""