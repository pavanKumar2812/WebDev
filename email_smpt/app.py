from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson import ObjectId
from email_sender import send_email

import datetime

app = Flask(__name__)

# Place the MongoDB URL
MONGO_URI = ""
client = MongoClient(MONGO_URI)
# Add the mongodb cluster name
db = client.email_marketing_db

@app.route('/')
def home():
    return "Marketing Email Backend is running"

@app.route('/api/subscribers', methods=['POST'])
def add_subscriber():
    data = request.json
    email = data.get('email')
    name = data.get('name', '')
    if not email:
        return jsonify({'error': 'Email is required'}), 400
    
    # Check if subscriber exists
    if db.subscribers.find_one({'email': email}):
        return jsonify({'error': 'Subscriber already exists'}), 400
    
    db.subscribers.insert_one({'email': email,
                               'name': name,
                               'subscribed': True})
    return jsonify({'message': 'Subscriber added successfully'}), 201

@app.route('/api/subscribers', methods=['GET'])
def get_subscriber():
    subscribers = list(db.subscribers.find({}, {"_id": 0}))
    return jsonify(subscribers)

@app.route('/api/campaigns', methods=['POST'])
def create_campaign():
    data = request.json
    name = data.get('name')
    subject = data.get('subject')
    content = data.get('content')

    if not all([name, subject, content]):
        return jsonify({'error': 'Name, subject and content are required'}), 400

    campaign = {
        'name': name,
        'subject': subject,
        'content': content,
        'created_at': datetime.datetime.now(datetime.UTC),
        'status': 'draft'  # status can be draft, sending, sent
    }

    result = db.campaigns.insert_one(campaign)
    return jsonify({'message': 'Campaign created', 'campaign_id': str(result.inserted_id)}), 201

@app.route('/api/campaigns', methods=['GET'])
def get_campaigns():
    campaigns = []
    for doc in db.campaigns.find():
        doc['_id'] = str(doc['_id'])  # Convert ObjectId to string
        campaigns.append(doc)
    return jsonify(campaigns)

@app.route('/api/send', methods=["POST"])
def send_campaigns():
    data = request.json
    campaign_id = data.get('campaign_id')
    
    if not campaign_id:
        return jsonify({'error': 'Campaign ID is required'}), 400

    campaign = db.campaigns.find_one({'_id': ObjectId(campaign_id)})
    
    if not campaign:
        return jsonify({'error': 'Campaign not Found'}), 404

    subscribers = db.subscribers.find({'subscribed': True})
    send_to = []

    for sub in subscribers:
        send_email(sub['email'], campaign['subject'], campaign['content'])
        send_to.append(sub['email'])

    return jsonify({'message': f"Emails sent to {len(send_to)} subscribers"}), 200

if __name__ == "__main__":
    app.run(debug=True)
