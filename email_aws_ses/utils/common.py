from bson import ObjectId
from bson.errors import InvalidId
from config import db

def get_object_id(id_str):
    try:
        return ObjectId(id_str)
    except (InvalidId, TypeError):
        return None

def get_collection(name):
    return db[name]

def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def get_campaign_or_dummy(campaign_id):
    obj_id = get_object_id(campaign_id)
    if not obj_id:
        return None, 'Invalid Campaign ID'

    try:
        campaign = db.campaigns.find_one({'_id': obj_id})
        if not campaign:
            # print("Campaign not found. Using dummy campaign.")
            campaign = {
                "subject": "Test Campaign Subject",
                "content": "This is a test email content for the dummy campaign."
            }
        return campaign, None
    except Exception as e:
        # print(f"Error accessing campaign: {e}. Using dummy campaign.")
        campaign = {
            "subject": "Test Campaign Subject",
            "content": "This is a test email content for the dummy campaign."
        }
        return campaign, None

def get_recipients():
    collections = [
        ("subscribers", "email", "isSubscribed"),
        ("users", "email", "isSubscribed"),
        ("quebec_city", "Email", "isSubscribed"),
        ("quebec_cities", "Email", "isSusbscribed"),  # typo retained
        ("Schools_ontario", "Unnamed: 11", "isSubscribed"),
        ("ontario_schools_2", "email", "isSubscribed"),
        ("University_hr", "email", "isSubscribed")
    ]

    all_emails = set()
    recipients = []

    for collection_name, email_field, subscribed_field in collections:
        try:
            docs = db[collection_name].find({subscribed_field: True})
            for doc in docs:
                email = doc.get(email_field)
                if email and email not in all_emails:
                    all_emails.add(email)
                    recipients.append({
                        "email": email,
                        "name": doc.get("name", "Subscriber")
                    })
        except Exception as e:
            # print(f"Error accessing collection {collection_name}: {e}")
            continue

    return recipients
