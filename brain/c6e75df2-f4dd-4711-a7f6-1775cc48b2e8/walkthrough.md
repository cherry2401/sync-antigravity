# Tổng Kết: Sửa Lỗi Custom n8n TikTok Nodes

## Tổng Quan

Đã sửa thành công các custom nodes n8n cho TikTok (Get Products, Upload Video). Các nodes này giờ có thể cài đặt và dùng miễn phí không giới hạn, thay thế service trả phí dlir2404.

---

## Các Vấn Đề Đã Sửa

### 1. ✅ Cải Thiện Cấu Trúc Credential

**Vấn đề**: Form credential không rõ ràng, user không biết phải điền gì.

**Giải pháp**: Viết lại file [`TikTokSession.credentials.ts`](file:///i:/Workflow/n8n/Test/TikTok/n8n-nodes-tiktok-custom/credentials/TikTokSession.credentials.ts)

**Thay đổi**:
- ✅ **Hướng dẫn chi tiết** từng bước bằng tiếng Việt
- ✅ **Ví dụ mẫu** rõ ràng với placeholder
- ✅ **Format JSON đơn giản** hơn: chỉ cần `url` và `headers`
- ✅ **Link trực tiếp** đến tool convert: curlconverter.com/json

**Credential sẽ hiển thị trong n8n**:
```
Field name: Session Data
Hướng dẫn: Tiếng Việt với emoji, dễ đọc
Mẫu JSON: Có placeholder rõ ràng
```

---

### 2. ✅ Thêm File Entry Point Bị Thiếu

**Vấn đề**: n8n không load được nodes vì thiếu file `index.ts`.

**Giải pháp**: Tạo file [`index.ts`](file:///i:/Workflow/n8n/Test/TikTok/n8n-nodes-tiktok-custom/index.ts)

```typescript
// Export credentials
export * from './credentials/TikTokSession.credentials';

// Export nodes  
export * from './nodes/TikTok/TikTokProducts.node';
export * from './nodes/TikTok/TikTokUpload.node';
```

---

### 3. ✅ Thêm Dependencies Thiếu

**Vấn đề**: Node `TikTokUpload` cần upload video file nhưng thiếu package `form-data`.

**Giải pháp**: Cập nhật [`package.json`](file:///i:/Workflow/n8n/Test/TikTok/n8n-nodes-tiktok-custom/package.json)

**Thay đổi**:
- Thêm `form-data: ^4.0.0`
- Bump version từ `1.0.3` → `1.0.4`

---

### 4. ✅ Sửa Lỗi TypeScript

**Vấn đề**: Field `icon` trong credentials gây lỗi compile.

**Giải pháp**: Xóa field `icon` không tương thích (credentials không hỗ trợ).

---

## Kết Quả Build

### Build Thành Công ✅
```bash
> n8n-nodes-tiktok-custom@1.0.4 build
> tsc && npm run copy-icons

✓ Không có lỗi TypeScript
✓ Icons đã copy vào dist/
```

### Package Đã Tạo ✅

**File**: `n8n-nodes-tiktok-custom-1.0.4.tgz`
- Kích thước: **36.6 kB**
- Giải nén: **120.0 kB**  
- Tổng files: **14 files**

**Nội dung package**:
- ✅ `dist/credentials/TikTokSession.credentials.js`
- ✅ `dist/nodes/TikTok/TikTokProducts.node.js`
- ✅ `dist/nodes/TikTok/TikTokUpload.node.js`
- ✅ `dist/nodes/TikTok/tiktok.png` (icon)
- ✅ `dist/index.js` (entry point)

---

## Hướng Dẫn Cài Đặt

Chi tiết đầy đủ → [`INSTALL_GUIDE.md`](file:///i:/Workflow/n8n/Test/TikTok/n8n-nodes-tiktok-custom/INSTALL_GUIDE.md)

### Cài Đặt Nhanh

**Cách 1: Qua npm (Recommended)**
```bash
cd ~/.n8n/nodes
npm install "i:\Workflow\n8n\Test\TikTok\n8n-nodes-tiktok-custom\n8n-nodes-tiktok-custom-1.0.4.tgz"
# Restart n8n
```

**Cách 2: Qua n8n UI**
1. Settings → Community Nodes
2. Install from file
3. Upload file `.tgz`
4. Restart n8n

---

## Cách Lấy TikTok Session

### Công Cụ Cần Thiết
- Trình duyệt: Chrome/Edge
- Website: https://curlconverter.com/json/

### Các Bước Thực Hiện

**Bước 1**: Đăng nhập TikTok.com

**Bước 2**: Mở DevTools
- Nhấn **F12**
- Chuyển sang tab **Network**
- Bật filter **XHR**

**Bước 3**: Capture Request
- **Để lấy Products**: Vào trang TikTok Shop/Creator Center → Products
- **Để upload**: Vào trang upload TikTok, bắt đầu upload video test
- Tìm request API có URL liên quan

**Bước 4**: Copy cURL
- Chuột phải vào request → **Copy** → **Copy as cURL (bash)**

**Bước 5**: Convert sang JSON
- Vào https://curlconverter.com/json/
- Paste cURL command
- Copy kết quả JSON

**Bước 6**: Dùng trong n8n
- Paste JSON vào credential field "Session Data"
- Click **Save**

### Format JSON Cần Có

```json
{
  "url": "https://www.tiktok.com/api/commerce/v1/creator/products",
  "headers": {
    "Cookie": "sessionid=<session_của_bạn>; msToken=<token_của_bạn>",
    "User-Agent": "Mozilla/5.0...",
    "Referer": "https://www.tiktok.com/",
    "Accept": "application/json"
  }
}
```

---

## ⚠️ Lưu Ý Quan Trọng

### 🔄 Session Hết Hạn
- Cookies TikTok (`sessionid`, `msToken`) **hết hạn** sau vài ngày đến vài tuần
- **Triệu chứng**: Node báo lỗi authentication
- **Giải pháp**: Capture lại session mới từ browser

### 🔗 API Endpoints
- URL trong code hiện tại là **placeholders**
- **Cần làm**: Capture URL thật từ browser DevTools
- Các operation khác nhau cần **endpoints khác nhau**:
  - Get Products: `/api/commerce/v1/creator/products`
  - Upload Video: `/api/v1/item/create/` (nhiều bước)

### ⏱️ Rate Limiting
- TikTok có giới hạn số request
- Request quá nhiều = bị block tạm thời
- **Giải pháp**: Thêm delay giữa các operations

---

## Kiểm Tra Sau Khi Cài

### Nodes Hiển Thị Chưa?
1. Mở workflow editor
2. Search "TikTok"
3. Phải thấy 2 nodes:
   - **Get Products In Showcase**
   - **TikTok Upload**

### Nếu Không Thấy Nodes
- Chắc chắn đã chạy `npm run build`
- **Restart n8n hoàn toàn** (không chỉ reload trang)
- Check n8n logs xem có error không
- Verify file `dist/index.js` đã được tạo

### Test Credential
1. Thêm node "Get Products In Showcase" vào workflow
2. Click **Create New Credential**
3. Chọn **TikTok Session**
4. Điền session data theo hướng dẫn
5. Click **Test** hoặc **Execute** node để kiểm tra

---

## Các Bước Tiếp Theo

Bạn cần làm thêm:

### 1. Cài Đặt Package
- Chọn 1 trong các method cài đặt
- Restart n8n
- Verify nodes đã xuất hiện

### 2. Capture Session
- Mở TikTok.com
- Dùng DevTools capture request
- Convert cURL sang JSON
- Lưu vào credential

### 3. Test Nodes
- Tạo workflow test
- Thêm node "Get Products"
- Chạy thử xem có lấy được data không

### 4. Update Endpoints (Nếu Cần)
- Nếu API URL không đúng
- Capture lại từ browser
- Update vào session data

---

## Tổng Kết

✅ **Build**: Thành công, không lỗi  
✅ **Package**: Đã tạo (36.6 kB)  
✅ **Cấu trúc**: Đầy đủ files trong dist/  
✅ **Entry Point**: index.js exports đúng  
✅ **Dependencies**: form-data đã add  
✅ **Hướng dẫn**: Tiếng Việt chi tiết  

⏳ **Chờ**: Bạn cài vào n8n và test với session thật

---

## Files Đã Sửa/Tạo

| File | Hành động | Mục đích |
|------|-----------|----------|
| [`credentials/TikTokSession.credentials.ts`](file:///i:/Workflow/n8n/Test/TikTok/n8n-nodes-tiktok-custom/credentials/TikTokSession.credentials.ts) | ✏️ Sửa | Format JSON tốt hơn, hướng dẫn tiếng Việt |
| [`index.ts`](file:///i:/Workflow/n8n/Test/TikTok/n8n-nodes-tiktok-custom/index.ts) | ➕ Tạo mới | Entry point export nodes & credentials |
| [`package.json`](file:///i:/Workflow/n8n/Test/TikTok/n8n-nodes-tiktok-custom/package.json) | ✏️ Sửa | Thêm form-data, version 1.0.4 |
| [`INSTALL_GUIDE.md`](file:///i:/Workflow/n8n/Test/TikTok/n8n-nodes-tiktok-custom/INSTALL_GUIDE.md) | ➕ Tạo mới | Hướng dẫn cài đặt tiếng Việt đầy đủ |
| `n8n-nodes-tiktok-custom-1.0.4.tgz` | 📦 Build | Package sẵn sàng cài đặt |

---

## Troubleshooting Nhanh

**Nodes không hiện**: Restart n8n + check logs  
**Auth Failed**: Session hết hạn → capture lại  
**API Error**: URL sai → capture endpoint mới  
**Rate Limited**: Đợi vài phút + thêm delay
