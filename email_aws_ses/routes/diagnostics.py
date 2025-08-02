from flask import Blueprint, jsonify
from datetime import datetime
from collections import defaultdict
from config import db

diagnostics_bp = Blueprint("diagnostics", __name__)

@diagnostics_bp.route("/api/collections", methods=["GET"])
def list_collections():
    collections = db.list_collection_names()
    return jsonify({"collections": collections})

@diagnostics_bp.route("/api/collections/<collection_name>", methods=["GET"])
def get_sample_document(collection_name):
    if collection_name not in db.list_collection_names():
        return jsonify({"error": f"Collection '{collection_name}' does not exist"}), 404

    doc = db[collection_name].find_one()
    if doc:
        doc["_id"] = str(doc["_id"])
        return jsonify(doc)
    return jsonify({"message": "No documents found"}), 404

@diagnostics_bp.route("/api/collections/<collection_name>/all", methods=["GET"])
def get_all_documents(collection_name):
    if collection_name not in db.list_collection_names():
        return jsonify({"error": f"Collection '{collection_name}' does not exist"}), 404

    documents = []
    for doc in db[collection_name].find():
        doc["_id"] = str(doc["_id"])
        documents.append(doc)

    return jsonify(documents)

@diagnostics_bp.route('/api/collections/<collection_name>/subscribed', methods=['GET'])
def get_subscribed_users(collection_name):
    if collection_name not in db.list_collection_names():
        return jsonify({'error': f"Collection '{collection_name}' does not exist"}), 404

    documents = []
    for doc in db[collection_name].find({'isSubscribed': True}):
        doc['_id'] = str(doc['_id'])
        documents.append(doc)

    return jsonify(documents)

# Fetch Data for Collection
@diagnostics_bp.route('/api/collections/<collection_name>/stats', methods=['GET'])
def get_collection_stats(collection_name):
    if collection_name not in db.list_collection_names():
        return jsonify({'error': f"Collection '{collection_name}' does not exist"}), 404

    total = db[collection_name].count_documents({})
    subscribed = db[collection_name].count_documents({'isSubscribed': True})
    non_subscribed = total - subscribed
    sample = list(db[collection_name].find().limit(10))
    for doc in sample:
        doc['_id'] = str(doc['_id'])

    return jsonify({
        "total": total,
        "subscribers": subscribed,
        "nonSubscribers": non_subscribed,
        "sample": sample
    })

# For Visualization: Monthly Subscribers Count
@diagnostics_bp.route('/api/collections/<collection_name>/monthly-subscribers', methods=['GET'])
def get_monthly_subscribers(collection_name):
    if collection_name not in db.list_collection_names():
        return jsonify({'error': f"Collection '{collection_name}' does not exist"}), 404

    cursor = db[collection_name].find({"isSubscribed": True}, {"createdAt": 1})
    month_counts = defaultdict(int)

    for doc in cursor:
        created_at = doc.get("createdAt")
        if isinstance(created_at, str):
            try:
                created_at = datetime.strptime(created_at, "%a, %d %b %Y %H:%M:%S %Z")
            except ValueError:
                continue
        elif not isinstance(created_at, datetime):
            continue

        month_key = created_at.strftime("%Y-%m")
        month_counts[month_key] += 1

    sorted_months = sorted(month_counts.keys())
    return jsonify({
        "months": sorted_months,
        "subscriberCounts": [month_counts[m] for m in sorted_months]
    })
