from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.routers import parking_router

app = FastAPI(title="Hệ Thống Bãi Đỗ Xe IoT")

# 1. Mount thư mục giao diện (Quan trọng: Folder static phải có index.html và admin.html)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# 2. Gắn Router Logic (API)
app.include_router(parking_router.router)

# 3. Vào trang chủ -> Hiện bảng LED
@app.get("/")
async def root():
    return FileResponse('app/static/index.html')

# 4. Vào trang admin -> Hiện quản lý
@app.get("/admin")
async def admin():
    return FileResponse('app/static/admin.html')