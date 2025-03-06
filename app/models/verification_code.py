from datetime import datetime, timedelta

from sqlalchemy import Column, Integer, DateTime, Boolean

from app.db.base import Base


class VerificationCode(Base):
    __tablename__ = "verification_codes"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(Integer)
    user_id = Column(Integer)
    is_used = Column(Boolean, default=False)
    attempts = Column(Integer, default=0)
    expires_at = Column(DateTime, default=(datetime.now()+timedelta(minutes=3)))
