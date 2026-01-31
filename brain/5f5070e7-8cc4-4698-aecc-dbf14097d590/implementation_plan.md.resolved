# Triển khai Dropdown Đường/Phố

## Yêu cầu
Tạo dropdown đường/phố như batdongsan.com.vn - có danh sách sẵn + tìm kiếm.

## Phương án đề xuất

### Phương án A: Overpass API (OpenStreetMap) ⭐ Đề xuất
Lấy danh sách đường từ OpenStreetMap theo bounding box của quận/huyện.

**Ưu điểm:**
- Dữ liệu thực, miễn phí
- Luôn cập nhật

**Nhược điểm:**
- Cần thời gian load (2-5 giây/quận)
- Rate limit: 2 request/giây

---

### Phương án B: Searchable Combobox với nhập tay
Tạo UI tương tự (dropdown + search) nhưng cho phép nhập tự do.

**Ưu điểm:**
- Không phụ thuộc API
- Nhanh, không cần chờ

**Nhược điểm:**
- Không có danh sách gợi ý sẵn

---

## Đề xuất: Kết hợp A + B

1. Tạo component `StreetCombobox` với UI giống batdongsan
2. Load đường từ Overpass API khi chọn quận
3. Nếu API lỗi hoặc không có dữ liệu → cho phép nhập tay
4. Cache kết quả để không load lại

## Verification Plan

### Manual Test
1. Mở http://localhost:3000/dang-tin
2. Click vào ô địa chỉ
3. Chọn Tỉnh → Quận → Phường
4. Kiểm tra dropdown Đường/Phố có hiện danh sách không
5. Thử tìm kiếm tên đường

---

> [!IMPORTANT]
> Anh/chị muốn dùng phương án nào?
> - **A**: Overpass API (có dữ liệu thực, chậm hơn)
> - **B**: Chỉ UI (nhanh, nhập tay)
> - **A+B**: Kết hợp cả hai (có dữ liệu + fallback)
