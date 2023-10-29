from .base import Base, Column, String, DateTime, ForeignKey, UUID, datetime, uuid

class User(Base):
    __tablename__ = 'users'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    firstname = Column(String(50), nullable=False)
    lastname = Column(String(50), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    color_id = Column(UUID(as_uuid=True), ForeignKey('colors.id'), nullable=False)
    profile_id = Column(UUID(as_uuid=True), ForeignKey('profiles.id'), nullable=False)