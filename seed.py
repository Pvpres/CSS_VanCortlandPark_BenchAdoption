import datetime
import calendar
from app import app
from models import db, Bench, Adoption

def add_months(sourcedate, months):
    """Add a given number of months to a date, correctly handling leap years and month boundaries."""
    month = sourcedate.month - 1 + months
    year = sourcedate.year + (month // 12)
    month = (month % 12) + 1
    day = min(sourcedate.day, calendar.monthrange(year, month)[1])
    return datetime.date(year, month, day)

# 100 Benches across Van Cortlandt Park
BENCHES = [
    # --- Van Cortlandt House Museum & South Lawn ---
    {"id": "VCP-001", "latitude": 40.8884, "longitude": -73.8942, "location": "Van Cortlandt House Museum - South Lawn"},
    {"id": "VCP-002", "latitude": 40.8895, "longitude": -73.8968, "location": "Broadway & W 242nd St Entrance"},
    {"id": "VCP-003", "latitude": 40.8912, "longitude": -73.8945, "location": "Parade Ground - West Running Path"},
    {"id": "VCP-004", "latitude": 40.8935, "longitude": -73.8930, "location": "Parade Ground - North Bleachers Area"},
    {"id": "VCP-005", "latitude": 40.8876, "longitude": -73.8918, "location": "Van Cortlandt Lake - South Shore"},
    {"id": "VCP-006", "latitude": 40.8901, "longitude": -73.8905, "location": "Van Cortlandt Lake - Promenade Bridge"},
    {"id": "VCP-007", "latitude": 40.8924, "longitude": -73.8890, "location": "Memorial Grove Trail"},
    {"id": "VCP-008", "latitude": 40.8950, "longitude": -73.8915, "location": "Vault Hill Overlook"},
    {"id": "VCP-009", "latitude": 40.8905, "longitude": -73.8858, "location": "Van Cortlandt Golf Course Clubhouse"},
    {"id": "VCP-010", "latitude": 40.8938, "longitude": -73.8860, "location": "John Kieran Nature Trail - South Entrance"},
    {"id": "VCP-011", "latitude": 40.8972, "longitude": -73.8845, "location": "John Kieran Nature Trail - Marsh View"},
    {"id": "VCP-012", "latitude": 40.9015, "longitude": -73.8820, "location": "Indian Field - Picnic Pavilion"},
    {"id": "VCP-013", "latitude": 40.9038, "longitude": -73.8805, "location": "Indian Field - Baseball Diamonds"},
    {"id": "VCP-014", "latitude": 40.8990, "longitude": -73.8935, "location": "Cross Country Trail - Cemetery Hill"},
    {"id": "VCP-015", "latitude": 40.9025, "longitude": -73.8955, "location": "Old Croton Aqueduct Trail - Northwest Woods"},
    {"id": "VCP-016", "latitude": 40.8855, "longitude": -73.8928, "location": "Hester & Piero's Mill Pond"},
    {"id": "VCP-017", "latitude": 40.8830, "longitude": -73.8900, "location": "Mosholu Parkway Greenway Link"},
    {"id": "VCP-018", "latitude": 40.8870, "longitude": -73.8785, "location": "Jerome Ave & E 233rd St Entrance"},
    {"id": "VCP-019", "latitude": 40.8955, "longitude": -73.8760, "location": "Woodlawn Station Path"},
    {"id": "VCP-020", "latitude": 40.9070, "longitude": -73.8885, "location": "Allen Shandler Recreation Area"},
    {"id": "VCP-021", "latitude": 40.8880, "longitude": -73.8948, "location": "Van Cortlandt House - Herb Garden Path"},
    {"id": "VCP-022", "latitude": 40.8868, "longitude": -73.8980, "location": "Broadway & W 240th St Plaza"},
    {"id": "VCP-023", "latitude": 40.8890, "longitude": -73.8960, "location": "Classic Playground - North Gate"},
    {"id": "VCP-024", "latitude": 40.8918, "longitude": -73.8932, "location": "Parade Ground - Cricket Pitch #1 Pavilion"},
    {"id": "VCP-025", "latitude": 40.8930, "longitude": -73.8950, "location": "Parade Ground - Cricket Pitch #4 Shade Trees"},
    {"id": "VCP-026", "latitude": 40.8942, "longitude": -73.8940, "location": "Parade Ground - Gaelic Football Field Sideline"},
    {"id": "VCP-027", "latitude": 40.8925, "longitude": -73.8958, "location": "Parade Ground - Track & Field Finish Line"},
    {"id": "VCP-028", "latitude": 40.8938, "longitude": -73.8975, "location": "Broadway & W 246th St Path"},
    {"id": "VCP-029", "latitude": 40.8888, "longitude": -73.8922, "location": "Van Cortlandt Lake - West Shore Willow Grove"},
    {"id": "VCP-030", "latitude": 40.8895, "longitude": -73.8898, "location": "Van Cortlandt Lake - East Bank Fishing Pier"},
    {"id": "VCP-031", "latitude": 40.8915, "longitude": -73.8892, "location": "Van Cortlandt Lake - North Wetland Overlook"},
    {"id": "VCP-032", "latitude": 40.8865, "longitude": -73.8925, "location": "Van Cortlandt Lake - Historic Mill Remains"},
    {"id": "VCP-033", "latitude": 40.8930, "longitude": -73.8885, "location": "Tibbetts Brook - South Footbridge"},
    {"id": "VCP-034", "latitude": 40.8955, "longitude": -73.8875, "location": "Tibbetts Brook - Wetland Bird Blind"},
    {"id": "VCP-035", "latitude": 40.8920, "longitude": -73.8882, "location": "Memorial Grove - Bronze Plaque Circle"},
    {"id": "VCP-036", "latitude": 40.8930, "longitude": -73.8898, "location": "Memorial Grove - Veteran Oak Canopy"},
    {"id": "VCP-037", "latitude": 40.8958, "longitude": -73.8910, "location": "Vault Hill - Historic Cemetery Enclosure"},
    {"id": "VCP-038", "latitude": 40.8945, "longitude": -73.8922, "location": "Vault Hill - South Ridge Meadow"},
    {"id": "VCP-039", "latitude": 40.8962, "longitude": -73.8928, "location": "Vault Hill - West Slope Trail"},
    {"id": "VCP-040", "latitude": 40.8908, "longitude": -73.8862, "location": "Golf Clubhouse - Putting Green Terrace"},
    {"id": "VCP-041", "latitude": 40.8915, "longitude": -73.8850, "location": "Golf Course - 1st Hole Tee Box"},
    {"id": "VCP-042", "latitude": 40.8890, "longitude": -73.8840, "location": "Golf Course - 9th Green Rest Area"},
    {"id": "VCP-043", "latitude": 40.8920, "longitude": -73.8835, "location": "Golf Course - 10th Hole Scenic Turn"},
    {"id": "VCP-044", "latitude": 40.8900, "longitude": -73.8852, "location": "Golf Course - 18th Fairway Pines"},
    {"id": "VCP-045", "latitude": 40.8882, "longitude": -73.8870, "location": "Bailey Ave & Golf Course Service Gate"},
    {"id": "VCP-046", "latitude": 40.8950, "longitude": -73.8855, "location": "John Kieran Trail - Red Maple Swamp Boardwalk"},
    {"id": "VCP-047", "latitude": 40.8962, "longitude": -73.8848, "location": "John Kieran Trail - Cattail Marsh Clearing"},
    {"id": "VCP-048", "latitude": 40.8985, "longitude": -73.8840, "location": "John Kieran Trail - North Spur"},
    {"id": "VCP-049", "latitude": 40.8995, "longitude": -73.8850, "location": "Tibbetts Brook - Old Railway Grade Path"},
    {"id": "VCP-050", "latitude": 40.8940, "longitude": -73.8955, "location": "Cross Country Course - The Flats"},
    {"id": "VCP-051", "latitude": 40.8965, "longitude": -73.8945, "location": "Cross Country Course - Cowpath Start"},
    {"id": "VCP-052", "latitude": 40.8980, "longitude": -73.8960, "location": "Cross Country Course - Back Hills Crest"},
    {"id": "VCP-053", "latitude": 40.8955, "longitude": -73.8965, "location": "Cross Country Course - Freshmans 1.5M Turn"},
    {"id": "VCP-054", "latitude": 40.8928, "longitude": -73.8952, "location": "Cross Country Course - Historic 5K Finish Chute"},
    {"id": "VCP-055", "latitude": 40.8988, "longitude": -73.8978, "location": "Cass Gallagher Nature Trail - West Loop"},
    {"id": "VCP-056", "latitude": 40.9008, "longitude": -73.8965, "location": "Cass Gallagher Nature Trail - Rocky Escarpment"},
    {"id": "VCP-057", "latitude": 40.8998, "longitude": -73.8985, "location": "Cass Gallagher Nature Trail - Fern Glen"},
    {"id": "VCP-058", "latitude": 40.9015, "longitude": -73.8980, "location": "Northwest Woods - Bridle Path Junction"},
    {"id": "VCP-059", "latitude": 40.9035, "longitude": -73.8970, "location": "Northwest Woods - Spring Pond Shaded Bench"},
    {"id": "VCP-060", "latitude": 40.8975, "longitude": -73.8992, "location": "Riverdale Stables Entrance & Trailhead"},
    {"id": "VCP-061", "latitude": 40.8985, "longitude": -73.8990, "location": "Broadway & W 251st St Entrance"},
    {"id": "VCP-062", "latitude": 40.9020, "longitude": -73.8995, "location": "Broadway & Mosholu Ave Pedestrian Gateway"},
    {"id": "VCP-063", "latitude": 40.9045, "longitude": -73.8960, "location": "Old Croton Aqueduct - Keeper's Gate Marker"},
    {"id": "VCP-064", "latitude": 40.9070, "longitude": -73.8950, "location": "Old Croton Aqueduct - High Stone Culvert"},
    {"id": "VCP-065", "latitude": 40.9095, "longitude": -73.8945, "location": "Northwest Woods - Yonkers City Line Boundary"},
    {"id": "VCP-066", "latitude": 40.8985, "longitude": -73.8910, "location": "John Muir Nature Trail - West Trailhead"},
    {"id": "VCP-067", "latitude": 40.8995, "longitude": -73.8890, "location": "John Muir Nature Trail - Tulip Tree Hollow"},
    {"id": "VCP-068", "latitude": 40.9010, "longitude": -73.8875, "location": "John Muir Nature Trail - Glacial Erratics Boulder"},
    {"id": "VCP-069", "latitude": 40.9018, "longitude": -73.8855, "location": "John Muir Nature Trail - East Terminus"},
    {"id": "VCP-070", "latitude": 40.9030, "longitude": -73.8880, "location": "Central Forest - Beech & Oak Sanctuary"},
    {"id": "VCP-071", "latitude": 40.9042, "longitude": -73.8895, "location": "Central Forest - Mossy Brook Crossing"},
    {"id": "VCP-072", "latitude": 40.9022, "longitude": -73.8810, "location": "Indian Field - Little League Field #1"},
    {"id": "VCP-073", "latitude": 40.9030, "longitude": -73.8818, "location": "Indian Field - Little League Field #2"},
    {"id": "VCP-074", "latitude": 40.9010, "longitude": -73.8830, "location": "Indian Field - Shaded Oak Picnic Area"},
    {"id": "VCP-075", "latitude": 40.9045, "longitude": -73.8798, "location": "Indian Field - North Playground Plaza"},
    {"id": "VCP-076", "latitude": 40.9052, "longitude": -73.8812, "location": "Indian Field - Dog Run Overlook"},
    {"id": "VCP-077", "latitude": 40.9032, "longitude": -73.8785, "location": "Van Cortlandt Park East & E 242nd St Entrance"},
    {"id": "VCP-078", "latitude": 40.9010, "longitude": -73.8778, "location": "Van Cortlandt Park East & E 240th St Path"},
    {"id": "VCP-079", "latitude": 40.9065, "longitude": -73.8895, "location": "Shandler Recreation - Picnic Grove #1"},
    {"id": "VCP-080", "latitude": 40.9075, "longitude": -73.8878, "location": "Shandler Recreation - Pavilion South"},
    {"id": "VCP-081", "latitude": 40.9082, "longitude": -73.8888, "location": "Shandler Recreation - Ballfield #1 Dugout"},
    {"id": "VCP-082", "latitude": 40.9062, "longitude": -73.8875, "location": "Shandler Recreation - Children's Play Area"},
    {"id": "VCP-083", "latitude": 40.9105, "longitude": -73.8890, "location": "North Woods Trail - Yonkers Border Ridge"},
    {"id": "VCP-084", "latitude": 40.9088, "longitude": -73.8868, "location": "North Woods Trail - Shandler Woodland Loop"},
    {"id": "VCP-085", "latitude": 40.9060, "longitude": -73.8845, "location": "Jerome Ave & Shandler Entrance Plaza"},
    {"id": "VCP-086", "latitude": 40.8840, "longitude": -73.8880, "location": "Mosholu Parkway - Greenway Bikeway Rest Stop"},
    {"id": "VCP-087", "latitude": 40.8850, "longitude": -73.8835, "location": "Mosholu Golf Driving Range - Spectator Area"},
    {"id": "VCP-088", "latitude": 40.8860, "longitude": -73.8810, "location": "Mosholu Golf Course - 1st Hole View"},
    {"id": "VCP-089", "latitude": 40.8845, "longitude": -73.8790, "location": "Jerome Ave & Gun Hill Rd Gateway"},
    {"id": "VCP-090", "latitude": 40.8885, "longitude": -73.8770, "location": "Woodlawn Playground - South Gate"},
    {"id": "VCP-091", "latitude": 40.8895, "longitude": -73.8765, "location": "Woodlawn Playground - Water Feature Terrace"},
    {"id": "VCP-092", "latitude": 40.8920, "longitude": -73.8768, "location": "Woodlawn Path - Old Croton Aqueduct Cross"},
    {"id": "VCP-093", "latitude": 40.8940, "longitude": -73.8755, "location": "Van Cortlandt Park East & E 236th St Entrance"},
    {"id": "VCP-094", "latitude": 40.8980, "longitude": -73.8762, "location": "Van Cortlandt Park East & E 238th St Path"},
    {"id": "VCP-095", "latitude": 40.8878, "longitude": -73.8965, "location": "Stadium Path - Van Cortlandt Stadium West"},
    {"id": "VCP-096", "latitude": 40.8870, "longitude": -73.8955, "location": "Stadium Path - Grandstand Lawn"},
    {"id": "VCP-097", "latitude": 40.8890, "longitude": -73.8985, "location": "Broadway & Manhattan College Pkwy Walkway"},
    {"id": "VCP-098", "latitude": 40.8845, "longitude": -73.8912, "location": "Tibbetts Tailrace - Greenway Crossing"},
    {"id": "VCP-099", "latitude": 40.8888, "longitude": -73.8935, "location": "Van Cortlandt House - Colonial Orchard Edge"},
    {"id": "VCP-100", "latitude": 40.8968, "longitude": -73.8918, "location": "Vault Hill - Meadow Crest Sunset Point"},
]

# 35 Adopted Benches (35% of 100 benches)
# Spanning all new duration lengths: 6 Mo (4), 1 Yr (4), 2 Yr (5), 3 Yr (4), 4 Yr (5), 5 Yr (4), 7 Yr (5), 10 Yr (4)
ADOPTIONS = [
    # ==========================================
    # --- 6 Months Duration (value="6") [4] ---
    # ==========================================
    {
        "bench_id": "VCP-003",
        "donor_name": "Bronx Road Runners Club",
        "email": "info@bronxrunners.org",
        "dedication": "In honor of all early morning runners pushing their personal bests.",
        "start_date": datetime.date(2026, 3, 1),
        "duration_months": 6,
        "end_date": datetime.date(2026, 9, 1),
    },
    {
        "bench_id": "VCP-015",
        "donor_name": "Maya & Julian Thorne",
        "email": "thorne.family@example.com",
        "dedication": "For the tranquility of Northwest Woods. Keep our trails wild.",
        "start_date": datetime.date(2026, 5, 15),
        "duration_months": 6,
        "end_date": datetime.date(2026, 11, 15),
    },
    {
        "bench_id": "VCP-022",
        "donor_name": "Kingsbridge Merchants Association",
        "email": "merchants@kingsbridge.org",
        "dedication": "Welcoming all neighbors and visitors to Van Cortlandt Park.",
        "start_date": datetime.date(2026, 8, 1),
        "duration_months": 6,
        "end_date": datetime.date(2027, 2, 1),
    },
    {
        "bench_id": "VCP-038",
        "donor_name": "Chloe Bennett",
        "email": "chloe.b@example.com",
        "dedication": "A peaceful perch above the park to sit, breathe, and dream.",
        "start_date": datetime.date(2026, 9, 10),
        "duration_months": 6,
        "end_date": datetime.date(2027, 3, 10),
    },

    # ==========================================
    # --- 1 Year Duration (value="12") [4] ---
    # ==========================================
    {
        "bench_id": "VCP-006",
        "donor_name": "Lucas & Emily Zhang",
        "email": "zhang.lucas@example.com",
        "dedication": "Where we watched the swans on our first autumn together.",
        "start_date": datetime.date(2025, 10, 1),
        "duration_months": 12,
        "end_date": datetime.date(2026, 10, 1),
    },
    {
        "bench_id": "VCP-013",
        "donor_name": "North Bronx Little League",
        "email": "board@northbronxll.org",
        "dedication": "Cheering on generations of Bronx youth baseball players.",
        "start_date": datetime.date(2025, 12, 1),
        "duration_months": 12,
        "end_date": datetime.date(2026, 12, 1),
    },
    {
        "bench_id": "VCP-029",
        "donor_name": "Amara Patel",
        "email": "amara.patel@example.com",
        "dedication": "Under the willows, finding stillness in the middle of the Bronx.",
        "start_date": datetime.date(2026, 2, 15),
        "duration_months": 12,
        "end_date": datetime.date(2027, 2, 15),
    },
    {
        "bench_id": "VCP-044",
        "donor_name": "VCP Senior Golf League",
        "email": "seniors@vcpgolf.org",
        "dedication": "Good friends, good swings, and 19th hole memories.",
        "start_date": datetime.date(2026, 6, 1),
        "duration_months": 12,
        "end_date": datetime.date(2027, 6, 1),
    },

    # ==========================================
    # --- 2 Years Duration (value="24") [5] ---
    # ==========================================
    {
        "bench_id": "VCP-008",
        "donor_name": "The Morales Family",
        "email": "morales.c@example.com",
        "dedication": "In loving memory of Roberto Morales — lover of open skies and high views.",
        "start_date": datetime.date(2024, 8, 15),
        "duration_months": 24,
        "end_date": datetime.date(2026, 8, 15),
    },
    {
        "bench_id": "VCP-025",
        "donor_name": "Caribbean American Sports Club",
        "email": "casc.bronx@example.com",
        "dedication": "Honoring Sunday afternoon cricket traditions on the Parade Ground.",
        "start_date": datetime.date(2024, 11, 1),
        "duration_months": 24,
        "end_date": datetime.date(2026, 11, 1),
    },
    {
        "bench_id": "VCP-033",
        "donor_name": "Friends of Tibbetts Brook",
        "email": "brookfriends@example.com",
        "dedication": "Dedicated to the restoration and daylighting of our park's waterways.",
        "start_date": datetime.date(2025, 4, 10),
        "duration_months": 24,
        "end_date": datetime.date(2027, 4, 10),
    },
    {
        "bench_id": "VCP-049",
        "donor_name": "Hudson River Valley Hikers",
        "email": "outreach@hrvhikers.org",
        "dedication": "Along the historic tracks where nature reclaimed its quiet glory.",
        "start_date": datetime.date(2025, 9, 20),
        "duration_months": 24,
        "end_date": datetime.date(2027, 9, 20),
    },
    {
        "bench_id": "VCP-057",
        "donor_name": "Dr. Aris Thorne & Family",
        "email": "thorne.aris@example.com",
        "dedication": "For botanical wonder and woodland serenity in the Northwest Woods.",
        "start_date": datetime.date(2026, 1, 15),
        "duration_months": 24,
        "end_date": datetime.date(2028, 1, 15),
    },

    # ==========================================
    # --- 3 Years Duration (value="36") [4] ---
    # ==========================================
    {
        "bench_id": "VCP-010",
        "donor_name": "Audubon Society of NYC - Bronx Chapter",
        "email": "bronx@nycaudubon.org",
        "dedication": "In honor of John Kieran and all who listen for songbirds in these woods.",
        "start_date": datetime.date(2023, 9, 1),
        "duration_months": 36,
        "end_date": datetime.date(2026, 9, 1),
    },
    {
        "bench_id": "VCP-036",
        "donor_name": "Veterans of Foreign Wars Post 95",
        "email": "commander@vfwpost95.org",
        "dedication": "Never forgotten. To those who served and sacrificed for our freedom.",
        "start_date": datetime.date(2024, 5, 12),
        "duration_months": 36,
        "end_date": datetime.date(2027, 5, 12),
    },
    {
        "bench_id": "VCP-052",
        "donor_name": "Manhattan University Harriers",
        "email": "crosscountry@manhattan.edu",
        "dedication": "Conquer the hills, embrace the challenge, celebrate the finish line.",
        "start_date": datetime.date(2025, 3, 1),
        "duration_months": 36,
        "end_date": datetime.date(2028, 3, 1),
    },
    {
        "bench_id": "VCP-063",
        "donor_name": "Aqueduct Preservation Alliance",
        "email": "contact@aqueductalliance.org",
        "dedication": "Celebrating 180 years of historic engineering and clean water.",
        "start_date": datetime.date(2026, 4, 18),
        "duration_months": 36,
        "end_date": datetime.date(2029, 4, 18),
    },

    # ==========================================
    # --- 4 Years Duration (value="48") [5] ---
    # ==========================================
    {
        "bench_id": "VCP-016",
        "donor_name": "Bronx Council for Environmental Quality",
        "email": "info@bceq.org",
        "dedication": "Dedicated to the protection of our wetlands, ponds, and native flora.",
        "start_date": datetime.date(2023, 1, 10),
        "duration_months": 48,
        "end_date": datetime.date(2027, 1, 10),
    },
    {
        "bench_id": "VCP-041",
        "donor_name": "Arthur & Beverly Sterling",
        "email": "sterlings@example.com",
        "dedication": "America's oldest public golf course — 50 years of teeing off together.",
        "start_date": datetime.date(2024, 6, 20),
        "duration_months": 48,
        "end_date": datetime.date(2028, 6, 20),
    },
    {
        "bench_id": "VCP-060",
        "donor_name": "Riverdale Equestrian Club",
        "email": "equestrian@riverdalestables.com",
        "dedication": "In celebration of horses and riders sharing these historic bridle paths.",
        "start_date": datetime.date(2025, 2, 14),
        "duration_months": 48,
        "end_date": datetime.date(2029, 2, 14),
    },
    {
        "bench_id": "VCP-071",
        "donor_name": "The Goldberg Family",
        "email": "goldberg.family@example.com",
        "dedication": "For Miriam, who found wonder in every wildflower and mossy stone.",
        "start_date": datetime.date(2025, 11, 5),
        "duration_months": 48,
        "end_date": datetime.date(2029, 11, 5),
    },
    {
        "bench_id": "VCP-082",
        "donor_name": "Parents of Community Board 8",
        "email": "parents.cb8@example.com",
        "dedication": "Laughter, playgrounds, and childhood memories made in the sun.",
        "start_date": datetime.date(2026, 5, 1),
        "duration_months": 48,
        "end_date": datetime.date(2030, 5, 1),
    },

    # ==========================================
    # --- 5 Years Duration (value="60") [4] ---
    # ==========================================
    {
        "bench_id": "VCP-019",
        "donor_name": "Woodlawn Civic Association",
        "email": "info@woodlawncivic.org",
        "dedication": "A welcoming path connecting our neighborhood to the heart of nature.",
        "start_date": datetime.date(2022, 7, 4),
        "duration_months": 60,
        "end_date": datetime.date(2027, 7, 4),
    },
    {
        "bench_id": "VCP-047",
        "donor_name": "Bronx River & Park Conservancy",
        "email": "nature@bronxconservancy.org",
        "dedication": "Restoring biodiversity and providing green corridors for all Bronx wildlife.",
        "start_date": datetime.date(2023, 10, 15),
        "duration_months": 60,
        "end_date": datetime.date(2028, 10, 15),
    },
    {
        "bench_id": "VCP-066",
        "donor_name": "The Alvarez Family",
        "email": "carlos.alvarez@example.com",
        "dedication": "Into the woods who can be lonely and sorrowful? In memory of Papa.",
        "start_date": datetime.date(2025, 1, 1),
        "duration_months": 60,
        "end_date": datetime.date(2030, 1, 1),
    },
    {
        "bench_id": "VCP-078",
        "donor_name": "Wakefield & Woodlawn Walkers",
        "email": "walkers@woodlawn.org",
        "dedication": "Every mile walked brings health, gratitude, and good company.",
        "start_date": datetime.date(2026, 3, 20),
        "duration_months": 60,
        "end_date": datetime.date(2031, 3, 20),
    },

    # ==========================================
    # --- 7 Years Duration (value="84") [5] ---
    # ==========================================
    {
        "bench_id": "VCP-027",
        "donor_name": "Van Cortlandt Track Alumni",
        "email": "alumni@vctrack.org",
        "dedication": "Where grit meets glory. Dedicated to every competitor who ran through the tape.",
        "start_date": datetime.date(2020, 4, 1),
        "duration_months": 84,
        "end_date": datetime.date(2027, 4, 1),
    },
    {
        "bench_id": "VCP-054",
        "donor_name": "National Scholastic Athletics Foundation",
        "email": "info@nationalscholastic.org",
        "dedication": "Cross country royalty was forged on this sacred Bronx turf.",
        "start_date": datetime.date(2021, 8, 25),
        "duration_months": 84,
        "end_date": datetime.date(2028, 8, 25),
    },
    {
        "bench_id": "VCP-069",
        "donor_name": "Metropolitan Hiking Club",
        "email": "hike@methiking.org",
        "dedication": "In appreciation of our volunteer trail maintainers who keep our paths clear.",
        "start_date": datetime.date(2023, 6, 10),
        "duration_months": 84,
        "end_date": datetime.date(2030, 6, 10),
    },
    {
        "bench_id": "VCP-085",
        "donor_name": "The Washington Family",
        "email": "washington.jerome@example.com",
        "dedication": "Three generations of summer barbecues and family reunions under the pines.",
        "start_date": datetime.date(2025, 4, 12),
        "duration_months": 84,
        "end_date": datetime.date(2032, 4, 12),
    },
    {
        "bench_id": "VCP-093",
        "donor_name": "Friends of the North Bronx Parks",
        "email": "support@northbronxparks.org",
        "dedication": "For the enduring green lungs of New York City and all future generations.",
        "start_date": datetime.date(2026, 2, 1),
        "duration_months": 84,
        "end_date": datetime.date(2033, 2, 1),
    },

    # ==========================================
    # --- 10 Years Duration (value="120") [4] ---
    # ==========================================
    {
        "bench_id": "VCP-002",
        "donor_name": "Elena & Mateo Rivera",
        "email": "rivera.family@example.com",
        "dedication": "In loving memory of Abuela Sofia, who walked this park every morning.",
        "start_date": datetime.date(2016, 11, 15),
        "duration_months": 120,
        "end_date": datetime.date(2026, 11, 15),
    },
    {
        "bench_id": "VCP-007",
        "donor_name": "Bronx Historical Society",
        "email": "info@bronxhistorical.org",
        "dedication": "Honoring the brave veterans remembered along Memorial Grove.",
        "start_date": datetime.date(2016, 10, 1),
        "duration_months": 120,
        "end_date": datetime.date(2026, 10, 1),
    },
    {
        "bench_id": "VCP-004",
        "donor_name": "Coach Marcus Williams",
        "email": "coach.marcus@example.com",
        "dedication": "Dedicated to all runners who pushed their limits on the Parade Ground.",
        "start_date": datetime.date(2020, 9, 1),
        "duration_months": 120,
        "end_date": datetime.date(2030, 9, 1),
    },
    {
        "bench_id": "VCP-005",
        "donor_name": "David & Sarah Chen",
        "email": "chen.d@example.com",
        "dedication": "Where we shared our first date by the lake. Forever grateful.",
        "start_date": datetime.date(2025, 5, 20),
        "duration_months": 120,
        "end_date": datetime.date(2035, 5, 20),
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
        # Clear out existing adoptions so we have an exact 35% adoption rate
        Adoption.query.delete()
        db.session.commit()

        new_count = 0
        for data in ADOPTIONS:
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

        db.session.commit()
        print(f"Successfully seeded {len(ADOPTIONS)} adoptions ({new_count} added).")

if __name__ == "__main__":
    seed_benches()
    seed_adoptions()
