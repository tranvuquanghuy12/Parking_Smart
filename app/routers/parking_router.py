# app/routers/parking_router.py

from fastapi import APIRouter, Body
# CHÚ Ý: Đảm bảo ParkingUserResponse đã được import từ schemas
from app.schemas.parking_schema import SlotUpdate, SlotResponse, ParkingUserCreate, ParkingUserResponse, TransactionRequest
from app.services.parking_service import ParkingService

# Khởi tạo Router
router = APIRouter(tags=["Parking System"])

# --- API SLOT (IoT) ---

@router.post("/slot/update")
async def update_slot(slot: SlotUpdate):
    """API cho thiết bị IoT gửi trạng thái đỗ xe"""
    return await ParkingService.update_slot(slot)

@router.get("/slots", response_model=list[SlotResponse])
async def get_slots():
    """Lấy danh sách trạng thái chỗ đỗ (Cho Dashboard)"""
    return await ParkingService.get_all_slots()

# --- API USER (Admin) ---

@router.post("/users/create", response_model=ParkingUserResponse)
async def create_user(user: ParkingUserCreate):
    """Tạo khách hàng mới (Kiểm tra trùng biển số)"""
    return await ParkingService.create_user(user)

@router.get("/users", response_model=list[ParkingUserResponse]) # <--- FIX Ở ĐÂY: ÉP Pydantic VALIDATE DỮ LIỆU
async def get_users():
    """Lấy danh sách tất cả khách hàng (Cho Admin Panel)"""
    return await ParkingService.get_all_users()

@router.post("/users/transaction")
async def transaction(req: TransactionRequest, type: str = "add"):
    """Xử lý nạp tiền (add) và thu phí (deduct)"""
    return await ParkingService.process_transaction(req.plate_number, req.amount, type)