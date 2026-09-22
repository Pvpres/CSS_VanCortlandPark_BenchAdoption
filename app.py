from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from models import db, Bench, Adoption
import os
import datetime
import calendar
import heapq
import random

def add_months(sourcedate, months):
    """Add a given number of months to a date, correctly handling leap years and month boundaries."""
    month = sourcedate.month - 1 + months
    year = sourcedate.year + (month // 12)
    month = (month % 12) + 1
    day = min(sourcedate.day, calendar.monthrange(year, month)[1])
    return datetime.date(year, month, day)

def format_duration_text(months):
    """Format duration in months into a clean, human-readable label (e.g. '10 Years', '6 Months')."""
    if not months:
        return "Adoption"
    years = months // 12
    rem = months % 12
    if rem == 0:
        return f"{years} Year" if years == 1 else f"{years} Years"
    elif years == 0:
        return f"{rem} Month" if rem == 1 else f"{rem} Months"
    else:
        return f"{years} yr, {rem} mo"

def format_date_display(d):
    """Format date into 'Mon DD, YYYY' format."""
    if not d:
        return ""
    if hasattr(d, "strftime"):
        return d.strftime("%b %-d, %Y")
    return str(d)

def calculate_tenure_details(adoption, today=None):
    """Compute comprehensive tenure, countdown, and progress bar metrics for an adoption record."""
    if today is None:
        today = datetime.date.today()

    start_date = adoption.start_date
    end_date = adoption.end_date

    duration_months = adoption.duration_months
    if not duration_months and start_date and end_date:
        duration_months = (end_date.year - start_date.year) * 12 + (end_date.month - start_date.month)
    if not duration_months or duration_months <= 0:
        duration_months = 120

    total_days = max(1, (end_date - start_date).days) if (start_date and end_date) else 1
    elapsed_days = (today - start_date).days if start_date else 0
    remaining_days = (end_date - today).days if end_date else 0

    percent_complete = max(0, min(100, int(round((elapsed_days / total_days) * 100))))
    is_expired = remaining_days < 0
    # Ending soon if active and expiring within ~6 months (180 days)
    is_ending_soon = (not is_expired) and (remaining_days <= 180)

    # Elapsed human text
    if elapsed_days < 0:
        elapsed_text = "Starts soon"
    elif elapsed_days < 30:
        elapsed_text = f"{elapsed_days} day{'s' if elapsed_days != 1 else ''}"
    elif elapsed_days < 365:
        m = max(1, elapsed_days // 30)
        elapsed_text = f"{m} month{'s' if m != 1 else ''}"
    else:
        y = elapsed_days // 365
        rem_m = (elapsed_days % 365) // 30
        if rem_m == 0:
            elapsed_text = f"{y} year{'s' if y != 1 else ''}"
        else:
            elapsed_text = f"{y} yr{'s' if y != 1 else ''}, {rem_m} mo"

    # Remaining human countdown text
    if is_expired:
        remaining_text = "Term Expired"
    elif remaining_days == 0:
        remaining_text = "Expires today"
    elif remaining_days == 1:
        remaining_text = "Expires tomorrow"
    elif remaining_days < 30:
        remaining_text = f"{remaining_days} days left"
    elif remaining_days < 365:
        m = max(1, round(remaining_days / 30.4))
        remaining_text = f"~{m} month{'s' if m != 1 else ''} left"
    else:
        y = remaining_days // 365
        rem_m = round((remaining_days % 365) / 30.4)
        if rem_m == 0:
            remaining_text = f"~{y} year{'s' if y != 1 else ''} left"
        else:
            remaining_text = f"~{y} yr, {rem_m} mo left"

    return {
        "donor_name": adoption.donor_name,
        "dedication": adoption.dedication,
        "start_date": str(start_date) if start_date else "",
        "end_date": str(end_date) if end_date else "",
        "start_date_formatted": format_date_display(start_date),
        "end_date_formatted": format_date_display(end_date),
        "duration_months": duration_months,
        "duration_text": format_duration_text(duration_months),
        "elapsed_days": elapsed_days,
        "remaining_days": remaining_days,
        "elapsed_text": elapsed_text,
        "remaining_text": remaining_text,
        "percent_complete": percent_complete,
        "is_ending_soon": is_ending_soon,
        "is_expired": is_expired,
        "status": "expired" if is_expired else ("ending_soon" if is_ending_soon else "adopted")
    }

app = Flask(__name__)

# Database configuration: fallback to local SQLite, or use DATABASE_URL from environment (Postgres/MySQL)
database_url = os.environ.get("DATABASE_URL", "sqlite:///benches.db")
# Fix legacy "postgres://" URLs used by Render/Heroku to "postgresql://" required by SQLAlchemy
if database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

app.config["SQLALCHEMY_DATABASE_URI"] = database_url
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-secret-key-vcp-bench-adoption")

db.init_app(app)

with app.app_context():
    db.create_all()
    # Auto-seed on startup if database is fresh/empty (e.g. initial launch on Render PostgreSQL)
    try:
        if Bench.query.count() == 0:
            print("Database is empty. Automatically seeding 100 benches and initial adoptions...")
            from seed import seed_benches, seed_adoptions
            seed_benches()
            seed_adoptions()
    except Exception as e:
        print(f"Auto-seed check: {e}")

@app.route("/admin/seed", methods=["GET", "POST"])
def admin_seed():
    """Manual seed endpoint accessible in the browser for environments without shell access (e.g. Render Free)."""
    from seed import seed_benches, seed_adoptions
    reset = request.args.get("reset", "0") in ("1", "true", "True")
    seed_benches(reset=reset)
    seed_adoptions(reset=reset)
    return jsonify({
        "status": "success",
        "message": "Database seeded successfully!",
        "benches": Bench.query.count(),
        "adoptions": Adoption.query.count()
    })

@app.route("/")
def index():
    benches_data = get_benches().get_json()
    return render_template('index.html', benches=benches_data)

@app.route("/api/benches", methods=["GET"])
def get_benches():
    today = datetime.date.today()
    benches = Bench.query.all()
    adoptions = Adoption.query.all()
    
    # Calculate detailed tenure metrics for adoptions
    adoptions_by_bench_id = {}
    for a in adoptions:
        details = calculate_tenure_details(a, today)
        existing = adoptions_by_bench_id.get(a.bench_id)
        # Prefer active (non-expired) adoptions
        if not existing or (existing["is_expired"] and not details["is_expired"]):
            adoptions_by_bench_id[a.bench_id] = details

    full_list = []
    for bench in benches:
        adoption_info = adoptions_by_bench_id.get(bench.id)
        is_available = adoption_info is None or adoption_info.get("is_expired", False)

        bench_status = "available"
        if not is_available:
            bench_status = "ending_soon" if adoption_info.get("is_ending_soon") else "adopted"

        full_list.append({
            "id": bench.id,
            "latitude": bench.latitude,
            "longitude": bench.longitude,
            "location": bench.location,
            "area": bench.area,
            "setting": bench.setting,
            "near_lake": bench.near_lake,
            "near_entrance": bench.near_entrance,
            "near_trail": bench.near_trail,
            "near_recreational_facility": bench.near_recreational_facility,
            "available": is_available,
            "status": bench_status,
            "current_adoption": adoption_info if not is_available else None,
            "past_adoption": adoption_info if is_available and adoption_info else None
        })

    return jsonify(full_list)

@app.route("/api/benches/<bench_id>/adopt", methods=["POST"])
def adopt_bench(bench_id):
    today = datetime.date.today()
    # 1. Verify bench exists
    bench = db.session.get(Bench, bench_id)
    if not bench:
        return jsonify({"error": "Bench not found"}), 404

    # 2. Check if bench is already actively adopted
    existing_adoption = Adoption.query.filter_by(bench_id=bench_id).filter(Adoption.end_date >= today).first()
    if existing_adoption:
        return jsonify({"error": "Bench is currently adopted"}), 400

    # 3. Extract data from JSON or form submission
    data = request.get_json() if request.is_json else request.form
    
    if not data or not data.get("donor_name") or not data.get("email"):
        return jsonify({"error": "donor_name and email are required"}), 400

    donor_name = data.get("donor_name").strip()
    email = data.get("email").strip()
    dedication = data.get("dedication", "").strip() or None

    # 4. Extract and validate duration_months (minimum 6 months up to 10 years / 120 months)
    duration_months_raw = data.get("duration_months")
    if duration_months_raw is None:
        duration_months = 120
    else:
        try:
            duration_months = int(duration_months_raw)
        except (ValueError, TypeError):
            return jsonify({"error": "duration_months must be a valid integer"}), 400

    if duration_months < 6 or duration_months > 120:
        return jsonify({"error": "Adoption length must be between 6 months and 10 years (6 to 120 months)"}), 400

    # 5. Calculate term dates
    start_date = today
    end_date = add_months(today, duration_months)

    # 6. Create, save, and commit adoption record
    new_adoption = Adoption(
        bench_id=bench.id,
        donor_name=donor_name,
        email=email,
        dedication=dedication,
        start_date=start_date,
        end_date=end_date,
        duration_months=duration_months
    )
    db.session.add(new_adoption)
    db.session.commit()

    tenure_details = calculate_tenure_details(new_adoption, today)

    return jsonify({
        "message": f"Bench {bench_id} successfully adopted!",
        "adoption": tenure_details
    }), 201
    

@app.route("/api/benches/recommend", methods=["POST"])
def recommend_bench():
    data = request.get_json(silent=True) or {}

    pref_setting = data.get("setting")            
    pref_area = data.get("area")                 
    pref_features = data.get("preferences", [])   

    if not isinstance(pref_features, list):
        pref_features = []

    allowed_features = {
        "near_lake": "Near Lake / Water",
        "near_entrance": "Near Park Entrance",
        "near_trail": "Near Nature Trail",
        "near_recreational_facility": "Near Recreational Facility"
    }
    valid_features = [f for f in pref_features if f in allowed_features]
    
    # 1. Fetch available benches (exclude currently active adoptions)
    today = datetime.date.today()
    active_adoptions = Adoption.query.filter(Adoption.end_date >= today).all()
    adopted_ids = {a.bench_id for a in active_adoptions}
    available_benches = [b for b in Bench.query.all() if b.id not in adopted_ids]
    
    if not available_benches:
        return jsonify({
            "message": "No benches currently available for adoption.",
            "recommendations": []
        }), 200

    # 2. Shuffle to break ties fairly among equal scores
    random.shuffle(available_benches)

    # 3. Score benches (+1 for each match)
    ranked = []
    for bench in available_benches:
        score = 0
        reasons = []

        # Setting match (+1)
        if pref_setting and bench.setting and bench.setting.lower() == pref_setting.lower():
            score += 1
            reasons.append(f"{bench.setting.capitalize()} setting")

        # Area match (+1)
        if pref_area and bench.area and bench.area.lower() == pref_area.lower():
            score += 1
            reasons.append(f"Located in {bench.area}")

        # Proximity flags match (+1 each)
        for feat in valid_features:
            if getattr(bench, feat, False):
                score += 1
                reasons.append(allowed_features[feat])

        ranked.append({
            "bench": {
                "id": bench.id,
                "location": bench.location,
                "area": bench.area,
                "setting": bench.setting,
                "latitude": bench.latitude,
                "longitude": bench.longitude,
                "near_lake": bench.near_lake,
                "near_entrance": bench.near_entrance,
                "near_trail": bench.near_trail,
                "near_recreational_facility": bench.near_recreational_facility,
            },
            "score": score,
            "reasons": reasons
        })

    # 4. Use min-heap via heapq.nlargest for O(N log K) time complexity with K = 5
    positive_scored = [b for b in ranked if b["score"] > 0]
    if positive_scored:
        top_5 = heapq.nlargest(5, positive_scored, key=lambda x: x["score"])
    else:
        # Fallback if no criteria matched: return 5 random available benches
        top_5 = heapq.nlargest(5, ranked, key=lambda x: x["score"])

    return jsonify({
        "total_available": len(available_benches),
        "total_matching": len(positive_scored),
        "recommendations": top_5
    }), 200

@app.route("/api/locate", methods=["GET", "POST"])
def locate_adoption():
    today = datetime.date.today()
    if request.method == "GET":
        data = request.args
    else:
        data = request.get_json(silent=True) if request.is_json else (request.form or {})

    donor_query = (data.get("donor_name") or "").strip()
    if not donor_query:
        return jsonify({"error": "donor_name is required"}), 400

    matches = db.session.query(Bench, Adoption).join(
        Adoption, Bench.id == Adoption.bench_id
    ).filter(
        Adoption.donor_name.ilike(f"%{donor_query}%")
    ).all()

    return jsonify({
        "count": len(matches),
        "benches": [
            {
                "id": bench.id,
                "location": bench.location,
                "area": bench.area,
                "latitude": bench.latitude,
                "longitude": bench.longitude,
                "adoption": calculate_tenure_details(adoption, today)
            }
            for bench, adoption in matches
        ]
    }), 200

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_DEBUG", "0") in ("1", "true", "True")
    app.run(host="0.0.0.0", port=port, debug=debug)



