# 🔐 Hệ thống Đăng ký / Đăng nhập & Quản lý Số dư — Auto-Like

## Executive Summary

Web Auto-Like hiện tại là **Vite + React frontend thuần**, gọi trực tiếp BaoStar API thông qua Vite proxy. **API key nằm lộ trong frontend** (`VITE_API_KEY`), không có hệ thống user, ai cũng có thể mua dịch vụ.

Cần xây dựng **backend server** để:
1. Bảo vệ BaoStar API key (chỉ backend giữ)
2. Quản lý tài khoản người dùng (đăng ký/đăng nhập)
3. Quản lý số dư & thanh toán
4. Proxy mọi request đến BaoStar API

> [!CAUTION]
> **Hiện tại API key BaoStar đang lộ hoàn toàn ở frontend.** Bất kỳ ai inspect code đều lấy được key và mua dịch vụ trên tài khoản của bạn. Backend là **bắt buộc**, không phải optional.

---

## Kiến trúc Tổng quan

```mermaid
flowchart LR
    subgraph Frontend["Frontend (Vite React)"]
        UI[Giao diện người dùng]
    end

    subgraph Backend["Backend (Express.js)"]
        AUTH[Auth API]
        PROXY[BaoStar Proxy]
        BAL[Balance API]
        DB[(SQLite/PostgreSQL)]
    end

    subgraph External["Bên ngoài"]
        BAOSTAR[BaoStar API]
        BANK[Ngân hàng / QR]
    end

    UI -->|JWT Token| AUTH
    UI -->|Mua dịch vụ| PROXY
    UI -->|Nạp / Xem số dư| BAL
    PROXY -->|API Key ẩn| BAOSTAR
    BAL -->|Webhook| BANK
```

---

## 1. Authentication (Đăng ký / Đăng nhập)

### 1.1 Phương thức đăng ký

| # | Phương thức | Đăng ký | Đăng nhập | Xác minh |
|---|---|---|---|---|
| 1 | **Username + Password** | username + mật khẩu | username + mật khẩu | Không cần |
| 2 | **Email + Password** | email + mật khẩu | email + mật khẩu | Gửi OTP email (tùy chọn) |
| 3 | **Số điện thoại + Password** | SĐT + mật khẩu | SĐT + mật khẩu | Gửi OTP SMS (tùy chọn, tốn phí) |

> [!IMPORTANT]
> **Khuyến nghị giai đoạn 1:** Chỉ xác minh bằng **email** (miễn phí với Nodemailer + Gmail). OTP SMS tốn phí (~200-400đ/tin), nên để giai đoạn 2 khi có doanh thu.

### 1.2 Database Schema — Users

```sql
CREATE TABLE users (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    username      TEXT UNIQUE NOT NULL,
    email         TEXT UNIQUE,
    phone         TEXT UNIQUE,
    password_hash TEXT NOT NULL,
    display_name  TEXT,
    balance       INTEGER DEFAULT 0,          -- Số dư (vnđ)
    role          TEXT DEFAULT 'user',         -- 'user' | 'admin'
    is_active     BOOLEAN DEFAULT 1,
    created_at    DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at    DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### 1.3 Luồng hoạt động

```mermaid
flowchart TD
    A[Mở trang web] --> B{Đã đăng nhập?}
    B -->|Có| C[Xem Dashboard + Services]
    B -->|Không| D[Trang đăng nhập]
    
    D --> E{Có tài khoản?}
    E -->|Có| F[Nhập username/email/SĐT + MK]
    E -->|Không| G[Đăng ký mới]
    
    G --> H[Nhập thông tin]
    H --> I[Tạo tài khoản]
    I --> F
    
    F --> J{Đúng MK?}
    J -->|Đúng| K[Cấp JWT Token]
    J -->|Sai| L[Báo lỗi + Retry]
    
    K --> C
    C --> M[Chọn dịch vụ + Mua]
    M --> N{Đủ số dư?}
    N -->|Đủ| O[Trừ tiền → Gọi BaoStar API]
    N -->|Không đủ| P[Báo lỗi: Nạp thêm tiền]
```

### 1.4 JWT Token Flow

| Item | Chi tiết |
|---|---|
| **Algorithm** | HS256 |
| **Access Token** | Hết hạn 24h, chứa `{ userId, username, role }` |
| **Refresh Token** | Hết hạn 7 ngày, lưu trong DB |
| **Lưu trữ** | `localStorage` (access) + `httpOnly cookie` (refresh) |

---

## 2. Hệ thống Số dư (Balance)

### 2.1 Mô hình tính giá

Bạn là **đại lý** mua qua BaoStar API với giá gốc. Bạn bán cho khách với **giá lẻ** (cộng lời):

```
Giá bán cho khách = Giá BaoStar × Hệ số lợi nhuận (VD: 1.2 = lời 20%)
```

| Ví dụ | Giá BaoStar | Hệ số | Giá bán | Lời |
|---|---|---|---|---|
| Like bài viết (100 like) | 54đ/like = 5,400đ | ×1.3 | 7,020đ | 1,620đ |
| VIP 30 ngày | 2,200đ × 30 | ×1.2 | 79,200đ | 13,200đ |

### 2.2 Database Schema — Transactions

```sql
-- Lịch sử nạp/rút/mua
CREATE TABLE transactions (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id     INTEGER NOT NULL REFERENCES users(id),
    type        TEXT NOT NULL,         -- 'deposit' | 'purchase' | 'refund'
    amount      INTEGER NOT NULL,      -- Số tiền (vnđ)
    balance_after INTEGER NOT NULL,    -- Số dư sau giao dịch
    description TEXT,
    metadata    TEXT,                   -- JSON: order_id, package_name, etc.
    status      TEXT DEFAULT 'completed', -- 'pending' | 'completed' | 'failed'
    created_at  DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Đơn hàng
CREATE TABLE orders (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id         INTEGER NOT NULL REFERENCES users(id),
    baostar_order_id INTEGER,          -- ID đơn từ BaoStar
    service_id      TEXT NOT NULL,      -- 'like-gia-re', 'follow', etc.
    package_name    TEXT NOT NULL,
    object_id       TEXT NOT NULL,
    quantity        INTEGER,
    amount          INTEGER NOT NULL,   -- Số tiền trừ
    cost            INTEGER NOT NULL,   -- Giá gốc BaoStar
    profit          INTEGER NOT NULL,   -- Lợi nhuận = amount - cost
    status          TEXT DEFAULT 'processing',
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### 2.3 Luồng mua dịch vụ

```mermaid
sequenceDiagram
    actor User
    participant FE as Frontend
    participant BE as Backend
    participant BS as BaoStar API

    User->>FE: Bấm "Mua dịch vụ"
    FE->>BE: POST /api/orders (JWT + data)
    
    BE->>BE: 1. Verify JWT
    BE->>BE: 2. Tính giá bán = giá_gốc × hệ_số
    BE->>BE: 3. Kiểm tra số dư ≥ giá bán?
    
    alt Không đủ tiền
        BE-->>FE: 400 "Không đủ số dư"
        FE-->>User: Hiện thông báo nạp tiền
    end
    
    BE->>BE: 4. Trừ số dư (transaction)
    BE->>BS: 5. Gọi BaoStar API (API key ẩn)
    
    alt BaoStar thành công
        BS-->>BE: 200 OK + order_id
        BE->>BE: 6. Lưu order
        BE-->>FE: ✅ Đặt hàng thành công
    else BaoStar lỗi
        BE->>BE: 6. Hoàn tiền (refund)
        BE-->>FE: ❌ Lỗi + đã hoàn tiền
    end
```

### 2.4 Nạp tiền

**Giai đoạn 1 — Nạp thủ công:**
1. User chuyển khoản ngân hàng với nội dung `NAPTIEN <username>`
2. Admin xác nhận → Cộng số dư

**Giai đoạn 2 — Tự động (sau khi có doanh thu):**
- Tích hợp cổng thanh toán (VNPay / MoMo /...)
- Webhook callback → Tự động cộng tiền

---

## 3. Bảo mật Route (Protected Routes)

### 3.1 Hành vi khi chưa đăng nhập

| Trang | Chưa đăng nhập | Đã đăng nhập |
|---|---|---|
| `/login`, `/register` | ✅ Truy cập được | Redirect → Dashboard |
| `/` (Dashboard) | Xem được (chỉ hiển thị danh sách dịch vụ) | Xem + số dư |
| `/facebook/*` (Services) | Xem được form, bấm "Mua" → Redirect Login | Mua bình thường |
| `/order-history` | Redirect → Login | Xem đơn hàng |
| `/deposit` | Redirect → Login | Nạp tiền |
| `/admin/*` | Redirect → Login | Chỉ role admin |

### 3.2 Frontend Guard

```tsx
// Khi bấm "Mua dịch vụ" mà chưa login
const handleSubmit = () => {
    if (!isAuthenticated) {
        toast.error('Vui lòng đăng nhập để mua dịch vụ');
        navigate('/login', { state: { from: location } });
        return;
    }
    if (user.balance < totalPrice) {
        toast.error(`Số dư không đủ. Cần ${totalPrice.toLocaleString()}đ, còn ${user.balance.toLocaleString()}đ`);
        return;
    }
    // Proceed with purchase...
};
```

---

## 4. Backend API Design

### 4.1 Auth Endpoints

| Method | Endpoint | Mô tả |
|---|---|---|
| `POST` | `/auth/register` | Đăng ký (username/email/phone + password) |
| `POST` | `/auth/login` | Đăng nhập |
| `POST` | `/auth/refresh` | Refresh access token |
| `GET` | `/auth/me` | Thông tin user + số dư |
| `POST` | `/auth/logout` | Đăng xuất (clear refresh token) |

### 4.2 Service Endpoints (Proxy BaoStar)

| Method | Endpoint | Mô tả | Auth |
|---|---|---|---|
| `GET` | `/api/prices` | Lấy danh sách gói dịch vụ | ❌ Public |
| `POST` | `/api/orders` | Mua dịch vụ (check balance → gọi BaoStar) | ✅ Required |
| `POST` | `/api/convert-uid` | Convert link → ID | ❌ Public |

### 4.3 Balance Endpoints

| Method | Endpoint | Mô tả | Auth |
|---|---|---|---|
| `GET` | `/api/user/balance` | Xem số dư | ✅ Required |
| `GET` | `/api/user/transactions` | Lịch sử giao dịch | ✅ Required |
| `POST` | `/api/admin/deposit` | Admin cộng tiền cho user | ✅ Admin only |

---

## 5. Cấu trúc thư mục Backend

```
server/
├── index.ts                 # Express server entry
├── config.ts                # Env vars, DB connection
├── middleware/
│   ├── auth.ts              # JWT verify middleware
│   └── admin.ts             # Admin role check
├── routes/
│   ├── auth.ts              # Login/Register/Me
│   ├── services.ts          # Proxy BaoStar API
│   ├── orders.ts            # Mua dịch vụ
│   └── admin.ts             # Admin endpoints
├── models/
│   ├── user.ts              # User CRUD
│   ├── transaction.ts       # Transaction CRUD
│   └── order.ts             # Order CRUD
├── utils/
│   ├── password.ts          # bcrypt hash/verify
│   ├── jwt.ts               # Token generate/verify
│   └── pricing.ts           # Tính giá bán từ giá gốc
└── database/
    ├── schema.sql            # DB schema
    └── seed.sql              # Admin user seed
```

---

## 6. Tech Stack

| Layer | Công nghệ | Lý do |
|---|---|---|
| **Frontend** | Vite + React + TypeScript | Giữ nguyên, thêm auth context |
| **Backend** | Express.js + TypeScript | Nhẹ, cùng stack JS, dễ deploy |
| **Database** | SQLite (better-sqlite3) | Không cần setup DB server, 1 file, đủ cho < 1000 users |
| **Auth** | bcrypt + JWT (jsonwebtoken) | Standard, stateless |
| **Proxy** | axios | Gọi BaoStar API từ backend |

> [!TIP]
> **Tại sao SQLite?** App nhỏ, 1 server, không cần scale. SQLite có performance tốt, zero-config, backup = copy 1 file. Khi scale lên thì migrate sang PostgreSQL.

---

## 7. Câu hỏi cần xác nhận

> [!IMPORTANT]
> Anh cần trả lời các câu hỏi sau trước khi code:

1. **Hệ số lợi nhuận**: Bán giá gấp bao nhiêu lần so với giá BaoStar? (VD: ×1.2 = lời 20%, ×1.5 = lời 50%)

2. **Nạp tiền giai đoạn 1**: Có muốn hiện trang QR chuyển khoản ngân hàng không? Nếu có, thông tin tài khoản ngân hàng?

3. **Xác minh email/SĐT**: Giai đoạn 1 có cần xác minh email không? Hay chỉ username + password là đủ?

4. **Admin dashboard**: Có cần trang admin để quản lý users, cộng tiền, xem doanh thu không?

5. **Deploy**: Dự kiến deploy ở đâu? (VPS/Cloudflare/Vercel+Railway...)

---

## Verification Plan

### Automated Tests
- Unit tests cho auth (register, login, JWT)
- Integration tests cho purchase flow (check balance → deduct → call API → refund on error)

### Manual Verification
- Đăng ký 3 phương thức (username, email, phone)
- Đăng nhập → xem số dư
- Admin cộng tiền → user thấy cập nhật
- Mua dịch vụ khi đủ tiền → đơn thành công
- Mua dịch vụ khi thiếu tiền → báo lỗi
- Mua dịch vụ khi chưa login → redirect login
- BaoStar API lỗi → hoàn tiền tự động

---

## ⚠️ NEXT STEPS
```
1️⃣ OK với Spec? Trả lời các câu hỏi ở mục 7 → gõ tiếp để bắt đầu code
2️⃣ Muốn xem UI đăng nhập/đăng ký trước? → /visualize
3️⃣ Cần chỉnh sửa Spec? → Tiếp tục thảo luận
```
