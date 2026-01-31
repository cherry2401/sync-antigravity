# Checklist: So Sánh API Request

## Thông Tin Cần Check Trong F12 DevTools

### 1. ✅ Tab "Headers" - Request URL
```
Tìm dòng:
Request URL: https://...

➡️ Copy URL đầy đủ (bao gồm tất cả query params)
```

### 2. ✅ Request Method
```
Tìm dòng:
Request Method: GET hoặc POST

➡️ Note lại là GET hay POST
```

### 3. ✅ Query String Parameters
```
Trong tab Headers, scroll xuống phần:
Query String Parameters

➡️ Check các params như:
   - count: ?
   - offset: ?
   - Các params khác: ?
```

### 4. ✅ Request Headers (quan trọng!)
```
Trong tab Headers, phần "Request Headers":

Check các headers:
- Cookie: sessionid=...; msToken=...
- User-Agent: ...
- Referer: ...
- Accept: ...
- Content-Type: ... (nếu là POST)

➡️ Copy toàn bộ headers quan trọng
```

### 5. ✅ Request Payload/Body (nếu là POST)
```
Tab "Payload" (như ảnh bạn gửi):

➡️ Click "View source" để xem raw JSON
➡️ Copy toàn bộ JSON body
```

### 6. ❓ Response
```
Tab "Response":

➡️ Xem structure của data trả về
➡️ Check xem có products[] array không
```

---

## Cách Check Nhanh

### Bước 1: Tìm Request
1. F12 → Network tab → XHR filter
2. Execute node dlir2404
3. Tìm request có tên liên quan đến "products" hoặc "showcase"

### Bước 2: Click Request
1. Click vào request đó
2. Sẽ thấy tabs: Headers, Payload, Preview, Response, Timing

### Bước 3: Copy Info
**Tab Headers:**
```
Right-click request → Copy → Copy as cURL
```
Paste vào notepad để tôi xem

HOẶC

Chụp screenshot:
- Tab Headers (Request URL + Request Headers section)
- Tab Payload (nếu có)

---

## Điểm Khác Biệt Có Thể

Từ ảnh bạn gửi, tôi thấy node dlir2404 có vẻ:

❌ **KHÔNG phải GET request đơn giản**  
✅ **Có thể là POST với body phức tạp**

Request Payload có nhiều fields:
- `requests` array
- `mode`, `credentials` 
- Các config khác

➡️ Đây là **khác hoàn toàn** với code GET đơn giản của mình!

---

## Action Ngay

**Bạn làm giúp tôi:**

1. Click vào request trong Network tab
2. Right-click → **Copy → Copy as cURL (bash)**
3. Paste vào đây cho tôi xem

Hoặc chụp rõ:
- Tab **Headers** (phần Request Headers)
- Tab **Payload** click "view source"

Tôi sẽ update code ngay! 🚀
