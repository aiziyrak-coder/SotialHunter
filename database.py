"""
SOCIAL HUNTER - Database Models and Connection
"""
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import config

Base = declarative_base()

class ActivePost(Base):
    """Kuzatilayotgan postlar"""
    __tablename__ = "active_posts"
    
    id = Column(Integer, primary_key=True)
    media_id = Column(String, unique=True, nullable=False)
    post_url = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)

class Lead(Base):
    """Topilgan lidlar"""
    __tablename__ = "leads"
    
    id = Column(Integer, primary_key=True)
    instagram_username = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    conversation_summary = Column(Text)
    media_id = Column(String)  # Qaysi postdan kelgan
    created_at = Column(DateTime, default=datetime.utcnow)
    notified = Column(Boolean, default=False)

class Conversation(Base):
    """Suhbatlar tarixi"""
    __tablename__ = "conversations"
    
    id = Column(Integer, primary_key=True)
    instagram_user_id = Column(String, nullable=False)
    instagram_username = Column(String)
    message_text = Column(Text, nullable=False)
    is_from_user = Column(Boolean, default=True)  # True = foydalanuvchidan, False = botdan
    created_at = Column(DateTime, default=datetime.utcnow)
    media_id = Column(String)

class AISettings(Base):
    """AI sozlamalari"""
    __tablename__ = "ai_settings"
    
    id = Column(Integer, primary_key=True)
    system_prompt = Column(Text, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# Database connection
engine = create_engine(config.DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """Ma'lumotlar bazasini yaratish"""
    Base.metadata.create_all(bind=engine)
    
    # AI sozlamalarini boshlang'ich qiymat bilan yaratish
    db = SessionLocal()
    try:
        if not db.query(AISettings).first():
            ai_settings = AISettings(system_prompt=config.AI_SYSTEM_PROMPT)
            db.add(ai_settings)
            db.commit()
    finally:
        db.close()

def get_db():
    """Database session yaratish"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
