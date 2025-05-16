from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, SmallInteger, DECIMAL
from sqlalchemy.sql import func
from app.database.connection import Base

class Dive(Base):
    __tablename__ = "dives"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    StartTime = Column(DateTime, nullable=False)
    Duration = Column(Integer, nullable=False)
    MaxDepth = Column(DECIMAL(8, 2), nullable=False)
    AvgDepth = Column(DECIMAL(8, 2), nullable=True)
    SampleInterval = Column(SmallInteger, nullable=True)
    PreviousMaxDepth = Column(DECIMAL(8, 2), nullable=True)
    DiveTime = Column(Integer, nullable=True)
    DiveNumberInSerie = Column(Integer, nullable=True)

    StartTemperature = Column(DECIMAL(5, 2), nullable=True)
    BottomTemperature = Column(DECIMAL(5, 2), nullable=True)
    EndTemperature = Column(DECIMAL(5, 2), nullable=True)

    SurfaceTime = Column(Integer, nullable=True)
    SurfacePressure = Column(Integer, nullable=True)
    AltitudeMode = Column(SmallInteger, nullable=True)

    Source = Column(Text, nullable=True)
    Mode = Column(SmallInteger, nullable=False, default=3)
    Note = Column(Text, nullable=True)
    PersonalMode = Column(SmallInteger, nullable=True)
    SerialNumber = Column(String, nullable=False, default="")

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
