@echo off
TITLE He Thong Quan Ly Bai Do Xe IoT
echo --- DANG KHOI DONG HE THONG ---

:: 1. Chạy Backend Server (Cửa sổ 1)
start "Backend Server" cmd /k "venv\Scripts\activate && python -m uvicorn app.main:app --reload"

:: 2. Đợi 5 giây cho Server khởi động xong
timeout /t 5

:: 3. Chạy Bot giả lập (Cửa sổ 2)
start "Fake Device IoT" cmd /k "venv\Scripts\activate && python fake_device.py"

:: 4. Tự động mở trình duyệt (MỚI THÊM)
:: Mở trang Dashboard (Màn hình LED)
start http://127.0.0.1:8000
:: Mở trang Admin
start http://127.0.0.1:8000/admin

echo --- DA CHAY XONG! ---