import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, ForeignKey, JSON, Text
from sqlalchemy.orm import relationship
from app.core.database import Base

class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(255), default="Tax Consultation")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    user = relationship("User", back_populates="conversations")
    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan", order_by="Message.created_at")

class Message(Base):
    __tablename__ = "messages"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    conversation_id = Column(String(36), ForeignKey("conversations.id", ondelete="CASCADE"), nullable=False, index=True)
    
    sender = Column(String(20), nullable=False)  # "USER", "COPILOT", "SYSTEM"
    content = Column(Text, nullable=False)
    cited_rules = Column(JSON, default=list)     # [{"rule_code": "IN-SEC37-SOFT-01", "source": "Sec 37(1)", "title": "..."}]
    
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationship
    conversation = relationship("Conversation", back_populates="messages")
