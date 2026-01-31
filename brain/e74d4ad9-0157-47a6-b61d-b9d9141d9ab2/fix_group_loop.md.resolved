# Fix Group Loop Structure

## 🔴 Vấn Đề Hiện Tại

**Flow hiện tại (SAI):**
```
Route By Post Type (Media - Group) 
  → Prepare Group Media Items (flatten ALL groups → media items)
  → Split Group Media Batch
  → ... upload ... post ...
  → Update Post Completed
  → Wait Group Delay
  → ??? (Không biết quay về đâu!)
```

**Kết quả:**
- ❌ Nếu nối về "Split Group Media Batch" → Bỏ qua "Prepare" → Không có data
- ❌ Nếu nối về "Prepare Group Media Items" → Không loop vì "Prepare" cần data mới từ Route

---

## ✅ Giải Pháp: Thêm Loop Node

### Cần thêm node "Split In Batches" để LOOP qua từng GROUP!

**Flow ĐÚNG:**

```
Route By Post Type (Media - Group)
  → 🆕 LOOP OVER GROUPS (Split In Batches)
    → Prepare Group Media Items (chỉ 1 group)
    → Split Group Media Batch (media của group này)
    → ... upload ... post ...
    → Update Post Completed
    → Wait Group Delay
    → LOOP lại LOOP OVER GROUPS ⬆️
```

---

## 📋 Hướng Dẫn Fix

### Bước 1: Thêm Node "Split In Batches"

1. Click vào canvas giữa "Route By Post Type (Media)" và "Prepare Group Media Items"
2. Thêm node "Split In Batches"
3. Đặt tên: **"Loop Over Groups"**
4. Config:
   - **Batch Size:** `1` (xử lý 1 group mỗi lần)
   - **Options:** Để mặc định

---

### Bước 2: Sửa "Prepare Group Media Items"

Thay code để CHỈ xử lý 1 group (item hiện tại):

```javascript
// KHÔNG dùng $input.all() nữa!
const groupData = $input.item.json;  // Chỉ lấy 1 group

const mediaUrls = groupData.media_urls || [];
const allMediaItems = [];

if (!mediaUrls || mediaUrls.length === 0) {
  allMediaItems.push({
    json: {
      ...groupData,
      media_ids: '',
      skip_upload: true
    }
  });
} else {
  mediaUrls.forEach((url, index) => {
    allMediaItems.push({
      json: {
        media_url: url,
        media_index: index,
        group_id: groupData.group_id,
        page_id: groupData.page_id,
        access_token: groupData.access_token,
        post_id: groupData.post_id,
        content: groupData.content,
        group_name: groupData.group_name,
        group_index: groupData.group_index,
        total_groups: groupData.total_groups,
        delay_seconds: groupData.delay_seconds,
        post_type: groupData.post_type || 'Group'
      }
    });
  });
}

return allMediaItems;
```

---

### Bước 3: Kết Nối Lại

**Kết nối mới:**

```
Route By Post Type (Media - Group)
  ↓
🆕 Loop Over Groups
  ↓
Prepare Group Media Items
  ↓
Split Group Media Batch
  ↓
... (upload, post, log, telegram, update)
  ↓
Wait Group Delay
  ↓
QUAY LẠI → Loop Over Groups (loop output)
```

**Cụ thể:**
1. Disconnect "Route By Post Type (Media)" → "Prepare Group Media Items"
2. Connect "Route By Post Type (Media)" → **"Loop Over Groups"**
3. Connect **"Loop Over Groups"** (output 1 - processing) → "Prepare Group Media Items"
4. Connect "Wait Group Delay" → **"Loop Over Groups"** (loop input)
5. Connect **"Loop Over Groups"** (output 0 - done) → ??? (có thể là "Split Posts Batch" để lấy post tiếp)

---

## 🎯 Tương Tự Cho Text-Only Groups

Nếu có nhánh Text-only groups, cũng cần thêm loop tương tự:

```
Route By Post Type (Text - Group)
  → Loop Over Groups (Text)
  → Post Text Only
  → Update/Log/Notify
  → Wait
  → Loop lại
```

---

## ✅ Expected Result

Sau khi fix:
- ✅ Post group 1 → wait → loop
- ✅ Post group 2 → wait → loop
- ✅ Post group 3 → wait → done
- ✅ Chuyển sang post tiếp theo (nếu có)

---

## 🔍 Verify

Test với post có 3 groups:
1. Execute workflow
2. Xem flow đăng lần lượt từng group
3. Có delay giữa các groups
4. Sau khi hết groups → workflow kết thúc hoặc chuyển post tiếp
