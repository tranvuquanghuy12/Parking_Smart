import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # Kết nối localhost mặc định
    MONGO_URI: str = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    # Sửa tên DB thành "Parking" cho khớp với Compass của anh
    DATABASE_NAME: str = os.getenv("DATABASE_NAME", "Parking")

settings = Settings()