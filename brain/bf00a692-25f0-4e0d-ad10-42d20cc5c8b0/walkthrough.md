# Walkthrough: Server Restart

Đã khởi động lại thành công hệ thống Auto-Like.

## Các bước đã thực hiện

1.  **Restart Frontend (Vite):**
    - Chạy `npm run dev` tại thư mục gốc.
    - Frontend hiện đang chạy tại [http://localhost:5173](http://localhost:5173).

2.  **Restart Backend (Express):**
    - Chạy `npx tsx index.ts` tại thư mục `server`.
    - Đã xác minh backend hoạt động bình thường qua health check.
    - Backend hiện đang chạy tại [http://localhost:3001](http://localhost:3001).

## Kết quả kiểm tra (Verification)

### Backend Health Check
```bash
curl.exe -s http://localhost:3001/health
{"status":"ok","time":"2026-02-12T06:42:07.941Z"}
```

Cả hai server đều đã sẵn sàng phục vụ.
