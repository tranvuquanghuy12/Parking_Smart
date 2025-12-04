import requests
import time
import random
import sys

# Địa chỉ Server của anh (đang chạy localhost)
SERVER_URL = "http://127.0.0.1:8000/slot/update"

# Danh sách các chỗ đỗ xe trong bãi giả định
SLOTS = ["A1", "A2", "B1", "B2", "C1", "C2"]

print("--- ĐANG KHỞI ĐỘNG THIẾT BỊ IOT GIẢ LẬP ---")
print(f"Sẽ gửi dữ liệu đến: {SERVER_URL}")
print("Nhấn Ctrl+C để dừng lại\n")

try:
    while True:
        # 1. Chọn bừa 1 chỗ đỗ
        target_slot = random.choice(SLOTS)
        
        # 2. Random trạng thái (True = Có xe, False = Trống)
        status = random.choice([True, False])
        
        # 3. Tạo gói tin (Payload) y hệt con ESP32 gửi
        payload = {
            "slot_id": target_slot,
            "is_occupied": status
        }
        
        # 4. Gửi đi!
        try:
            response = requests.post(SERVER_URL, json=payload)
            
            if response.status_code == 200:
                trang_thai = "🔴 CÓ XE" if status else "🟢 TRỐNG"
                print(f"[Gửi OK] Slot {target_slot} -> {trang_thai}")
            else:
                print(f"[Lỗi Server] Code: {response.status_code}")
                
        except requests.exceptions.ConnectionError:
            print("⚠️ Lỗi: Không kết nối được Server! (Anh đã bật backend chưa?)")

        # 5. Nghỉ 2 giây rồi gửi tiếp (mô phỏng cảm biến quét liên tục)
        time.sleep(2)

except KeyboardInterrupt:
    print("\nĐã tắt thiết bị giả lập.")
    sys.exit(0)