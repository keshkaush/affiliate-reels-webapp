from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Boolean, ForeignKey, Float
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Content(Base):
    __tablename__ = 'content'

    id = Column(Integer, primary_key=True)
    platform = Column(String(50), nullable=False)
    video_url = Column(String(500), nullable=False, unique=True)
    title = Column(String(255))
    description = Column(Text)
    author = Column(String(100))
    views = Column(Integer, default=0)
    likes = Column(Integer, default=0)
    shares = Column(Integer, default=0)
    comments = Column(Integer, default=0)
    timestamp = Column(DateTime, default=datetime.now)
    niche = Column(String(100))
    keywords_matched = Column(Text) # Storing as comma-separated string for simplicity
    is_faceless = Column(Boolean, default=False)
    products_found = Column(Text) # Storing as comma-separated string
    status = Column(String(50), default='new') # e.g., 'new', 'processed', 'flagged_for_affiliate'

    affiliate_links = relationship('ProductAffiliateLink', back_populates='content', cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Content(id={self.id}, title='{self.title[:30]}', platform='{self.platform}')>"

class AffiliateProgram(Base):
    __tablename__ = 'affiliate_programs'

    id = Column(Integer, primary_key=True)
    network = Column(String(100), nullable=False, unique=True)
    name = Column(String(255))
    commission_rate = Column(String(50)) # e.g., "5%", "Up to 10%"
    cookie_duration = Column(Integer) # days
    priority_score = Column(Float)

    affiliate_links = relationship('ProductAffiliateLink', back_populates='affiliate_program')

    def __repr__(self):
        return f"<AffiliateProgram(network='{self.network}', name='{self.name}')>"

class ProductAffiliateLink(Base):
    __tablename__ = 'product_affiliate_links'

    id = Column(Integer, primary_key=True)
    product_name = Column(String(255), nullable=False)
    affiliate_link = Column(String(500), nullable=False, unique=True)
    content_id = Column(Integer, ForeignKey('content.id'), nullable=True) # Optional, link to specific content
    affiliate_program_id = Column(Integer, ForeignKey('affiliate_programs.id'), nullable=False)
    added_by_user = Column(Boolean, default=True) # True if manually added by user, False if auto-discovered
    created_at = Column(DateTime, default=datetime.now)

    content = relationship('Content', back_populates='affiliate_links')
    affiliate_program = relationship('AffiliateProgram', back_populates='affiliate_links')

    def __repr__(self):
        return f"<ProductAffiliateLink(product='{self.product_name}', link='{self.affiliate_link[:50]}')>"

def init_db(database_url):
    engine = create_engine(database_url)
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)
