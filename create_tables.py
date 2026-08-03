from database import engine, Base

print(engine.url)

from models import *

print(Base.metadata.tables.keys())

print("Creating tables...")

Base.metadata.create_all(bind=engine)

print("All tables created successfully!")