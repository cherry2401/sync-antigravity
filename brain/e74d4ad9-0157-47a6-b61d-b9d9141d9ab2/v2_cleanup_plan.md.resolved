# Workflow V2 - Vấn đề và Giải pháp Clean Up

## Vấn đề hiện tại

### 1. **Logic SAI: Node "IF Skip Upload"**

**Hiện tại** (lines 28-35, 1347-1363):
```
IF Skip Upload (check skip_upload === true)
├─ TRUE → Create Group Post  ❌ SAI!
└─ FALSE → Prepare Post Data with Media  ❌ SAI!
```

**Lý do SAI**:
- `skip_upload = true` nghĩa là KHÔNG có media cần upload
- Nên khi TRUE, phải đi thẳng vào **Post (không media)**
- Khi FALSE, phải upload media trước

**Nhưng code hiện tại**:
- TRUE → Đi vào Create Post (OK)  
- FALSE → Đi vào "Prepare Post Data with Media" ??? (SAI - phải đi vào bước upload!)

### 2. **Vị trí SAI: Node "Construct Facebook URL"**

**Hiện tại** (line 225, position 8032,2240):
- Node này đứng Ở TỌA ĐỘ **TRƯỚC** "Create Group Post"
- Nhưng nó LẠI dùng output từ "Create Group Post" (line 222: `$input.first().json`)

→ **KHÔNG THỂ** lấy data từ node phía SAU!

### 3. **Flow đang bị rối**

```mermaid
graph TB
    A[Wait Group Delay] --> B[Prepare Group Media Items]
    B --> C[Split Group Media Batch]
    C --> D{IF Skip Upload}
    D -->|TRUE ???| E[Create Group Post]
    D -->|FALSE ???| F[Prepare Post Data with Media]
    F --> E
    C -->|Loop output| G[Convert File ID to URL]
    G --> H[Format File URL]
    H --> I[Upload to Facebook]
    I --> J[Wait After Upload]
    J --> C
    
    style D fill:#f99
    style E fill:#9f9
```

**Vấn đề**:
- ❌ "IF Skip Upload" có 2 outputs nhưng logic NGƯỢC
- ❌ Split Batch có 2 outputs:
  - Output 0 → "IF Skip Upload" (khi XONG loop)
  - Output 1 → "Convert File ID" (mỗi lần loop)
- ❌ THIẾU aggregate node để collect Media IDs sau khi upload xong!

## Giải pháp Clean

### Flow ĐÚNG nên là:

```mermaid
graph TB
    A[Wait Group Delay] --> B[Prepare Group Media Items]
    B --> C{IF Group Has Media?}
    
    C -->|NO| D[Prepare Post without Media]
    D --> E[Create Group Post]
    
    C -->|YES| F[Split Media Batch]
    F -->|Each item| G[Convert File ID to URL]
    G --> H[Format File URL]
    H --> I[Upload to Facebook]
    I --> J[Wait After Upload]
    J --> F
    F -->|Done| K[Collect Media IDs]
    K --> L[Prepare Post with Media]
    L --> E
    
    E --> M[Construct Facebook URL]
    M --> N{IF Success?}
    N -->|YES| O[Log Success]
    N -->|NO| P[Log Error]
```

### Chi tiết thay đổi

#### **XÓA nodes không cần:**
- ❌ "IF Skip Upload" (node sai logic)

#### **SỬA nodes hiện có:**

**1. Node "Prepare Group Media Items"** (line 72):
```javascript
// OLD: Return array hoặc skip flag
// NEW: Chỉ return flag check
const groupData = $input.first().json;
const mediaUrls = groupData.media_urls || [];

return [{
  json: {
    ...groupData,
    has_media: mediaUrls.length > 0,
    media_urls: mediaUrls
  }
}];
```

**2. SỬA node "IF Group Has Media"** (thay thế "IF Skip Upload"):
- Đổi tên từ "IF Skip Upload"
- Đổi condition: `$json.has_media === true` (thay vì `skip_upload`)
- Đổi output:
  - TRUE → Split Media Batch
  - FALSE → Prepare Post without Media

**3. THÊM node "Collect Media IDs"** (sau upload loop):
```javascript
// Collect all uploaded IDs
const uploadedItems = $input.all();
const groupData = $('Wait Group Delay').item.json;

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

**4. DI CHUYỂN "Construct Facebook URL"**:
- Từ position: `[8032, 2240]`
- Sang position SAU "Create Group Post": `[9680, 2240]`

#### **Connections MỚI:**

```javascript
"Wait Group Delay": {
  "main": [[{"node": "Prepare Group Media Items"}]]
},
"Prepare Group Media Items": {
  "main": [[{"node": "IF Group Has Media"}]]
},
"IF Group Has Media": {
  "main": [
    [{"node": "Prepare Post Data without Media"}],  // FALSE
    [{"node": "Split Group Media Batch"}]           // TRUE
  ]
},
"Split Group Media Batch": {
  "main": [
    [{"node": "Collect Media IDs"}],              // Loop done
    [{"node": "Convert Group File ID to URL"}]    // Each item
  ]
},
"Collect Media IDs": {
  "main": [[{"node": "Prepare Post Data with Media"}]]
},
"Prepare Post Data with Media": {
  "main": [[{"node": "Create Group Post using Page"}]]
},
"Prepare Post Data without Media": {
  "main": [[{"node": "Create Group Post using Page"}]]
},
"Create Group Post using Page": {
  "main": [[{"node": "Construct Facebook URL"}]]   // ← DI CHUYỂN
},
"Construct Facebook URL": {
  "main": [[{"node": "If"}]]
}
```

## Tóm tắt thay đổi

| Action | Node | Reason |
|--------|------|--------|
| ✏️ SỬA | IF Skip Upload → IF Group Has Media | Logic đúng |
| ✏️ SỬA | Prepare Group Media Items | Chỉ return flag |
| ➕ THÊM | Collect Media IDs | Aggregate IDs sau upload |
| 🔀 DI CHUYỂN | Construct Facebook URL | Phải SAU Create Post |
| ✏️ SỬA | Connections | Flow logic rõ ràng |

## Kết quả

✅ Flow rõ ràng, dễ hiểu
✅ Logic đúng 100%
✅ Mỗi group upload media RIÊNG
✅ Không bị duplicate Media ID
✅ Error handling đầy đủ
