from app.database import slot_collection, user_collection
from app.schemas.parking_schema import SlotUpdate, ParkingUserCreate
from datetime import datetime
from fastapi.encoders import jsonable_encoder
from fastapi import HTTPException
from math import ceil # Cần thư viện math để làm tròn lên

class ParkingService:
    # --- PHẦN 1: XỬ LÝ SLOT ---
    @staticmethod
    async def update_slot(data: SlotUpdate):
        slot_dict = jsonable_encoder(data)
        slot_dict['updated_at'] = datetime.now().strftime("%H:%M:%S %d/%m/%Y")
        await slot_collection.update_one(
            {"slot_id": data.slot_id},
            {"$set": slot_dict},
            upsert=True
        )
        return slot_dict

    @staticmethod
    async def get_all_slots():
        slots = []
        async for slot in slot_collection.find():
            if "_id" in slot: 
                slot["id"] = str(slot["_id"])
                del slot["_id"]
            slots.append(slot)
        return slots

    # --- PHẦN 2: XỬ LÝ USER & TIỀN (KHẮC PHỤC LỖI CRASH 500) ---
    @staticmethod
    async def get_all_users():
        users = []
        # Hàm này đã được fix để xử lý các document thiếu trường (như "Test Admin")
        async for u in user_collection.find():
            # CHUYỂN ĐỔI BẢO ĐẢM
            u["id"] = str(u["_id"])
            del u["_id"]
            
            # Xử lý các trường có thể bị thiếu (nếu chưa xóa sạch data rác)
            user_safe = {
                "id": u["id"],
                "fullname": u.get("fullname", "--- Thiếu Tên ---"),
                "plate_number": u.get("plate_number", "--- Thiếu Biển ---"),
                "balance": u.get("balance", 0)
            }
            users.append(user_safe)
        return users

    @staticmethod
    async def create_user(user: ParkingUserCreate):
        existing = await user_collection.find_one({"plate_number": user.plate_number})
        if existing:
            raise HTTPException(status_code=400, detail="Biển số xe đã tồn tại!")
        
        user_dict = jsonable_encoder(user)
        new_user = await user_collection.insert_one(user_dict)
        user_dict["id"] = str(new_user.inserted_id)
        return user_dict 

    @staticmethod
    async def process_transaction(plate_number: str, amount: int, type: str):
        user = await user_collection.find_one({"plate_number": plate_number})
        if not user:
            raise HTTPException(status_code=404, detail="Không tìm thấy xe!")

        current_bal = user.get("balance", 0)
        
        # if type == "add":
        #     new_bal = current_bal + amount
        # elif type == "deduct":
        #     if current_bal < amount:
        #         raise HTTPException(status_code=400, detail="Không đủ tiền!")
        #     new_bal = current_bal - amount

        if type == "add":
            # Nếu là nạp tiền, dùng amount mà Frontend gửi lên
            fee_charged = amount 
            new_bal = current_bal + amount
            days = 0 # Không tính ngày
        
        elif type == "deduct":
            # Nếu là thu phí, tính tiền dựa trên duration_hours và loại xe
            days = ceil(duration_hours / 24.0)
            vehicle_type = user.get("vehicle_type", "CAR")
            rate = FEE_RATES.get(vehicle_type, FEE_RATES["CAR"])
            
            amount_to_deduct = int(days * rate)
            fee_charged = amount_to_deduct

            if current_bal < amount_to_deduct:
                raise HTTPException(status_code=400, detail=f"Số dư {current_bal} VNĐ không đủ để trả phí {amount_to_deduct} VNĐ!")
            
            new_bal = current_bal - amount_to_deduct

        # --- BƯỚC 2: CẬP NHẬT DB VÀ TRẢ VỀ ---
        await user_collection.update_one(
            {"plate_number": plate_number},
            {"$set": {"balance": new_bal}}
        )
        return {"plate": plate_number, "new_balance": new_bal}
 