from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from models import db, Bench, Adoption

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///benches.db"

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/api/benches", methods=["GET"])
def get_benches():
    """Steps
    1. Get all active entries from adoptions table and all available benches from benches table
    2. cross reference into one dictionary/json format
                    For available benches:
                    {
                        "id": "VC-001",
                        "latitude": 40.897,
                        "longitude": -73.886,
                        "location": "Parade Ground",
                        "available": true,
                        "current_adoption": null
                    }
                    For adopted benches:
                    {
                    "id": "VC-002",
                    "latitude": 40.898,
                    "longitude": -73.885,
                    "location": "Lake Trail",
                    "available": false,
                    "current_adoption": {
                        "donor_name": "Smith Family",
                        "end_date": "2028-06-01"
                    }
                    (the adoption is a json within the json)"""
    benches = Bench.query.all()
    adoptions = Adoption.query.all()
    adoptions_keys_public = ["donor_name", "dedication", "start_date", "end_date"]
    
    #removes admin info from adoption entity and returns keys matched to bench_id only those needed by frontend
    adoptions_by_bench_id = {
        a.bench_id: {
            key: str(getattr(a, key)) if hasattr(getattr(a, key), "isoformat") else getattr(a, key)
            for key in adoptions_keys_public
        }
        for a in adoptions
    }
    full_list = []
    
    for bench in benches:
        matching_adoption = adoptions_by_bench_id.get(bench.id)
        full_list.append({
            "id": bench.id,
            "latitude": bench.latitude,
            "longitude": bench.longitude,
            "location": bench.location,
            "available": matching_adoption is None,
            "current_adoption": matching_adoption
                })

    return jsonify(full_list)

if __name__ == '__main__':
    app.run(debug=True)



