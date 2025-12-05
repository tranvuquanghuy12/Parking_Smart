import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

# Cấu hình cứng để test (loại trừ lỗi do file config)
MONGO_URI = "mongodb://localhost:27017"
DATABASE_NAME = "Parking"

async def test_connection():
    print("⏳ Đang thử kết nối MongoDB...")
    try:
        client = AsyncIOMotorClient(MONGO_URI)
        db = client[DATABASE_NAME]
        
        # Thử chọc vào bảng users
        user_col = db.get_collection("users")
        
        # Thử thêm 1 dòng dữ liệu giả
        print("⏳ Đang thử thêm dữ liệu mẫu...")
        result = await user_col.insert_one({"name": "Test Admin", "role": "Debug"})
        
        print(f"✅ THÀNH CÔNG RỰC RỠ! Đã thêm được ID: {result.inserted_id}")
        print("👉 Giờ anh vào MongoDB Compass, bấm Refresh là thấy bảng users ngay!")
        
    except Exception as e:
        print(f"❌ TOANG RỒI: {e}")

if __name__ == "__main__":
    asyncio.run(test_connection())