from sqlalchemy import Column
from sqlalchemy.sql.expression import null, text, true
from sqlalchemy.sql.sqltypes import TIMESTAMP, Integer, Numeric, String
from .database import Base

class User(Base):
    __tablename__ = 'users'
    
    username = Column(String, nullable=False, primary_key=True, unique=True)
    display_name = Column(String, nullable=False)
    email = Column(String, nullable=False, primary_key=True, unique=True)
    mobile_number = Column(Numeric, nullable=False, primary_key=True, unique=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))