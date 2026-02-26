# Split AdminPage.tsx into Sub-Components

## Mục tiêu
Tách `AdminPage.tsx` (908 dòng, 26 functions, 5 tabs) thành các component nhỏ, dễ bảo trì. Đảm bảo không mất chức năng, không lỗi TypeScript.

## Chiến lược: "Lift State Up"

`AdminPage.tsx` giữ vai trò **Tab Router** — chỉ quản lý tab navigation và shared state (`stats`). Mỗi tab trở thành 1 component riêng, tự quản lý state và data loading.

---

## Proposed Changes

### Shared Types

#### [NEW] [admin.ts](file:///I:/Website/Auto-like/src/types/admin.ts)
- Chứa tất cả 7 interfaces: `Stats`, `ChartPoint`, `AdminUser`, `Order`, `DepositLog`, `PricingPackage`, `PricingService`
- Type alias `Tab`
- Tất cả sub-components import từ đây

---

### Sub-Components

#### [NEW] [AdminDashboard.tsx](file:///I:/Website/Auto-like/src/pages/admin/AdminDashboard.tsx)
- **State sở hữu:** `stats`, `chartData`, `chartRange`
- **Functions:** `loadStats`, `loadChart`
- **JSX:** Lines 335-407 (stat cards + chart)
- **Props:** không cần (tự gọi API)

#### [NEW] [AdminUsers.tsx](file:///I:/Website/Auto-like/src/pages/admin/AdminUsers.tsx)
- **State sở hữu:** `users`, `userSearch`, `depositModal`, `depositAmount`, `deleteConfirm`
- **Functions:** `loadUsers`, `handleDeposit`, `handleDeleteUser`, `toggleUserActive`, `exportCsv('users')`
- **JSX:** Lines 410-499 + Modals 852-904
- **Props:** `onDataChange?: () => void` (để AdminDashboard biết refresh stats nếu cần — **optional, sẽ tự load lại khi chuyển tab**)

#### [NEW] [AdminOrders.tsx](file:///I:/Website/Auto-like/src/pages/admin/AdminOrders.tsx)
- **State sở hữu:** `orders`, `orderFilters`, `showOrderFilters`
- **Functions:** `loadOrders`, `exportCsv('orders')`
- **JSX:** Lines 788-849
- **Props:** không cần

#### [NEW] [AdminPricing.tsx](file:///I:/Website/Auto-like/src/pages/admin/AdminPricing.tsx)
- **State sở hữu:** `pricingDetail`, `expandedServices`, `pricingPlatform`, `pricingMode`
- **Functions:** `loadPricingDetail`, `updateMarkup`, `updatePackageMarkup`, `togglePackage`, `toggleExpand`, `markupToPercent`, `percentToMarkup`, `formatMarkup`
- **JSX:** Lines 563-785
- **Props:** không cần

#### [NEW] [AdminDeposits.tsx](file:///I:/Website/Auto-like/src/pages/admin/AdminDeposits.tsx)
- **State sở hữu:** `deposits`, `depositFilters`, `showDepositFilters`
- **Functions:** `loadDeposits`, `exportCsv('transactions')`
- **JSX:** Lines 502-560
- **Props:** không cần

---

### Parent Component

#### [MODIFY] [AdminPage.tsx](file:///I:/Website/Auto-like/src/pages/AdminPage.tsx)
- **Giảm từ ~908 → ~60 dòng**
- Chỉ còn: tab navigation + lazy render component theo tab
- Import 5 sub-components
- Giữ nguyên: `isAdmin` check, `navigate('/')`, tab state

---

## Sơ đồ dependency

```
AdminPage.tsx (tab router, ~60 lines)
├── AdminDashboard  (tự load /admin/stats, /admin/stats/chart)
├── AdminUsers      (tự load /admin/users, modals nạp/trừ/xóa)
├── AdminOrders     (tự load /admin/orders)
├── AdminPricing    (tự load /admin/pricing-detail)
└── AdminDeposits   (tự load /admin/deposit-history)

types/admin.ts (shared interfaces)
```

## Rủi ro & Cách phòng tránh

| Rủi ro | Phòng tránh |
|--------|------------|
| Thiếu props, thiếu import | TypeScript sẽ báo lỗi compile ngay lập tức |
| Mất modal (nạp/trừ/xóa user) | Chuyển vào AdminUsers — giữ nguyên logic 100% |
| `exportCsv` trùng code | Duplicate nhỏ (~10 dòng) vào mỗi component cần — chấp nhận được |
| Stats không refresh khi nạp tiền | Mỗi component tự load data khi mount → chuyển tab stats = auto refresh |

## Verification Plan
1. `npm run dev` frontend — kiểm tra 0 TypeScript errors
2. Mở browser, kiểm tra từng tab: Stats, Users, Deposits, Pricing, Orders
3. Test hành động: nạp tiền, khóa user, đổi markup → xác nhận data đúng
