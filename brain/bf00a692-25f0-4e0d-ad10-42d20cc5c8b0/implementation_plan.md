# Admin Deposit History Implementation Plan

## Goal
Add a dedicated "Deposit History" (Lịch sử nạp) tab to the Admin Panel to view all user deposit transactions.

## Proposed Changes

### Backend
#### [MODIFY] [admin.ts](file:///I:/Website/Auto-like/server/routes/admin.ts)
- Add `GET /admin/deposit-history` endpoint.
- Query `transactions` table filtering by `type = 'deposit'`.
- Join with `users` table to get username (or rely on `user_id` if username is not needed, but screenshot shows "Mã đơn" which might be transaction ID, and maybe user info is implicit or needed). Screenshot shows "Diễn tả" (Description) which often contains "Hệ thống ACB nạp...".
- Return fields: `id`, `created_at`, `amount`, `balance_after`, `description` (and maybe `user_id`/`username`).

### Frontend
#### [MODIFY] [AdminPage.tsx](file:///I:/Website/Auto-like/src/pages/AdminPage.tsx)
- Add new tab `deposits` ("Lịch sử nạp") to `tabs` array.
- Create `DepositHistory` component or render logic within `AdminPage`.
- Fetch data from `/admin/deposit-history` when tab is active.
- Render table with columns: `#` (ID), `Mã đơn` (maybe transaction ID), `Ngày tạo`, `Hành động` (defaults to "Nạp ngân hàng ..."), `Số tiền` (Amount + Balance calculation), `Diễn tả`.

## Verification Plan
1. Open Admin Panel.
2. Click "Lịch sử nạp" tab.
3. Verify table displays deposit transactions.
4. Compare with screenshot (layout and data columns).
