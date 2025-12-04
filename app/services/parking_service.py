from app.database import slot_collection, user_collection
from app.schemas.parking_schema import SlotUpdate, ParkingUserCreate
from datetime import datetime
from fastapi.encoders import jsonable_encoder
from fastapi import HTTPException

class ParkingService:
    
    # --- XỬ LÝ SLOT (IoT) ---
    @staticmethod
    async def update_slot(data: SlotUpdate):
        slot_dict = jsonable_encoder(data)
        slot_dict['updated_at'] = datetime.now().strftime("%H:%M:%S %d/%m/%Y")
        
        # Upsert: Có rồi thì update, chưa có thì tạo mới
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
            if "_id" in slot: del slot["_id"]
            slots.append(slot)
        return slots

    # --- XỬ LÝ USER (Admin) ---
    @staticmethod
    async def create_user(user: ParkingUserCreate):
        # Check trùng biển số
        if await user_collection.find_one({"plate_number": user.plate_number}):
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
        new_bal = current_bal + amount if type == "add" else current_bal - amount

        if type == "deduct" and new_bal < 0:
            raise HTTPException(status_code=400, detail="Không đủ tiền thanh toán!")

        await user_collection.update_one(
            {"plate_number": plate_number},
            {"$set": {"balance": new_bal}}
        )
        return {"plate": plate_number, "new_balance": new_bal}