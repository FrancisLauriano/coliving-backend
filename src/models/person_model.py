# models/person_model.py:
from config.database import db
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid


class Person(db.Model):
    __tablename__ = "persons"

    id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        server_default=db.text("gen_random_uuid()")
    )
    name = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    person_type = db.Column(db.String(50), nullable=False)
    registration_date = db.Column(db.Date, server_default=func.now())
    password = db.Column(db.String(255), nullable=False)

    def to_dict(self):
        return {
            "id": str(self.id),
            "name": self.name,
            "phone": self.phone,
            "email": self.email,
            "person_type": self.person_type,
            "registration_date": self.registration_date.isoformat() if self.registration_date else None,
        }
