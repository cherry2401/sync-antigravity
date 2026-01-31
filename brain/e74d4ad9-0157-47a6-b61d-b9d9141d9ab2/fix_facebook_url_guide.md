# Hướng Dẫn Sửa Lỗi Facebook URL trong v5

## 🔴 Vấn Đề
Cả Page và Group posts đều không output Facebook URL, chỉ hiện "N/A"

## 🎯 Nguyên Nhân
Code đang dùng `$json.post_id` nhưng Facebook API trả về field `id`

---

## ✅ Cách Sửa (2 nodes cần fix)

### 1️⃣ **Construct Facebook URL** (text posts)

**Bước 1:** Mở workflow `Scheduled_Group_Post_v5` trong n8n

**Bước 2:** Tìm node **"Construct Facebook URL"** (nằm sau "Post Text Only")

**Bước 3:** Double-click vào node → tab "Parameters"

**Bước 4:** Trong code editor, tìm dòng:
```javascript
const postId = $json.post_id || '';
```

**Bước 5:** Đổi thành:
```javascript
const postId = $json.id || $json.post_id || '';
```

**Bước 6:** Click **"Execute node"** để test → Nhấn **"Save"**

---

### 2️⃣ **Construct Facebook URL1** (media posts)

**Bước 1:** Tìm node **"Construct Facebook URL1"** (nằm sau "Create Group Post using Page")

**Bước 2:** Double-click vào node → tab "Parameters"

**Bước 3:** Tìm dòng:
```javascript
const postId = $json.post_id || '';
```

**Bước 4:** Đổi thành:
```javascript
const postId = $json.id || $json.post_id || '';
```

**Bước 5:** Click **"Execute node"** để test → Nhấn **"Save"**

---

## 📊 Giải Thích

**Trước (SAI):**
```javascript
const postId = $json.post_id || '';  // ❌ field không tồn tại
// → postId = ''
// → URL = "https://www.facebook.com/123456/posts/" → "N/A"
```

**Sau (ĐÚNG):**
```javascript
const postId = $json.id || $json.post_id || '';  // ✅ 
// → postId = "4721470959918861_122147074707821515"
// → URL = "https://www.facebook.com/4721470959918861/posts/122147074707821515"
```

---

## ✅ Kiểm Tra

Sau khi sửa xong:
1. Execute lại workflow từ đầu
2. Check output của các nodes sau khi đăng thành công
3. Verify field `facebook_url` có giá trị đúng

**Expected output:**
```json
{
  "facebook_url": "https://www.facebook.com/4721470959918861/posts/122147074707821515",
  "post_type_display": "Page"
}
```
