from fastapi import APIRouter, Body
from app.schemas.parking_schema import SlotUpdate, SlotResponse, ParkingUserCreate, ParkingUserResponse, TransactionRequest
from app.services.parking_service import ParkingService

router = APIRouter(tags=["Parking System"])

# API cập nhật chỗ đỗ (Cho ESP32)
@router.post("/slot/update")
async def update_slot(slot: SlotUpdate):
    return await ParkingService.update_slot(slot)

# API lấy danh sách chỗ (Cho Dashboard)
@router.get("/slots", response_model=list[SlotResponse])
async def get_slots():
    return await ParkingService.get_all_slots()

# API tạo khách hàng
@router.post("/users/create", response_model=ParkingUserResponse)
async def create_user(user: ParkingUserCreate):
    return await ParkingService.create_user(user)

# API danh sách khách hàng
@router.get("/users")
async def get_users():
    # Logic lấy user đơn giản nên viết thẳng ở đây cũng đc, hoặc chuyển qua Service
    from app.database import user_collection
    users = []
    async for u in user_collection.find():
        u["id"] = str(u["_id"])
        users.append(u)
    return users

# API giao dịch tiền
@router.post("/users/transaction")
async def transaction(req: TransactionRequest, type: str = "add"):
    return await ParkingService.process_transaction(req.plate_number, req.amount, type)