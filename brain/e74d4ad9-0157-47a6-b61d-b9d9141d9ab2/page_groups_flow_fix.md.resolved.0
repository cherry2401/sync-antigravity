# Page → Groups Flow - Đúng Structure

## 🎯 Requirement

**User muốn:**
1. Đăng **1 POST lên PAGE trước**
2. SAU ĐÓ đăng **POST ĐÓ lên TẤT CẢ GROUPS** (loop từng group)

---

## 🔴 Vấn Đề Hiện Tại

### Hiểu về `Split Group Media Batch`:

Node này **KHÔNG PHẢI loop over groups**!

Nó là **Split In Batches** để loop qua **MEDIA ITEMS** của TẤT CẢ groups đã được flatten!

**Flow hiện tại:**
```
Prepare Group Media Items 
  → Output: [media1_group1, media2_group1, media1_group2, media2_group2, ...]
  ↓
Split Group Media Batch (batch size = 1)
  → Xử lý từng MEDIA ITEM, KHÔNG phải từng GROUP!
```

**Kết quả:** Sẽ upload media lần lượt, NHƯNG post tất cả groups cùng lúc sau khi upload hết!

---

## ✅ GIẢI PHÁP ĐÚNG

Cần **2 TẦNG LOOP:**

### Tầng 1: Loop Over Groups
### Tầng 2: Loop Over Media (của mỗi group)

---

## 📋 Structure Mới

```
Route By Post Type (Media - Page)
  ↓
Prepare Page Media → ... → Post to Page → Update Page
  ↓
Wait After Page
  ↓
Route By Post Type (Media - Group) 
  ↓
🆕 LOOP GROUPS (Split In Batches - batch=1)
  ↓ [Output 1 - Processing]
  ↓
Filter Current Group (Code: lọc 1 group từ all groups)
  ↓
Prepare Media for Current Group
  ↓
🆕 LOOP MEDIA (Split In Batches - batch=1)
  ↓ [Output 1]
  ↓
Convert → Format → Upload → Wait
  ↓ [Loop back to LOOP MEDIA]
  ↓ [Output 0 - All media done]
  ↓
Create Group Post
  ↓
Log → Telegram → Update
  ↓
Wait Group Delay
  ↓ [Loop back to LOOP GROUPS]
  ↓
[Output 0 - All groups done]
  ↓
Continue to next post or end
```

---

## 🔧 Implementation

### Node 1: "Loop Groups" (Split In Batches)
- **Position:** Sau "Route By Post Type (Media - Group)"
- **Config:** Batch Size = 1

### Node 2: "Filter Current Group" (Code)
```javascript
// Lấy group hiện tại từ loop
const currentGroupData = $input.item.json;

// Return as single item
return {
  json: currentGroupData
};
```

### Node 3: "Prepare Media for Current Group" (Code)
```javascript
// Chỉ prepare media cho 1 group
const groupData = $input.first().json;
const mediaUrls = groupData.media_urls || [];

if (!mediaUrls || mediaUrls.length === 0) {
  return [{
    json: {
      ...groupData,
      skip_upload: true
    }
  }];
}

return mediaUrls.map((url, index) => ({
  json: {
    media_url: url,
    media_index: index,
    ...groupData
  }
}));
```

### Node 4: "Loop Media Items" (Split In Batches)
- **Position:** Sau "Prepare Media for Current Group"  
- **Config:** Batch Size = 1
- **Loop back:** Sau "Wait After Upload" → quay về "Loop Media Items"

### Connections:
```
Loop Groups [0] → Next post/End
Loop Groups [1] → Filter Current Group
Filter Current Group → Prepare Media → Loop Media Items
Loop Media Items [0] → Create Post
Loop Media Items [1] → Convert → Upload → (loop back)
Create Post → ... → Wait → (loop back to Loop Groups)
```

---

## 🎯 Expected Behavior

1. Post to Page
2. Wait
3. **Start Groups loop:**
   - Group 1:
     - Upload media 1 → wait
     - Upload media 2 → wait
     - Create post with all media
     - Log, notify, wait
   - Group 2:
     - Upload media 1 → wait
     - ...
   - Group 3...
4. Done

---

## ⚠️ Alternative: Simplify if Media Upload is Fast

Nếu không cần wait giữa từng media upload:

```
Loop Groups
  ↓
Prepare ALL media for current group → Upload ALL → Wait
  ↓
Create Post → Log → Wait
  ↓ (loop back)
```

Cách này đơn giản hơn nhưng upload tất cả media cùng lúc (parallel).
