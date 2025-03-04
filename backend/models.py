from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from backend.database import Base

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String)

    allocations = relationship("Allocation", back_populates="project")

class Allocation(Base):
    __tablename__ = "allocations"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    amount = Column(Float)

    project = relationship("Project", back_populates="allocations")
    vesting_schedules = relationship("VestingSchedule", back_populates="allocation")

class VestingSchedule(Base):
    __tablename__ = "vesting_schedules"

    id = Column(Integer, primary_key=True, index=True)
    allocation_id = Column(Integer, ForeignKey("allocations.id"))
    unlock_date = Column(String)
    amount = Column(Float)

    allocation = relationship("Allocation", back_populates="vesting_schedules")
