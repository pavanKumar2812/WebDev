from flask import Blueprint, send_file
from config import db
from datetime import datetime, timezone
from PIL import Image
import io

tracking_bp = Blueprint("tracking", __name__, url_prefix="/api")

def generate_pixel():
    # Create a transparent 1x1 PNG image
    img = Image.new("RGBA", (1, 1), (0, 0, 0, 0))
    byte_io = io.BytesIO()
    img.save(byte_io, 'PNG')
    byte_io.seek(0)
    return byte_io

@tracking_bp.route('/track/open/<campaign_id>/<recipient_id>.png')
def track_open(campaign_id, recipient_id):
    db.events.insert_one({
        'campaign_id': campaign_id,
        'recipient': recipient_id,
        'event': 'open',
        'timestamp': datetime.now(timezone.utc),
    })

    return send_file(generate_pixel(), mimetype='image/png')

from flask import redirect, request

@tracking_bp.route('/track/click/<campaign_id>/<recipient_id>')
def track_click_redirect(campaign_id, recipient_id):
    db.events.insert_one({
        'campaign_id': campaign_id,
        'recipient': recipient_id,
        'event': 'click',
        'timestamp': datetime.now(timezone.utc),
    })

    redirect_url = request.args.get('redirect')
    if redirect_url:
        return redirect(redirect_url)
    else:
        return "Click tracked, no redirect provided", 200
