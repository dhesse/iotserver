from flask import Flask, request
from sqlalchemy import create_engine, Column, Float, Integer, DateTime, Text, select
from sqlalchemy.orm import declarative_base, Session
import datetime

Base = declarative_base()

class AirQuality(Base):
    __tablename__ = "air_quality"

    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime)
    location = Column(Text)
    temperature = Column(Float)
    humidity = Column(Float)
    pressure = Column(Float)
    resistance = Column(Integer)

    def __repr__(self):
        return f"AirQual(timestap={self.timestamp}, temperature={self.temperature})"

ENGINE = create_engine("sqlite:///airquality.sqlite")
Base.metadata.create_all(ENGINE)
    
app = Flask(__name__)

@app.route("/")
def hello_world():
    print('/ called')
    json = request.get_json()
    with Session(ENGINE) as session:
        airqual = AirQuality(
            timestamp = datetime.datetime.now(),
            location = "living_room",
            temperature = json['temperature'],
            humidity = json['humidity'],
            pressure = json['pressure'],
            resistance = json['resistance']
        )
        session.add(airqual)
        session.commit()
        smt = select(AirQuality)
        for aq in session.scalars(smt):
            print(aq)
    return "<p>OK</p>"
