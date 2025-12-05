from pydantic import BaseModel, Field
from typing import Optional, Literal # <--- ĐÃ THÊM Literal

# Định nghĩa các loại xe (Chỉ chấp nhận 2 giá trị này)
VehicleType = Literal['CAR', 'MOTORBIKE'] # <--- MỚI

# --- Schema cho Chỗ Đỗ Xe (IoT) ---
class SlotUpdate(BaseModel):
    slot_id: str
    is_occupied: bool

class SlotResponse(BaseModel):
    slot_id: str
    is_occupied: bool
    updated_at: str

# --- Schema cho Giao Dịch (Admin) ---
# app/schemas/parking_schema.py
class TransactionRequest(BaseModel):
    plate_number: str
    duration_hours: float = 0 # Dùng cho việc thu phí
    amount: int = 0          # Dùng cho việc nạp tiền

# --- Schema cho User (Kế thừa từ User mẫu hoặc tạo mới) ---
class ParkingUserCreate(BaseModel):
    fullname: str
    plate_number: str
    balance: int = 0
    # Thêm loại xe (BẮT BUỘC)
    vehicle_type: VehicleType = 'CAR' # <--- ĐÃ THÊM

class ParkingUserResponse(ParkingUserCreate):
    id: str