from sqlalchemy import Column, Integer, DECIMAL, ForeignKey, DateTime
from sqlalchemy.sql import func
from app.database.connection import Base

class DiveSample(Base):
    __tablename__ = "dive_samples"

    id = Column(Integer, primary_key=True, index=True)
    dive_id = Column(Integer, ForeignKey("dives.id", ondelete="CASCADE"), nullable=False)

    time = Column(Integer, nullable=False)  # seconds
    depth = Column(DECIMAL(8, 2), nullable=True)  # meters
    temperature = Column(DECIMAL(5, 2), nullable=True)  # °C

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
