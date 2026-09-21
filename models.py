from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

#Bench Table represents the physical benches available at the park
class Bench(db.Model):
    id = db.Column(db.String, primary_key=True)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    location = db.Column(db.String)
    #maybe add description feature

#Adoption table in DB represents the actually ownership  
class Adoption(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    #ties each adoption to a specific bench via the unique bench id as a foreign key 
    bench_id = db.Column(
        db.String,
        db.ForeignKey("bench.id"),
        nullable=False
    )
    donor_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    dedication = db.Column(db.String)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    

    
    
    