from .base import Base, Column, String, Enum, UUID, uuid

class Color(Base):
    __tablename__ = 'colors'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    name = Column(Enum('Red', 'Blue', 'Green', 'Yellow', 'Orange', 'Purple', 'Brown', 'Black', 'White', 'Grey'), nullable=False)