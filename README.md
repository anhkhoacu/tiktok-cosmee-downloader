# 🚀 TikTok Fast-Recovery & SEO Metadata Sync Tool

Hệ thống cào và đồng bộ hóa dữ liệu Video tự động từ TikTok dành cho cộng đồng dermo-cosmetics **Cosmee.vn**. Công cụ giúp tự động tải video chất lượng cao (không logo) và trích xuất cấu trúc dữ liệu Marketing (JSON SEO) phục vụ cho việc làm content và tối ưu hóa tìm kiếm.

---

## ⚡ Tính Năng Cốt Lõi

1. **Quản Lý Kênh Tập Trung (`kenh.txt`):** - Tách biệt danh sách nguồn cào ra file cấu hình riêng. Tự động nhận diện, bỏ qua dòng trống hoặc ghi chú.
2. **Logic Tải Ưu Tiên (Mới Nhất Trước):**
   - Tự động đảo ngược thứ tự xử lý, bốc các video vừa mới đăng trên kênh để tải về trước, đảm bảo không bỏ lỡ trend.
3. **Cơ Chế "Fast-Recovery" (Tránh trùng lặp):**
   - **Đối với video cũ đã tải:** Chỉ mất 1 giây để ghi đè/cập nhật dữ liệu tương tác (Views, Likes, Comments, Shares) vào file JSON SEO, bỏ qua việc tải lại file MP4 để tiết kiệm băng thông.
   - **Đối với video mới tinh:** Kích hoạt luồng tải Full HD không đóng dấu (No Watermark).
4. **Hệ Thống Nghỉ Thông Minh (3 Tầng Chống Quét):**
   - Nghỉ 1s - 1.5s khi lướt qua video cũ.
   - Nghỉ ngẫu nhiên 5s - 15s sau khi tải xong video mới (Giả lập hành vi người dùng).
   - Nghỉ ngẫu nhiên 10s - 30s khi chuyển giao giữa các kênh để hạ nhiệt luồng mạng.
5. **Giao Diện Terminal Công Nghệ:**
   - Tích hợp mã màu ANSI trực quan. Thanh trạng thái `Loading Bar` thu gọn thông minh, tự động tối ưu độ dài chuỗi tránh lỗi tràn dòng hay dính chữ trên Console.

---

## 📂 Cấu Trúc Thư Mục Đầu Ra

Mỗi kênh khi quét sẽ tự động tạo một thư mục riêng theo định dạng `Tên-kênh_Cosmee`:
```text
📂 Ngan_aleybeauty_Cosmee/
├── 📄 Khoi-nghi-le-o-nha-uop-matcha-latte-749944-@ngan_aleybeauty.mp4
└── 📄 Khoi-nghi-le-o-nha-uop-matcha-latte-749944-@ngan_aleybeauty.json