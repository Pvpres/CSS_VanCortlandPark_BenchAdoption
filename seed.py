from app import app
from models import db, Bench

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

if __name__ == "__main__":
    seed_benches()

