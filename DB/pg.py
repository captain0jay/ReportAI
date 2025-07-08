from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, func
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
load_dotenv()
# Define DB connection
engine = create_engine(os.environ.get('PG_DB_URL'))
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

# Model Definition
class MyTable(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, autoincrement=True)
    slug = Column(String(255), nullable=False, unique=True)
    text = Column(Text, nullable=False)
    date_created = Column(DateTime(timezone=True), server_default=func.now())
    date_updated = Column(DateTime(timezone=True), onupdate=func.now())

# DB Manager
class DBManager:
    def __init__(self):
        self.session = SessionLocal()

    async def add_entry(self, slug, text):
        entry = MyTable(slug=slug, text=text)
        self.session.add(entry)
        self.session.commit()
        return entry.id

    async def fetch_by_slug(self, slug):
        return self.session.query(MyTable).filter(MyTable.slug == slug).first()

