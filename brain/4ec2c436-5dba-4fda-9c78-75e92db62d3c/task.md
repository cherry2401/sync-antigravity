# Auto CDP Connector Implementation

## Hướng 1: Auto CDP Port Scanner (MŨI NHỌN)
- [x] Thêm CDP port scanner vào `browserRelay.ts` - quét port 9222
- [x] Tự động kết nối CDP endpoint khi phát hiện Chrome debugging port
- [x] Ưu tiên tab đang active (page type, non-chrome URLs)
- [x] Cập nhật StatusBar indicator (CDP Direct, tooltip)
- [x] Extreme HMR Fix & Stability 🚁
    - [x] Migrate communication files to system `AppData` (userData)
    - [x] Expose `getCommDir` API in Electron Main/Preload
    - [x] Refactor `BrowserRelay` to use AppData paths for CDP
    - [x] Update `App.tsx`, `ChatPanel.tsx`, `ChopperLogs.tsx` to use dynamic paths
    - [x] Fix chat session/watcher race condition
    - [x] Cleanup: Delete local `data/` folder and update `CHOPPER_GUIDE.md`
- [x] ⚠️ **Blocked by Windows Security** - Port 9222 không bind được

## Hướng 2: Extension Auto-Attach (TRIỂN KHAI) ✅
- [x] Thêm `chrome.tabs.onUpdated` listener vào `background.js`
- [x] Tự động attach khi tab load xong (`status === 'complete'`)
- [x] Badge luôn hiện ON tự động
- [x] Sửa lỗi HTTP 404 preflight block Extension kết nối
- [x] Cập nhật StatusBar sang màu xanh 🟢 khi Extension connect
- [x] Tinh chỉnh UI: Đồng bộ icon Circle, màu sắc và xóa emoji dư thừa (Balanced UI)
- [x] Tạo hướng dẫn cài Extension (SETUP_GUIDE.md)
- [x] Sửa lỗi HMR loop & Nâng cấp Watcher lên cấp Global ✅
- [x] Tạo hướng dẫn vận hành cho Chopper (CHOPPER_GUIDE.md)
- [x] Kiểm tra thực tế: Hệ thống đã chạy im lặng và ổn định! 🟢

## Tài liệu
- [x] Hướng dẫn cài Extension Auto-Attach
