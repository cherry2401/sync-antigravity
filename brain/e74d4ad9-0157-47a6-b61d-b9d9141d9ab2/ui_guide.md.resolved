# Hướng dẫn: Chuyển v3_CLEAN thành Switch Architecture

## ✅ Đã có trong v3_CLEAN (giữ nguyên):
- Schedule Trigger ✓
- Read Posts Schedule ✓
- Split Posts Batch ✓
- Parse Media & Groups (cần sửa nhỏ)
- Read Groups Config ✓
- Combine Post + Groups (cần sửa nhỏ)
- Split Groups Batch ✓
- Wait Group Delay ✓
- Log Success/Error ✓
- Update Post Completed ✓

## 🆕 Cần THÊM/SỬA:

### Bước 1: Thêm Filter Pending
1. Drag node **Filter** vào giữa "Read Posts Schedule" và "Split Posts Batch"
2. Cấu hình:
   - Conditions: `Status` equals `Pending`
   - Kết nối: Read Posts Schedule → Filter Pending → Split Posts Batch

### Bước 2: Sửa "Parse Media & Groups"
1. Mở node "Parse Media & Groups"
2. Trong code, thêm dòng `has_media`:
```javascript
return {
  json: {
    post_id: postData['Post ID'],
    content: postData['Content'],
    media_urls: mediaUrls,
    has_media: mediaUrls.length > 0,  // ← THÊM DÒNG NÀY
    group_ids: groupIds
  }
};
```

### Bước 3: Sửa "Combine Post + Groups Data"
1. Tìm dòng: `has_media: (postData.media_urls || []).length > 0,`
2. Đổi thành: `has_media: postData.has_media,`

### Bước 4: XÓA các nodes cũ không dùng
Xóa các nodes sau (không cần trong kiến trúc Switch):
- ❌ IF Skip Upload
- ❌ IF Group Has Media  
- ❌ Prepare Group Media Items
- ❌ Split Group Media Batch
- ❌ Convert Group File ID to URL
- ❌ Format Group File URL
- ❌ Upload Group Media to Facebook
- ❌ Wait After Group Media Upload
- ❌ Prepare Post Data with Media
- ❌ Prepare Post Data without Media
- ❌ Construct Facebook URL

### Bước 5: Thêm Switch Node
1. Thêm node **Switch** sau "Wait Group Delay"
2. Tên: `Switch Media Type`
3. Cấu hình 2 rules:
   - **Rule 0** (Text Only): 
     - Condition: `{{ $json.has_media }}` equals `false`
     - Output: 0
   - **Rule 1** (Has Media):
     - Condition: `{{ $json.has_media }}` equals `true`
     - Output: 1

### Bước 6: Nhánh TEXT ONLY (Output 0)
Thêm các nodes:
1. **Post Text Only** (Facebook Page node)
   - Resource: Group
   - Operation: createGroupPostByPage
   - Page ID: `{{ $json.page_id }}`
   - Group ID: `{{ $json.group_id }}`
   - Content Type: `text`
   - Text: `{{ $json.content }}`

2. **Log Success (Text)** - Copy từ "Log Success to Sheet"

3. **Wait Between Groups (Text)** - 30 seconds

4. Kết nối về "Split Groups Batch"

### Bước 7: Nhánh MEDIA (Output 1)
1. **Prepare Media Items** (Code node):
```javascript
const groupData = $input.first().json;
const mediaUrls = groupData.media_urls || [];

return mediaUrls.map((url, index) => ({
  json: {
    media_url: url,
    media_index: index,
    page_id: groupData.page_id,
    access_token: groupData.access_token,
    _group_data: groupData
  }
}));
```

2. **Split Media Batch** (SplitInBatches node)

3. **Convert File ID** (HTTP Request):
   - URL: `https://api.telegram.org/bot8326759079:AAGrogwPkaOEHSLuJR0xuuhNLdEehu_EQ2M/getFile?file_id={{ $json.media_url }}`

4. **Format Media URL** (Code):
```javascript
const BOT_TOKEN = '8326759079:AAGrogwPkaOEHSLuJR0xuuhNLdEehu_EQ2M';
const item = $input.first().json;

return {
  json: {
    ...item,
    media_download_url: `https://api.telegram.org/file/bot${BOT_TOKEN}/${item.result.file_path}`
  }
};
```

5. **Upload to Facebook** (HTTP Request):
   - Method: POST
   - URL: `https://graph.facebook.com/v24.0/{{ $json.page_id }}/photos`
   - Query params:
     - `url`: `{{ $json.media_download_url }}`
     - `published`: `false`
     - `access_token`: `{{ $json.access_token }}`

6. **Wait After Upload** - 2 seconds

7. Kết nối về "Split Media Batch" (loop)

8. **Collect Media IDs** (Code - sau khi Split Media Batch done):
```javascript
const uploadedItems = $input.all();
const groupData = uploadedItems[0].json._group_data;

const mediaIds = uploadedItems
  .map(item => item.json.id)
  .filter(id => id);

return [{
  json: {
    ...groupData,
    media_ids: mediaIds.join(',')
  }
}];
```

9. **Post With Media** (Facebook Page node):
   - Resource: Group
   - Operation: createGroupPostByPage
   - Page ID: `{{ $json.page_id }}`
   - Group ID: `{{ $json.group_id }}`
   - Content Type: `media`
   - Text: `{{ $json.content }}`
   - Media IDs: `={{ $json.media_ids }}`

10. **Log Success (Media)** - Copy từ "Log Success to Sheet"

11. **Wait Between Groups (Media)** - 30 seconds

12. Kết nối về "Split Groups Batch"

### Bước 8: Finalize
1. Kết nối cả 2 nhánh về "Split Groups Batch"
2. "Split Groups Batch" Done output → "Update Post Completed"
3. "Update Post Completed" → "Wait Between Posts" (180s)
4. "Wait Between Posts" → "Split Posts Batch"

### Bước 9: Test
1. Save workflow
2. Execute với test data
3. Check logs

## Tổng quan kết nối:
```
Switch Media Type
├─ Output 0 → Post Text Only → Log → Wait → Split Groups Batch
└─ Output 1 → Prepare Media → Split Media Batch 
              → Convert → Format → Upload → Wait → [loop back]
              → [Done] → Collect IDs → Post With Media → Log → Wait → Split Groups Batch
```

✅ Done!
