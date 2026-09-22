# 🌳 Van Cortlandt Park — Bench Adoption System

> **Hey Columbia Software Solutions! 👋**  
> Built with ❤️ for the CSS community and Van Cortlandt Park conservancy.

Welcome to the **Van Cortlandt Park Bench Adoption System** — an interactive, modern web application designed to connect park visitors, families, and benefactors with benches across NYC's third-largest park.

---

## ✨ Features at a Glance

- 🗺️ **Interactive Geospatial Map**: Powered by MapLibre GL & Positron vector tiles, featuring real GPS coordinates across historic grounds, lakesides, woodlands, and running trails.
- 🟡🟢🔵 **Multi-Tier Status Visuals**:
  - **Available** (Green) — Ready to adopt with customizable dedication plaque and 6-month to 10-year terms.
  - **Adopted** (Gold / Amber) — View who adopted each bench, when, and for how long.
  - **Ending Soon** (Vivid Blue) — Distinct pulsing blue pins highlighting adoptions expiring within 6 months.
- 📊 **Adoption Tenure Card & Live Progress Bar**:
  - Displays total tenure (e.g. *10-Year Adoption*), formatted start and end dates.
  - Dynamic elapsed tenure (*"9 yrs, 10 mo"*) and human countdown (*"~2 months left"*).
  - Elegant visual timeline progress bar showing percent of dedication completed.
- 🧭 **"Find a Bench for Me" Recommendation Wizard**:
  - Guided questionnaire matching desired atmosphere (*Quiet & Peaceful*, *Active & Lively*, *Scenic Overlooks*), landscape environments, and amenities (lake, trail, recreational facility).
  - Scored using an efficient min-heap algorithm (`heapq.nlargest`) and presented in a docked interactive sidebar.
- 🔎 **Donor & Family Search**:
  - Instant lookup by donor or family name with camera fly-to animation and automated bounds fitting.
- 🔄 **Self-Healing Database & Lifecycle Engine**:
  - Automatically identifies expired adoptions and releases benches back to park inventory.
  - Auto-inspects database schema on startup to seamlessly handle migrations between local SQLite and cloud PostgreSQL (Render).

---

## 🚀 Quickstart

### 1. Clone & Set Up Environment
```bash
git clone https://github.com/Pvpres/CSS_VanCortlandPark_BenchAdoption.git
cd CSS_VanCortlandPark_BenchAdoption

# Create & activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Launch the Application
```bash
python3 app.py
```
Visit **[http://localhost:5000](http://localhost:5000)** in your browser!

### 3. Database Seeding & Reset
The database auto-seeds 100 benches and sample adoptions on first boot. You can also reseed or reset anytime via the browser:
```text
http://localhost:5000/admin/seed?reset=1
```

---

## 🛠️ Tech Stack

- **Backend**: Python 3, Flask, Flask-SQLAlchemy, SQLite (Dev) / PostgreSQL (Prod)
- **Frontend**: Vanilla JS (ES6+), MapLibre GL JS, CSS3 Modern Flexbox/Grid
- **Deployment**: Gunicorn, Render-ready with environment auto-detection

---

### 💬 Shoutout to Columbia Software Solutions
Huge thanks to **Columbia Software Solutions (CSS)** for this awesome project prompt! 💙🦁
