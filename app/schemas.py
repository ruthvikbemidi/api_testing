from pydantic import BaseModel
from pydantic.networks import EmailStr
from datetime import datetime

class User(BaseModel):
    username: str
    display_name: str
    email: EmailStr
    mobile_number: int
    created_at: datetime
    
    class Config:
        orm_mode = True
    
class CreateUserAccount(BaseModel):
    username: str
    display_name: str
    email: EmailStr
    mobile_number: int
    
class UpdateUserAccount(BaseModel):
    display_name: str
    email: EmailStr
    mobile_number: int