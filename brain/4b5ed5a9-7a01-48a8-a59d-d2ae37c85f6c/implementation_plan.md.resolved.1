# SORA Video Generation Workflow - Implementation Plan

Tạo workflow n8n để tự động hóa việc tạo video từ SORA (OpenAI) sử dụng phương pháp giả lập người dùng thông qua API endpoints.

## User Review Required

> [!IMPORTANT]
> **Authentication Token**: Token sẽ được lấy tự động từ extension Chrome khi người dùng truy cập trang SORA hoặc bấm vào profile. Extension sẽ webhook token qua n8n và lưu vào data table để workflow đọc.

> [!NOTE]
> **Testing Strategy**: Sẽ test Image to Video trước, sau đó mới implement Text to Video.

## Proposed Changes

### Component 1: Token Management System

Trước khi tạo workflow chính, cần setup hệ thống quản lý token:

#### [NEW] Chrome Extension để capture Bearer Token
- Extension lắng nghe các request đến `sora.chatgpt.com`
- Trích xuất Bearer token từ headers
- Webhook token qua n8n endpoint

#### [NEW] n8n Webhook nhận token
- Nhận token từ extension
- Lưu vào data table với timestamp
- Giữ token mới nhất

---

### Component 2: Image to Video Workflow

#### **Node 1: Manual Trigger / Schedule Trigger**
- Input parameters:
  - `imagePath`: Đường dẫn file ảnh local
  - `prompt`: Text mô tả video
  - `orientation`: `portrait` / `landscape` / `square` (default: `portrait`)
  - `n_frames`: Số frames (default: `300`)
  - `size`: `small` / `medium` / `large` (default: `small`)

---

#### **Node 2: Read Token từ Data Table**
- Đọc Bearer token mới nhất từ data table
- Verify token chưa expire

---

#### **Node 3: Read Binary File (Ảnh)**
- Đọc file ảnh từ `imagePath`
- Output: binary data

---

#### **Node 4: Upload Image**

**HTTP Request Node**

**Endpoint**: `https://sora.chatgpt.com/backend/project_y/file/upload`

**Method**: POST

**Authentication**: Bearer Token (từ Node 2)

**Body Type**: Form-Data
- `file`: {{$binary.data}} (binary data từ Node 3)
- `use_case`: `inpaint_safe`

**Response Extract**:
```json
{
  "file_id": "file_00000000fb5071f585fae749a9f5b38f",
  "asset_pointer": "sediment://file_00000000fb5071f585fae749a9f5b38f",
  "url": "https://...",
  "size": 82081
}
```

**Cần lưu**: `file_id`

---

#### **Node 5: Create Video Task**

**HTTP Request Node**

**Endpoint**: `https://sora.chatgpt.com/backend/nf/create`

**Method**: POST

**Authentication**: Bearer Token

**Headers**:
```json
{
  "Content-Type": "application/json"
}
```

**Body** (JSON):
```json
{
  "kind": "video",
  "prompt": "{{$node["Manual Trigger"].json["prompt"]}}",
  "title": null,
  "inpaint_items": [
    {
      "kind": "file",
      "file_id": "{{$node["Upload Image"].json["file_id"]}}"
    }
  ],
  "model": "sy_8",
  "n_frames": {{$node["Manual Trigger"].json["n_frames"] || 300}},
  "orientation": "{{$node["Manual Trigger"].json["orientation"] || "portrait"}}",
  "size": "{{$node["Manual Trigger"].json["size"] || "small"}}",
  "audio_caption": null,
  "audio_transcript": null,
  "cameo_ids": null,
  "cameo_replacements": null,
  "metadata": null,
  "remix_target_id": null,
  "storyboard_id": null,
  "style_id": null,
  "video_caption": null
}
```

**Response Extract**:
```json
{
  "id": "task_01kcxvng92fvka5x9r15f3atgd",
  "priority": 1,
  "rate_limit_and_credit_balance": {
    "rate_limit_reached": false,
    "access_resets_in_seconds": 86400,
    "estimated_num_videos_remaining": 10
  }
}
```

**Cần lưu**: 
- `id` (task_id)
- `rate_limit_and_credit_balance.estimated_num_videos_remaining`

---

#### **Node 6: Check Rate Limit (IF Node)**

**Condition**: `{{$node["Create Video Task"].json["rate_limit_and_credit_balance"]["estimated_num_videos_remaining"]}} > 0`

- **True**: Tiếp tục workflow
- **False**: Stop và thông báo hết quota

---

#### **Node 7: Loop - Poll Video Status**

**Loop with Wait Node**

**HTTP Request Node**

**Endpoint**: `https://sora.chatgpt.com/backend/nf/pending/v2`

**Method**: GET

**Authentication**: Bearer Token

**Response** (Array):
```json
[
  {
    "id": "task_01kcxvng92fvka5x9r15f3atgd",
    "status": "preprocessing",  // hoặc "processing", "completed"
    "prompt": "POV unboxing sản phẩm...",
    "title": null,
    "progress_pct": null,
    "generations": []  // Array rỗng khi đang processing
  }
]
```

**Logic**:
- GET status mỗi 15 giây
- Tìm task có `id` = task_id từ Node 5
- Kiểm tra `status`:
  - `preprocessing` hoặc `processing`: Tiếp tục poll
  - `completed`: Task xong, nhưng cần chờ thêm để video xuất hiện trong drafts
- Timeout: 10 phút

**Note**: Khi status = completed, `generations` vẫn có thể rỗng. Cần đợi thêm và check drafts.

---

#### **Node 8: Get Video URL from Drafts**

**HTTP Request Node**

**Endpoint**: `https://sora.chatgpt.com/backend/project_y/profile/drafts?limit=15`

**Method**: GET

**Authentication**: Bearer Token

**Response**:
```json
{
  "items": [
    {
      "id": "gen_01kcxvs35fesdt4994xkeyhvb2",
      "kind": "sora_draft",
      "task_id": "task_01kcxvng92fvka5x9r15f3atgd",
      "prompt": "POV unboxing sản phẩm...",
      "downloadable_url": "https://videos.openai.com/az/files/...",
      "download_urls": {
        "watermark": "https://...",
        "no_watermark": null,
        "endcard_watermark": null
      },
      "width": 352,
      "height": 640,
      "created_at": 1766233791.301746
    }
  ],
  "cursor": "..."
}
```

**Logic**:
- Tìm item có `task_id` = task_id từ Node 5
- Thường video mới nhất sẽ ở **items[0]** (index 0)
- Extract `downloadable_url` hoặc `download_urls.watermark`

---

#### **Node 9: Download Video**

**HTTP Request Node**

**Endpoint**: `{{$node["Get Video URL"].json["items"][0]["downloadable_url"]}}`

**Method**: GET

**Response Format**: Binary

**Output**: Binary video data

---

#### **Node 10: Save Video to Local**

**Write Binary File Node**

**File Path**: `I:/Workflow/n8n/Test/Sora AI/output/sora_{{$now.format("yyyyMMdd_HHmmss")}}.mp4`

**Data**: {{$binary.data}}

---

### Component 3: Text to Video Workflow

Tương tự Image to Video, nhưng có các khác biệt:

#### **Bỏ qua Node 3 và 4** (Read Binary File và Upload Image)

#### **Node 5 Modified: Create Video Task**

**Body** (JSON) - Không có `inpaint_items`:
```json
{
  "kind": "video",
  "prompt": "{{$node["Manual Trigger"].json["prompt"]}}",
  "title": null,
  "model": "sy_8",
  "n_frames": {{$node["Manual Trigger"].json["n_frames"] || 300}},
  "orientation": "{{$node["Manual Trigger"].json["orientation"] || "portrait"}}",
  "size": "{{$node["Manual Trigger"].json["size"] || "small"}}",
  "audio_caption": null,
  "audio_transcript": null,
  "cameo_ids": null,
  "cameo_replacements": null,
  "inpaint_items": null,
  "metadata": null,
  "remix_target_id": null,
  "storyboard_id": null,
  "style_id": null,
  "video_caption": null
}
```

**Các node còn lại giống hệt Image to Video workflow.**

---

## Implementation Notes

### Token Management
- Extension Chrome sẽ capture token khi user:
  - Truy cập `sora.chatgpt.com`
  - Click vào profile
  - Thực hiện bất kỳ action nào trigger API call
- Token được webhook qua n8n và store trong data table
- Workflow luôn đọc token mới nhất

### Video Status Polling
- Response từ `/backend/nf/pending/v2` trả về array tất cả pending tasks
- Cần filter theo `task_id` để tìm đúng task
- Video mới tạo thường ở index 0 của drafts array

### Storage
- Video sẽ được save vào local path: `I:/Workflow/n8n/Test/Sora AI/output/`
- Format tên file: `sora_YYYYMMDD_HHMMSS.mp4`

### Error Handling
1. **Rate Limit**: Check `estimated_num_videos_remaining` trước khi tạo video
2. **Token Expired**: Implement retry logic hoặc thông báo user cần refresh token
3. **Timeout**: Set timeout 10 phút cho polling. Nếu quá thời gian → fail và notify
4. **Video Not Found in Drafts**: Retry 3 lần với delay 5s giữa mỗi lần

## Verification Plan

### Test Image to Video:
1. Chuẩn bị 1 ảnh test trong folder
2. Set prompt: "POV unboxing sản phẩm. Video sắc nét, chân thật"
3. Run workflow
4. Verify:
   - Upload ảnh thành công → có `file_id`
   - Create task thành công → có `task_id`
   - Polling status cho đến khi completed
   - Get video URL từ drafts
   - Download video về local
   - Check video playback

### Test Text to Video:
1. Set prompt: "Tạo review sản phẩm khăn len quàng cổ"
2. Run workflow (không cần ảnh)
3. Verify tương tự như trên

### Test Token Management:
1. Verify extension capture được token
2. Verify token được lưu vào data table
3. Verify workflow đọc được token

### Test Error Scenarios:
1. Test khi hết quota (`estimated_num_videos_remaining` = 0)
2. Test khi token expired
3. Test khi timeout (giả lập bằng cách set timeout rất ngắn)
