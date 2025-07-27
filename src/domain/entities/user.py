from datetime import datetime
from typing import Optional
import uuid

class User:
    id: Optional[str] = None
    
    def __init__(
            self, 
            user_id: Optional[str] = None, 
            name: str = "", 
            email: str = "",
            created_at: Optional[datetime] = None,
            updated_at: Optional[datetime] = None
            ):
        self.user_id = user_id or str(uuid.uuid4())
        self.name = name
        self.email = email
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()

    def is_valid_email(self) -> bool:
        return "@" in self.email and "." in self.email.split("@")[1]

    def __repr__(self):
        return f"User(user_id={self.user_id}, name={self.name}, email={self.email})"