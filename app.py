from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from models import db, Bench, Adoption
import datetime

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

@app.route("/api/benches/<bench_id>/adopt", methods=["POST"])
def adopt_bench(bench_id):
    # 1. Verify bench exists
    bench = db.session.get(Bench, bench_id)
    if not bench:
        return jsonify({"error": "Bench not found"}), 404

    # 2. Check if bench is already adopted
    existing_adoption = Adoption.query.filter_by(bench_id=bench_id).first()
    if existing_adoption:
        return jsonify({"error": "Bench is already adopted"}), 400

    # 3. Extract data from JSON or form submission
    data = request.get_json() if request.is_json else request.form
    
    if not data or not data.get("donor_name") or not data.get("email"):
        return jsonify({"error": "donor_name and email are required"}), 400

    donor_name = data.get("donor_name").strip()
    email = data.get("email").strip()
    dedication = data.get("dedication", "").strip() or None

    # 4. Calculate 10-year term dates
    today = datetime.date.today()
    start_date = today
    try:
        end_date = today.replace(year=today.year + 10)
    except ValueError:
        # Fallback for leap-year edge cases (e.g. Feb 29)
        end_date = today + datetime.timedelta(days=365 * 10)

    # 5. Create, save, and commit adoption record
    new_adoption = Adoption(
        bench_id=bench.id,
        donor_name=donor_name,
        email=email,
        dedication=dedication,
        start_date=start_date,
        end_date=end_date
    )
    db.session.add(new_adoption)
    db.session.commit()

    return jsonify({
        "message": f"Bench {bench_id} successfully adopted!",
        "adoption": {
            "bench_id": bench.id,
            "donor_name": donor_name,
            "dedication": dedication,
            "start_date": str(start_date),
            "end_date": str(end_date)
        }
    }), 201
    
if __name__ == '__main__':
    app.run(debug=True)



