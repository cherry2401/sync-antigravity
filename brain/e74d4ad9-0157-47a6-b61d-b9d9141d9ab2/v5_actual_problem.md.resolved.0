# Workflow V5 - Phân Tích Lại Đúng

## 🔍 Flow Hiện Tại ĐANG LÀM GÌ?

### Prepare Group Media Items:
```javascript
// Input: [group1_data, group2_data, group3_data]
// Output: [
//   {media_url: "m1", group_id: "g1", page_id: "p1", ...},
//   {media_url: "m2", group_id: "g1", page_id: "p1", ...},
//   {media_url: "m1", group_id: "g2", page_id: "p2", ...},
//   {media_url: "m2", group_id: "g2", page_id: "p2", ...},
// ]
```

### Split Group Media Batch (batch=1):
```
Loop iteration 1: media1_group1
  → Upload media1 → ID: "123"
  → Create Group Post (group_id: g1, page_id: p1, mediaIds: "123")
  → Post created! ✅
  
Loop iteration 2: media2_group1  
  → Upload media2 → ID: "456"
  → Create Group Post (group_id: g1, page_id: p1, mediaIds: "456")
  → Post created again?! ❌❌❌
```

## 🔴 VẤN ĐỀ THỰC SỰ

**Workflow sẽ TẠO NHIỀU POSTS cho cùng 1 group!**

- Media 1 của group 1 → Tạo post có 1 media
- Media 2 của group 1 → Tạo post khác có 1 media
- Media 1 của group 2 → Tạo post có 1 media
- ...

**KẾT QUẢ:** Thay vì 1 post với 3 media, sẽ có 3 posts riêng biệt!

---

## ✅ CẦN PHẢI LÀM

### Option 1: Upload HẾT media, rồi mới post

```
Loop qua groups (1 group / lần):
  → Upload TẤT CẢ media của group này → Collect media IDs
  → Tạo 1 POST duy nhất với TẤT CẢ media IDs
  → Log, notify
  → Next group
```

### Option 2: Dùng node "Aggregate" 

Upload từng media, nhưng AGGREGATE media IDs trước khi post:

```
Loop media items:
  → Upload → Collect ID
  ↓ (when done with all media of 1 group)
Aggregate all media IDs
  → Create post with all IDs
```

---

## 🎯 RECOMMENDED: Option 1

Đơn giản và rõ ràng:

```
Route By Post Type (Media - Group)
  ↓
Loop Groups (Split In Batches - batch=1)
  ↓
Prepare Media for Current Group (Code)
  ↓
HTTP Request (Upload multiple media in parallel or loop)
  ↓
Aggregate Media IDs (Code: collect all IDs)
  ↓
Create Group Post (with all media IDs)
  ↓
Log → Notify → Wait
  ↓
Loop back to next group
```

---

## 💡 Simplified Version

Nếu mỗi group chỉ có ÍT media (<5), có thể upload PARALLEL:

```javascript
// Node: "Upload All Group Media"
const groupData = $input.first().json;
const mediaUrls = groupData.media_urls || [];

// Upload tất cả parallel bằng HTTP Request node với multiple items
// n8n sẽ tự động execute parallel

// Sau đó aggregate results
```

---

## ❓ CÂU HỎI

**Hiện tại khi bạn chạy workflow:**
1. Mỗi group có BAO NHIÊU media thường?
2. Có bao nhiêu groups?
3. Workflow tạo ra bao nhiêu posts? (1 post/group hay nhiều posts/group?)

Câu trả lời sẽ giúp tôi đề xuất giải pháp chính xác!
