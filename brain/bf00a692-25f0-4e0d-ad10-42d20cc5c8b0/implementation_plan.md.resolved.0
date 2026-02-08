# Auto-Like: BaoStar Facebook Services Web App

Xây dựng web app React TypeScript tích hợp API BaoStar để cung cấp dịch vụ tăng tương tác Facebook. Giao diện dark theme, hiện đại, premium.

## Proposed Changes

### Project Initialization

#### [NEW] Vite + React + TypeScript Project
- Khởi tạo bằng `npx create-vite@latest ./ --template react-ts`
- Cài thêm: `react-router-dom`, `axios`, `react-hot-toast`, `lucide-react`

---

### Config & Environment

#### [NEW] [.env.example](file:///I:/Website/Auto-like/.env.example)
```
VITE_API_DOMAIN=https://your-domain.com
VITE_API_KEY=your-api-key-here
```

#### [NEW] [.gitignore](file:///I:/Website/Auto-like/.gitignore)
Standard Vite/Node gitignore

---

### API Service Layer

#### [NEW] [api.ts](file:///I:/Website/Auto-like/src/services/api.ts)
- Axios instance với `baseURL` và `api-key` header từ env
- Hàm `buyService(endpoint, body)` - gọi POST mua dịch vụ
- Hàm `getPackages()` - GET `/api/prices` lấy danh sách gói
- Hàm `getOrderLogs(type, ids)` - POST `/api/logs-order`

#### [NEW] [types.ts](file:///I:/Website/Auto-like/src/types/index.ts)
- `Package`, `ServiceCategory`, `OrderResponse`, `OrderLog`, `BuyRequest`

---

### UI Components & Pages

#### [NEW] [App.tsx](file:///I:/Website/Auto-like/src/App.tsx)
- React Router setup với tất cả routes

#### [NEW] [Layout.tsx](file:///I:/Website/Auto-like/src/components/Layout.tsx)
- Dark theme sidebar + header + main content area
- Sidebar chứa menu Facebook services
- Header hiển thị tên app + thông tin

#### [NEW] [ServicePage.tsx](file:///I:/Website/Auto-like/src/components/ServicePage.tsx)
- Component tái sử dụng cho mọi trang dịch vụ Facebook
- Chọn gói → Nhập object_id + quantity → Submit
- Hiển thị kết quả + toast notification

#### [NEW] [Dashboard.tsx](file:///I:/Website/Auto-like/src/pages/Dashboard.tsx)
- Trang tổng quan với thống kê, các dịch vụ nổi bật

#### [NEW] [OrderHistory.tsx](file:///I:/Website/Auto-like/src/pages/OrderHistory.tsx)
- Xem nhật ký đơn hàng từ `/api/logs-order`

#### [NEW] [index.css](file:///I:/Website/Auto-like/src/index.css)
- Dark theme design system: CSS variables, gradients, glassmorphism
- Responsive layout, animations, hover effects

---

### Facebook Service Routes
Tất cả dùng chung `ServicePage` component, khác nhau ở `endpoint` và `packages`:

| Route | Endpoint API |
|-------|-------------|
| `/like-gia-re` | `/api/facebook-like-gia-re/buy` |
| `/like-chat-luong` | `/api/facebook-like-chat-luong/buy` |
| `/like-comment` | `/api/facebook-like-binh-luan/buy` |
| `/comment` | `/api/facebook-binh-luan/buy` |
| `/follow` | `/api/facebook-follow/buy` |
| `/like-page` | `/api/facebook-like-page/buy` |
| `/mem-group` | `/api/facebook-mem-group/buy` |
| `/mat-live` | `/api/facebook-eyes/buy` |
| `/share` | `/api/facebook-share/buy` |
| `/vip` | `/api/facebook-vip-clone/buy` |

---

## Verification Plan

### Automated
```bash
npm run build
```
- Build phải pass không lỗi TypeScript

### Manual (Browser)
1. Chạy `npm run dev`
2. Mở `http://localhost:5173`
3. Kiểm tra: Sidebar hiển thị đủ menu → Click từng item → Form hiển thị đúng
4. Kiểm tra responsive trên mobile viewport
