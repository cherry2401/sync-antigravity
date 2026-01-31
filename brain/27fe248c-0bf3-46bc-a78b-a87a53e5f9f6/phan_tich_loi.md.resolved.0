# Phân Tích Lỗi Facebook Graph API

## 📌 Tóm Tắt Lỗi

Bạn đang gặp lỗi khi gọi Facebook Graph API với thông báo:

> **Bad request - please check your parameters**
> 
> Unsupported post request. Object with ID '**114993947297504**' does not exist, cannot be loaded due to missing permissions, or does not support this operation.

---

## 🔍 Nguyên Nhân Chính

Có **3 lý do chính** gây ra lỗi này:

### 1. **Token Không Hợp Lệ Cho Page ID**

![Token Info](file:///C:/Users/Cherry/.gemini/antigravity/brain/27fe248c-0bf3-46bc-a78b-a87a53e5f9f6/uploaded_image_2_1763540122535.png)

Theo hình ảnh từ **Facebook Access Token Manager**:
- Token có **Tên Trang**: "Nguyễn Trần Linh Vũ"
- Token có **ID Trang**: `114993947297504`
- Token type: **PAGE token** (không phải User token)
- Cảnh báo: **"⚠️ Không hết hạn (Page Token)"** - màu tím

**Vấn đề**: Bạn đang dùng **Page Access Token** nhưng cố gắng POST lên một endpoint yêu cầu **User Access Token** hoặc quyền khác.

---

### 2. **Quyền Hạn (Permissions) Không Đúng**

Từ hình ảnh Token Manager, token chỉ có các quyền:
```
pages_show_list, pages_messaging, pages_read_engagement, 
pages_manage_metadata, pages_read_user_content, pages_manage_posts, 
pages_manage_engagement, pages_utility_messaging, public_profile
```

**Thiếu quyền quan trọng**:
- `publish_to_groups` (nếu đăng lên group)
- `pages_manage_posts` với scope cao hơn
- Hoặc cần **User Access Token** thay vì Page Token

---

### 3. **URL Endpoint Không Đúng**

![API Request](file:///C:/Users/Cherry/.gemini/antigravity/brain/27fe248c-0bf3-46bc-a78b-a87a53e5f9f6/uploaded_image_0_1763540122535.png)

Từ hình ảnh, URL bạn đang dùng:
```
https://graph.facebook.com/v22.0/{{$json.target_page_id}}/feed
```

**Phân tích**:
- `{{$json.target_page_id}}` được thay thế thành `114993947297504`
- Bạn đang cố POST lên `/114993947297504/feed`

**Vấn đề**: 
- Nếu `114993947297504` là **Page ID**, bạn cần dùng **Page Access Token của chính page đó**
- Nếu bạn dùng token của page khác, sẽ bị lỗi permissions
- Nếu `114993947297504` là **User/Profile ID**, không thể POST lên `/feed` (chỉ có thể đọc)

---

## ✅ Giải Pháp

### **Kiểm Tra Token vs Target Page**

Bạn cần xác nhận:

1. **Token của page nào?**
   - Hiện tại: Token thuộc page "Nguyễn Trần Linh Vũ" (ID: `114993947297504`)

2. **Muốn đăng lên page nào?**
   - Nếu đăng lên **cùng page** (`114993947297504`): ✅ OK
   - Nếu đăng lên **page khác**: ❌ KHÔNG được phép

### **Cách Sửa Lỗi**

#### Nếu đăng lên cùng page với token:

✅ Endpoint đúng:
```
POST https://graph.facebook.com/v22.0/114993947297504/feed
```

✅ Sử dụng token hiện tại (token của page `114993947297504`)

---

#### Nếu đăng lên page khác:

Bạn cần:
1. **Lấy Page Access Token của page đích**
2. Hoặc dùng **User Access Token** với quyền `pages_manage_posts` cho cả 2 page

---

### **Kiểm Tra Config Pages Sheet**

![Google Sheets](file:///C:/Users/Cherry/.gemini/antigravity/brain/27fe248c-0bf3-46bc-a78b-a87a53e5f9f6/uploaded_image_1_1763540122535.png)

Theo Google Sheets của bạn:
- **Page đích**: Có cột "Page đích" với giá trị (có thể là Page ID hoặc Page Name)
- **Access Token**: Cột "Access Token" phải chứa token **của page đích đó**

**Kiểm tra**:
```
1. Cột "Page đích" = ID gì? 
2. Access Token trong sheet có phải của page đó không?
```

---

## 🎯 Hướng Dẫn Cụ Thể

### Bước 1: Xác định Page ID muốn đăng

Mở Google Sheets, xem giá trị tại:
- Dòng 2: Page đích = ?
- Dòng 3: Page đích = ?

### Bước 2: Lấy đúng Access Token

Với mỗi Page ID, cần:
1. Vào [Facebook Access Token Manager](https://business.facebook.com/latest/home)
2. Chọn đúng page muốn đăng
3. Generate Page Access Token với quyền:
   - ✅ `pages_manage_posts`
   - ✅ `pages_read_engagement`

### Bước 3: Update Sheet hoặc Workflow

**Option 1**: Update Google Sheets
```
Cột "Access Token" = [Token của page tương ứng với cột "Page đích"]
```

**Option 2**: Sửa Workflow
- Đảm bảo biến `$json.target_page_id` là **Page ID hợp lệ**
- Đảm bảo token được sử dụng là **Page Access Token của page đó**

---

## ⚠️ Lưu Ý Quan Trọng

### Page Access Token vs User Access Token

| Token Type | Dùng để | Hạn chế |
|-----------|---------|---------|
| **Page Access Token** | Đăng bài **lên chính page đó** | Chỉ dùng cho 1 page cụ thể |
| **User Access Token** | Đăng bài **lên các page mà user quản lý** | Cần quyền `pages_manage_posts` |

### Endpoint Không Hợp Lệ

❌ **KHÔNG thể POST lên**:
- User Profile feed: `/[USER_ID]/feed` (chỉ đọc được)
- Page khác với token không phù hợp

✅ **CÓ thể POST lên**:
- Page feed với Page Access Token: `/[PAGE_ID]/feed`
- Page feed với User Access Token (nếu có quyền)

---

## 📝 Tóm Lại

**Nguyên nhân chính**: 
> Bạn đang dùng **Page Access Token của page A** để cố POST lên `/feed` của **object khác** mà token không có quyền.

**Giải pháp**:
1. ✅ Kiểm tra `target_page_id` = gì
2. ✅ Kiểm tra token có phải của page đó không
3. ✅ Nếu không, lấy đúng token của page đích
4. ✅ Hoặc dùng User Access Token thay vì Page Token

---

## 🛠️ Debug Steps

Để kiểm tra token và permissions:

```bash
# Test token info
GET https://graph.facebook.com/v22.0/me?access_token=YOUR_TOKEN

# Test permissions
GET https://graph.facebook.com/v22.0/me/permissions?access_token=YOUR_TOKEN

# Test page access
GET https://graph.facebook.com/v22.0/PAGE_ID?access_token=YOUR_TOKEN
```

Nếu cần, tôi có thể giúp bạn debug cụ thể hơn nếu bạn cho tôi biết:
- Page đích là page nào?
- Token hiện tại được lấy từ đâu?
