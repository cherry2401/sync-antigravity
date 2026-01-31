# Code cho các nodes cần thay đổi

## 1. Node: "Combine Post + Groups Data" - SỬA LẠI

```javascript
// Combine post data with groups config - KHÔNG collect mediaIds nữa
const groupsConfig = $('Read Groups Config').all();
const postData = $('Parse Media & Groups').first().json;

// Normalize post group IDs
const postGroupIds = postData.group_ids
  .map(id => String(id).trim())
  .filter(id => id);

console.log('Post wants to go to groups:', postGroupIds);

// Filter active groups matching post's group_ids
const targetGroups = groupsConfig.filter(group => {
  const groupId = String(group.json['Group ID'] || '').trim();
  const isActive = group.json['Active'] === true || group.json['Active'] === 'TRUE';
  return groupId && postGroupIds.includes(groupId) && isActive;
});

if (targetGroups.length === 0) {
  throw new Error(`No active groups found for post ${postData.post_id}`);
}

// Return groups data WITH media_urls (not media_ids)
return targetGroups.map((group, index) => ({
  json: {
    post_id: postData.post_id,
    content: postData.content,
    media_urls: postData.media_urls,  // ← THAY ĐỔI: Pass URLs, not IDs
    media_count: postData.media_count,
    group_id: String(group.json['Group ID']),
    group_name: group.json['Group Name'],
    page_id: String(group.json['Page ID']),
    access_token: group.json['Access Token'],
    delay_seconds: parseInt(group.json['Delay (seconds)'] || '0') || 0,
    group_index: index + 1,
    total_groups: targetGroups.length
  }
}));
```

## 2. Node MỚI: "Prepare Media for This Group" (sau Wait Group Delay)

**Type**: Code Node

**Logic**:
```javascript
// Prepare media for CURRENT group only
const groupData = $input.first().json;
const mediaUrls = groupData.media_urls || [];

console.log(`Preparing media for group ${groupData.group_index}/${groupData.total_groups}`);
console.log(`Media URLs count: ${mediaUrls.length}`);

// If no media, skip upload
if (mediaUrls.length === 0) {
  return [{
    json: {
      ...groupData,
      skip_media_upload: true,
      media_ids: ''
    }
  }];
}

// Return each media URL as separate item for upload
return mediaUrls.map((url, index) => ({
  json: {
    media_url: url,
    media_index: index,
    // Keep group data for later merge
    _group_data: groupData
  }
}));
```

## 3. Node MỚI: "Split Media for This Group"

**Type**: SplitInBatches Node

**Config**:
- Batch Size: 1
- Options: Default

**Kết nối**:
- Input: Prepare Media for This Group
- Output: Convert File ID to URL (node đã có sẵn)

## 4. Node: "Upload Media to Facebook" - CẬP NHẬT

**QUAN TRỌNG**: Node này CẦN lấy Page ID và Access Token từ `_group_data`!

**Old code** (lines 208-238):
```javascript
// Lấy từ Read Groups Config1 (TOÀN CỤC - SAI!)
Page ID: {{ $('Read Groups Config1').first().json['Page ID'] }}
Access Token: {{ $('Read Groups Config1').first().json['Access Token'] }}
```

**NEW code**:
```javascript
// Lấy từ _group_data của GROUP HIỆN TẠI
method: POST
url: =https://graph.facebook.com/v24.0/{{ $json._group_data.page_id }}/photos

Query Parameters:
- url: ={{ $('Format File URL').item.json.media_url }}
- published: false
- access_token: ={{ $json._group_data.access_token }}
```

## 5. Node MỚI: "Collect Media IDs for Group" (sau Wait After Media Upload)

**Type**: Aggregate Node

**Config**:
- Aggregate: All Item Data
- Options: Default

**Logic**: Collect tất cả Media IDs đã upload cho group hiện tại

## 6. Node MỚI: "Format Media IDs for Group"

**Type**: Code Node

**Logic**:
```javascript
// Aggregate all uploaded Media IDs for THIS group
const uploadResults = $input.all();

// Get group data from first item
const groupData = uploadResults[0].json._group_data;

// Extract Media IDs from upload responses
const mediaIds = uploadResults
  .map(item => item.json.id)  // Facebook returns {id: "123456"}
  .filter(id => id);

console.log(`Group ${groupData.group_index}: Uploaded ${mediaIds.length} media`);
console.log(`Media IDs: ${mediaIds.join(',')}`);

return [{
  json: {
    ...groupData,
    media_ids: mediaIds.join(','),
    has_media: mediaIds.length > 0
  }
}];
```

## 7. Node: "Create Group Post using Page" - CẬP NHẬT INPUT

**Old**:
```
mediaIds: ={{ $json.media_ids }}
```

**New**: KHÔNG ĐỔI (vẫn lấy từ $json.media_ids, nhưng giờ media_ids là UNIQUE cho mỗi group)

## Kết nối các nodes (Connections)

```
Wait Group Delay
└─→ Prepare Media for This Group
    └─→ IF Has Media?
        ├─ YES → Split Media for This Group
        │         └─→ Convert File ID to URL
        │             └─→ Format File URL
        │                 └─→ Upload Media to Facebook (updated)
        │                     └─→ Wait After Media Upload
        │                         └─→ Split Media for This Group (loop back)
        │                             └─ Done → Collect Media IDs for Group
        │                                      └─→ Format Media IDs for Group
        │                                          └─→ Create Group Post using Page
        └─ NO → Create Group Post using Page (without media)
```

## Summary of Changes

| Node | Action | Reason |
|------|--------|--------|
| Combine Post + Groups Data | ✏️ Modified | Pass `media_urls` thay vì `media_ids` |
| Prepare Media for This Group | ➕ New | Prepare media cho TỪNG group |
| Split Media for This Group | ➕ New | Loop upload từng media |
| Upload Media to Facebook | ✏️ Modified | Lấy credentials từ `_group_data` |
| Collect Media IDs for Group | ➕ New | Aggregate IDs sau upload |
| Format Media IDs for Group | ➕ New | Format thành string cho group |

## Testing

Sau khi fix:
1. Tạo 1 post có media + 2 groups
2. Chạy workflow
3. Kiểm tra logs:
   - ✅ Group 1: Upload media → Get Media IDs → Post success
   - ✅ Group 2: Upload media (RIÊNG) → Get NEW Media IDs → Post success
