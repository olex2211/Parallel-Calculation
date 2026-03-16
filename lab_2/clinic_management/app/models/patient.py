from datetime import date, datetime
from typing import Optional


class Patient:
    def __init__(
        self,
        first_name: str,
        last_name: str,
        date_of_birth: date,
        phone: str,
        email: str,
        id: Optional[int] = None,
        created_at: Optional[datetime] = None,
    ):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.date_of_birth = date_of_birth
        self.phone = phone
        self.email = email
        self.created_at = created_at
