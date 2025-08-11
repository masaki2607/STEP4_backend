from sqlalchemy import Column, String
from database import Base

class Employee(Base):
    __tablename__ = "employees"

    emp_id = Column(String(20), primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    password = Column(String(255), nullable=False)