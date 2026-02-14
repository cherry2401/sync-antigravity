# Walkthrough: Lịch sử đơn hàng — Service Page Tab

## Tổng quan
Thêm tab **"Lịch sử đơn"** bên cạnh tab **"Chọn gói dịch vụ"** trong trang Service Page, cho phép user xem đơn hàng đã mua cho dịch vụ đang xem.

## Các thay đổi

### 1. Backend — Filter orders by service
**File:** [orders.ts](file:///I:/Website/Auto-like/server/routes/orders.ts)

- `GET /api/orders` hỗ trợ query param `?service_id=xxx`
- Khi có `service_id` → chỉ trả đơn hàng của dịch vụ đó
- Không có → trả tất cả (backward compatible)

### 2. Frontend — Tab UI + Order History
**File:** [ServicePage.tsx](file:///I:/Website/Auto-like/src/pages/ServicePage.tsx)

- **State mới:** `activeTab`, `serviceOrders`, `loadingOrders`
- **Tab bar** thay thế label "Chọn gói dịch vụ":
  - 📦 Chọn gói dịch vụ (mặc định)
  - 📋 Lịch sử đơn (chỉ hiện khi đăng nhập, kèm badge số đơn)
- **Order history table** gồm: Mã đơn, Gói, UID, SL, Giá, Trạng thái, Thời gian
- **Status badges:** Đang chạy (vàng), Hoàn thành (xanh), Thất bại (đỏ)
- **Empty state** với icon khi chưa có đơn
- Auto-fetch khi chuyển sang tab history

### 3. CSS
**File:** [index.css](file:///I:/Website/Auto-like/src/index.css)

- `.service-tabs` / `.service-tab` — tab bar với active underline
- `.order-history-table` — compact table với hover, scrollable trên mobile
- `.order-status-badge` — 3 trạng thái: processing/completed/failed
- `.tab-badge` — counter nhỏ trên tab

## Verification
- Frontend (`localhost:5173`) và Backend (`localhost:3001`) đều running OK
- Health check: `{"status":"ok"}`
