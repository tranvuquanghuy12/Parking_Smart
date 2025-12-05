from motor.motor_asyncio import AsyncIOMotorClient
# Chú ý dấu chấm (.) ở trước chữ config
from .config import settings 

# Tạo kết nối
client = AsyncIOMotorClient(settings.MONGO_URI)
db = client[settings.DATABASE_NAME]

# Định nghĩa bảng
user_collection = db.get_collection("users")
slot_collection = db.get_collection("slots")