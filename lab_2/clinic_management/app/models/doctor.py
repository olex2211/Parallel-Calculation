from datetime import datetime
from decimal import Decimal
from typing import Optional


class Doctor:
    def __init__(
        self,
        first_name: str,
        last_name: str,
        specialization: str,
        hourly_rate: Decimal,
        phone: str,
        email: str,
        id: Optional[int] = None,
        created_at: Optional[datetime] = None,
    ):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.specialization = specialization
        self.hourly_rate = hourly_rate
        self.phone = phone
        self.email = email
        self.created_at = created_at
