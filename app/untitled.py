from app.config import settings

print(f"API Key exists: {'Yes' if settings.GROQ_API_KEY else 'No'}")
print(f"MongoDB URI: {settings.MONGODB_URI}")
print(f"Database: {settings.DATABASE_NAME}")