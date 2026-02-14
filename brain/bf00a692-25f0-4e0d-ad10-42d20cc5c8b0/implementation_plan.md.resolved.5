# Thêm Tab "Lịch sử đơn hàng" trong Service Page

Thêm tab "Lịch sử đơn hàng" bên cạnh tab "Chọn gói dịch vụ" trong trang đặt dịch vụ. Tab này hiển thị các đơn hàng đã mua cho dịch vụ hiện tại.

## Proposed Changes

### Backend — Filter orders by service

#### [MODIFY] [orders.ts](file:///I:/Website/Auto-like/server/routes/orders.ts)

Thêm query param `service_id` vào `GET /api/orders`:

```diff
- FROM orders WHERE user_id = ?
+ FROM orders WHERE user_id = ? AND (? IS NULL OR service_id = ?)
```

Khi gọi `/api/orders?service_id=like-bai-viet` → chỉ trả về đơn hàng của dịch vụ đó.

---

### Frontend — Tab UI + Order History Table

#### [MODIFY] [ServicePage.tsx](file:///I:/Website/Auto-like/src/pages/ServicePage.tsx)

1. **Thêm state:**
   - `activeTab: 'packages' | 'history'`
   - `serviceOrders: Order[]`
   - `loadingOrders: boolean`

2. **Thêm tab bar** thay thế label "Chọn gói dịch vụ":
   ```
   ┌─────────────────┬──────────────────┐
   │ 📦 Chọn gói DV  │ 📋 Lịch sử đơn  │
   └─────────────────┴──────────────────┘
   ```

3. **Tab "Lịch sử đơn"** hiển thị bảng:
   - Cột: Mã đơn | Gói | UID | Số lượng | Giá | Trạng thái | Thời gian
   - Status badges: `processing` (vàng), `completed` (xanh), `failed` (đỏ)
   - Empty state nếu chưa có đơn
   - Chỉ hiển thị khi đã đăng nhập

4. **Fetch orders** khi chuyển sang tab history hoặc khi mua thành công

---

### CSS — Tab & Table Styles

#### [MODIFY] [index.css](file:///I:/Website/Auto-like/src/index.css)

- `.service-tabs` — flexbox tab bar với border-bottom
- `.service-tab` — tab button với active state underline
- `.order-history-table` — compact table phù hợp với form card
- `.order-status-badge` — badge cho processing/completed/failed
- Mobile responsive cho table (horizontal scroll)

## Verification Plan

### Manual
- Chuyển qua lại giữa 2 tab
- Mua đơn hàng → chuyển sang tab history → thấy đơn mới
- Khi chưa đăng nhập → tab history ẩn hoặc hiện thông báo
- Kiểm tra mobile responsive
