from pydantic import BaseModel, Field
from typing import Optional

# --- Schema cho Chỗ Đỗ Xe (IoT) ---
class SlotUpdate(BaseModel):
    slot_id: str
    is_occupied: bool

class SlotResponse(BaseModel):
    slot_id: str
    is_occupied: bool
    updated_at: str

# --- Schema cho Giao Dịch (Admin) ---
class TransactionRequest(BaseModel):
    plate_number: str
    amount: int
    
# --- Schema cho User (Kế thừa từ User mẫu hoặc tạo mới) ---
class ParkingUserCreate(BaseModel):
    fullname: str
    plate_number: str
    balance: int = 0

class ParkingUserResponse(ParkingUserCreate):
    id: str