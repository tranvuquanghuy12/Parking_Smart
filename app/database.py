from motor.motor_asyncio import AsyncIOMotorClient
from .config import settings

client = AsyncIOMotorClient(settings.MONGO_URI)
db = client[settings.DATABASE_NAME]

# --- ĐỊNH NGHĨA CÁC COLLECTION ---
# Nơi lưu thông tin khách hàng
user_collection = db.get_collection("users")
# Nơi lưu trạng thái chỗ đỗ xe (IoT gửi lên)
slot_collection = db.get_collection("slots")