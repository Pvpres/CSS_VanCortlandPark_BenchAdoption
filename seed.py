import datetime
from app import app
from models import db, Bench, Adoption

BENCHES = [
    {
        "id": "VCP-001",
        "latitude": 40.8884,
        "longitude": -73.8942,
        "location": "Van Cortlandt House Museum - South Lawn"
    },
    {
        "id": "VCP-002",
        "latitude": 40.8895,
        "longitude": -73.8968,
        "location": "Broadway & W 242nd St Entrance"
    },
    {
        "id": "VCP-003",
        "latitude": 40.8912,
        "longitude": -73.8945,
        "location": "Parade Ground - West Running Path"
    },
    {
        "id": "VCP-004",
        "latitude": 40.8935,
        "longitude": -73.8930,
        "location": "Parade Ground - North Bleachers Area"
    },
    {
        "id": "VCP-005",
        "latitude": 40.8876,
        "longitude": -73.8918,
        "location": "Van Cortlandt Lake - South Shore"
    },
    {
        "id": "VCP-006",
        "latitude": 40.8901,
        "longitude": -73.8905,
        "location": "Van Cortlandt Lake - Promenade Bridge"
    },
    {
        "id": "VCP-007",
        "latitude": 40.8924,
        "longitude": -73.8890,
        "location": "Memorial Grove Trail"
    },
    {
        "id": "VCP-008",
        "latitude": 40.8950,
        "longitude": -73.8915,
        "location": "Vault Hill Overlook"
    },
    {
        "id": "VCP-009",
        "latitude": 40.8905,
        "longitude": -73.8858,
        "location": "Van Cortlandt Golf Course Clubhouse"
    },
    {
        "id": "VCP-010",
        "latitude": 40.8938,
        "longitude": -73.8860,
        "location": "John Kieran Nature Trail - South Entrance"
    },
    {
        "id": "VCP-011",
        "latitude": 40.8972,
        "longitude": -73.8845,
        "location": "John Kieran Nature Trail - Marsh View"
    },
    {
        "id": "VCP-012",
        "latitude": 40.9015,
        "longitude": -73.8820,
        "location": "Indian Field - Picnic Pavilion"
    },
    {
        "id": "VCP-013",
        "latitude": 40.9038,
        "longitude": -73.8805,
        "location": "Indian Field - Baseball Diamonds"
    },
    {
        "id": "VCP-014",
        "latitude": 40.8990,
        "longitude": -73.8935,
        "location": "Cross Country Trail - Cemetery Hill"
    },
    {
        "id": "VCP-015",
        "latitude": 40.9025,
        "longitude": -73.8955,
        "location": "Old Croton Aqueduct Trail - Northwest Woods"
    },
    {
        "id": "VCP-016",
        "latitude": 40.8855,
        "longitude": -73.8928,
        "location": "Hester & Piero's Mill Pond"
    },
    {
        "id": "VCP-017",
        "latitude": 40.8830,
        "longitude": -73.8900,
        "location": "Mosholu Parkway Greenway Link"
    },
    {
        "id": "VCP-018",
        "latitude": 40.8870,
        "longitude": -73.8785,
        "location": "Jerome Ave & E 233rd St Entrance"
    },
    {
        "id": "VCP-019",
        "latitude": 40.8955,
        "longitude": -73.8760,
        "location": "Woodlawn Station Path"
    },
    {
        "id": "VCP-020",
        "latitude": 40.9070,
        "longitude": -73.8885,
        "location": "Allen Shandler Recreation Area"
    },
]

ADOPTIONS = [
    # --- Ending Soon (Adopted in 2016, 10-year term ending in 2026) ---
    {
        "bench_id": "VCP-002",
        "donor_name": "Elena & Mateo Rivera",
        "email": "rivera.family@example.com",
        "dedication": "In loving memory of Abuela Sofia, who walked this park every morning.",
        "start_date": datetime.date(2016, 11, 15),
        "end_date": datetime.date(2026, 11, 15)
    },
    {
        "bench_id": "VCP-007",
        "donor_name": "Bronx Historical Society",
        "email": "info@bronxhistorical.org",
        "dedication": "Honoring the brave veterans remembered along Memorial Grove.",
        "start_date": datetime.date(2016, 10, 1),
        "end_date": datetime.date(2026, 10, 1)
    },

    # --- Midterm (Adopted 2020-2022, 10-year term ending 2030-2032) ---
    {
        "bench_id": "VCP-004",
        "donor_name": "Van Cortlandt Track Alumni",
        "email": "alumni@vctrack.org",
        "dedication": "Dedicated to all runners who pushed their limits on the Parade Ground.",
        "start_date": datetime.date(2020, 9, 1),
        "end_date": datetime.date(2030, 9, 1)
    },
    {
        "bench_id": "VCP-011",
        "donor_name": "Friends of John Kieran Trail",
        "email": "kieranfriends@example.com",
        "dedication": "Preserving nature and peaceful bird watching for all Bronx residents.",
        "start_date": datetime.date(2021, 6, 15),
        "end_date": datetime.date(2031, 6, 15)
    },
    {
        "bench_id": "VCP-014",
        "donor_name": "Coach Marcus Williams",
        "email": "coach.marcus@example.com",
        "dedication": "Champions are made on Cemetery Hill. Keep pushing!",
        "start_date": datetime.date(2022, 4, 10),
        "end_date": datetime.date(2032, 4, 10)
    },

    # --- Recently Created (Adopted 2025-2026, 10-year term ending 2035-2036) ---
    {
        "bench_id": "VCP-005",
        "donor_name": "David & Sarah Chen",
        "email": "chen.d@example.com",
        "dedication": "Where we shared our first date by the lake. Forever grateful.",
        "start_date": datetime.date(2025, 5, 20),
        "end_date": datetime.date(2035, 5, 20)
    },
    {
        "bench_id": "VCP-009",
        "donor_name": "The O'Connor Family",
        "email": "oconnor.golf@example.com",
        "dedication": "For Grandpa Joe — may all your drives be straight and your putts true.",
        "start_date": datetime.date(2026, 1, 10),
        "end_date": datetime.date(2036, 1, 10)
    },
    {
        "bench_id": "VCP-018",
        "donor_name": "Woodlawn Community League",
        "email": "community@woodlawnleague.org",
        "dedication": "A resting spot for neighbors, families, and friends of Woodlawn.",
        "start_date": datetime.date(2026, 7, 4),
        "end_date": datetime.date(2036, 7, 4)
    },
]

def seed_benches():
    with app.app_context():
        db.create_all()

        new_count = 0
        for data in BENCHES:
            bench = db.session.get(Bench, data["id"])
            if not bench:
                bench = Bench(
                    id=data["id"],
                    latitude=data["latitude"],
                    longitude=data["longitude"],
                    location=data["location"]
                )
                db.session.add(bench)
                new_count += 1
            else:
                bench.latitude = data["latitude"]
                bench.longitude = data["longitude"]
                bench.location = data["location"]

        db.session.commit()
        print(f"Successfully seeded {len(BENCHES)} benches ({new_count} new, {len(BENCHES) - new_count} updated).")

def seed_adoptions():
    with app.app_context():
        new_count = 0
        for data in ADOPTIONS:
            adoption = Adoption.query.filter_by(bench_id=data["bench_id"]).first()
            if not adoption:
                adoption = Adoption(
                    bench_id=data["bench_id"],
                    donor_name=data["donor_name"],
                    email=data["email"],
                    dedication=data["dedication"],
                    start_date=data["start_date"],
                    end_date=data["end_date"]
                )
                db.session.add(adoption)
                new_count += 1
            else:
                adoption.donor_name = data["donor_name"]
                adoption.email = data["email"]
                adoption.dedication = data["dedication"]
                adoption.start_date = data["start_date"]
                adoption.end_date = data["end_date"]

        db.session.commit()
        print(f"Successfully seeded {len(ADOPTIONS)} adoptions ({new_count} new, {len(ADOPTIONS) - new_count} updated).")

if __name__ == "__main__":
    seed_benches()
    seed_adoptions()

