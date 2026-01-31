# Fix Wait Group Delay - Giải Pháp Đúng

## 📸 Phân Tích Workflow (từ screenshot)

**Vùng màu CAM (Đăng Page):**
```
... → Post to Page Timeline → ... → Update Post Completed → Wait Group Delay1
```

**Vùng màu HỒNG (Đăng Group):**
```
... → Create Group Post → ... → Update Post Completed1 → Wait Group Delay
```

---

## 🔴 Vấn Đề

Node `Wait Group Delay` hiện tại:
```javascript
={{ $('Split Group Media Batch').item.json.delay_seconds }}
```

❌ **Lỗi:** Page flow không chạy qua `Split Group Media Batch`

---

## ✅ Giải Pháp ĐÚNG: Dùng `$input`

### Thay đổi "Wait Amount" thành:

```javascript
={{ $input.first().json.delay_seconds || 180 }}
```

### 🎯 Tại sao đúng?

- `$input` = data từ node TRƯỚC ĐÓ (Update Post Completed/Update Post Completed1)
- ✅ KHÔNG cần reference tên node cụ thể
- ✅ Hoạt động cho CẢ Page và Group flows
- ✅ Fallback 180 nếu không có field

---

## 🔍 Kiểm Tra Cần Thiết

### ⚠️ Đảm bảo node "Update Post Completed" pass data qua:

Node này cần **KHÔNG xóa** data cũ, chỉ add thêm fields mới.

Kiểm tra trong node "Update Post Completed":
- Nếu chỉ update Sheet → data BỊ MẤT
- Cần có code pass-through data

### Nếu "Update Post Completed" KHÔNG có `delay_seconds`:

**Option A: Thêm field vào Update nodes**

Trong cả 2 nodes `Update Post Completed` và `Update Post Completed1`:

Thêm vào config:
```javascript
{
  ...existing fields,
  delay_seconds: $json.delay_seconds || 180
}
```

**Option B: Dùng node khác TRƯỚC Update**

Reference node TRƯỚC "Update Post Completed":
```javascript
={{ $('Telegram Notify Success').first().json.delay_seconds || 180 }}
```

HOẶC:

```javascript
={{ $('Log Success to Sheet').first().json.delay_seconds || 180 }}
```

---

## 📋 Hướng Dẫn Fix NHANH NHẤT

### Cách 1: Dùng $input (RECOMMENDED)

1. Mở node `Wait Group Delay`
2. Xóa expression cũ
3. Nhập:
   ```javascript
   ={{ $input.first().json.delay_seconds || 180 }}
   ```
4. Execute để test
5. Nếu **LỖI hoặc không có delay** → Dùng Cách 2

---

### Cách 2: Reference node CỤ THỂ có data

Tìm node MÀ CẢ 2 flows đều chạy qua VÀ có `delay_seconds`:

**Test từng node này:**

```javascript
={{ $('Construct Facebook URL').first().json.delay_seconds || 180 }}
```

HOẶC

```javascript
={{ $('Construct Facebook URL1').first().json.delay_seconds || 180 }}
```

HOẶC (nếu workflow có):

```javascript
={{ $('Post Text Only').first().json.delay_seconds || 180 }}
```

---

## 🎯 Cách Tìm Node Đúng

1. Execute workflow với Page post
2. Xem OUTPUT của từng node TRƯỚC `Wait Group Delay`
3. Tìm node CÓ field `delay_seconds` trong output
4. Dùng node đó trong expression

**VD:** Nếu thấy "Construct Facebook URL" có output:
```json
{
  "delay_seconds": 160,
  "facebook_url": "...",
  ...
}
```

→ Dùng: `={{ $('Construct Facebook URL').first().json.delay_seconds || 180 }}`

---

## ✅ Tóm Tắt

**Thử theo thứ tự:**

1. ✅ `$input.first().json.delay_seconds || 180`
2. ✅ `$('Construct Facebook URL').first().json.delay_seconds || 180`  
3. ✅ `$('Log Success to Sheet').first().json.delay_seconds || 180`

**Pick cái nào KHÔNG LỖI và có giá trị đúng!**
