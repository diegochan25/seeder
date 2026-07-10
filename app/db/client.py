from datetime import timezone
from pymongo import MongoClient
from app.config.settings import settings


client = MongoClient(settings.mongodb_uri, tz_aware=True, tzinfo=timezone.utc)