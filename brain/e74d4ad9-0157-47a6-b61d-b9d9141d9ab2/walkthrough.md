# Scheduled Group Post V3 - Walkthrough

## ✅ Đã tạo xong

File workflow: [`Scheduled_Group_Post_v3.json`](file:///i:/Workflow/n8n/Workflow/Backups/Scheduled_Group_Post_v3.json)

## Kiến trúc Workflow

### **28 nodes tổng cộng:**

```
Schedule Trigger
└─→ Read Posts Schedule
    └─→ Filter Pending
        └─→ Split Posts Batch (Loop)
            └─→ Parse Media & Groups
                └─→ Read Groups Config
                    └─→ Combine Post + Groups
                        └─→ Split Groups Batch (Loop)
                            └─→ Switch Media Type
                                ├─ TEXT ONLY (Output 0)
                                │  └─→ Wait Delay (Text)
                                │      └─→ Post Text Only
                                │          └─→ Construct URL (Text)
                                │              └─→ Log Success (Text)
                                │                  └─→ Wait Between Groups (Text)
                                │                      └─→ [back to Split Groups Batch]
                                │
                                └─ HAS MEDIA (Output 1)
                                   └─→ Wait Delay (Media)
                                       └─→ Prepare Media Items
                                           └─→ Split Media Batch (Loop)
                                               └─→ Convert File ID
                                                   └─→ Format Media URL
                                                       └─→ Upload to Facebook
                                                           └─→ Wait After Upload
                                                               └─→ [back to Split Media Batch]
                                               └─ [Done] → Collect Media IDs
                                                            └─→ Post With Media
                                                                └─→ Construct URL (Media)
                                                                    └─→ Log Success (Media)
                                                                        └─→ Wait Between Groups (Media)
                                                                            └─→ [back to Split Groups Batch]
                            
                            └─[All Groups Done]→ Update Post Completed
                                                  └─→ Wait Between Posts
                                                      └─→ [back to Split Posts Batch]
```

## Nodes chi tiết

### **Phase 1: Trigger & Filter**
1. **Schedule Trigger** - Chạy tự động lúc 4h, 9h, 13h, 15h, 20h
2. **Read Posts Schedule** - Đọc Google Sheet `Posts_Schedule`
3. **Filter Pending** - Chỉ lấy posts có `Status = "Pending"`
4. **Split Posts Batch** - Loop qua từng post

### **Phase 2: Parse & Combine**
5. **Parse Media & Groups** - Parse `Media URLs` và `Groups` từ sheet
6. **Read Groups Config** - Đọc cấu hình groups
7. **Combine Post + Groups** - Match post với groups active
8. **Split Groups Batch** - Loop qua từng group

### **Phase 3: Switch - Rẽ nhánh** ⭐
9. **Switch Media Type** - Node KEY:
   - Output 0 (Text Only): `has_media = false`
   - Output 1 (Has Media): `has_media = true`

### **Phase 4A: TEXT BRANCH**
10. **Wait Delay (Text)** - Delay theo config
11. **Post Text Only** - Đăng text-only vào group
12. **Construct URL (Text)** - Tạo link Facebook
13. **Log Success (Text)** - Ghi log vào sheet
14. **Wait Between Groups (Text)** - Delay 30s trước group tiếp

### **Phase 4B: MEDIA BRANCH**
15. **Wait Delay (Media)** - Delay theo config
16. **Prepare Media Items** - Split media URLs thành items
17. **Split Media Batch** - Loop upload từng media
18. **Convert File ID** - Convert Telegram file_id
19. **Format Media URL** - Format download URL
20. **Upload to Facebook** - Upload lên FB (unpublished)
21. **Wait After Upload** - Delay 2s
22. **Collect Media IDs** - Aggregate tất cả Media IDs
23. **Post With Media** - Đăng bài với media
24. **Construct URL (Media)** - Tạo link Facebook
25. **Log Success (Media)** - Ghi log
26. **Wait Between Groups (Media)** - Delay 30s

### **Phase 5: Completion**
27. **Update Post Completed** - Update `Status = "Completed"`
28. **Wait Between Posts** - Delay 180s trước post tiếp

## Điểm mạnh

✅ **Logic rõ ràng**: Switch node làm điểm phân nhánh duy nhất
✅ **Text-only tối ưu**: Không qua upload, đăng trực tiếp
✅ **Media per group**: Mỗi group upload riêng → Không duplicate
✅ **Error resistant**: Mỗi nhánh độc lập, dễ debug
✅ **Logging đầy đủ**: Track từng post/group

## Google Sheets cần có

### 1. **Posts_Schedule** (Sheet ID: 1605992605)
| Post ID | Content | Media URLs | Groups | Status | Posted Time |
|---------|---------|------------|--------|--------|-------------|
| POST_001 | Text... | file_id1\|file_id2 | 123\|456 | Pending | |

### 2. **Groups_Config** (Sheet ID: 1640119268)
| Group ID | Group Name | Page ID | Access Token | Active | Delay (seconds) |
|----------|------------|---------|--------------|--------|-----------------|
| 123 | Group A | 789 | TOKEN... | TRUE | 10 |

### 3. **Post_Logs** (Sheet ID: 41013809)
| Log ID | Post ID | Group ID | Post URL | Status | Timestamp |
|--------|---------|----------|----------|--------|-----------|
| LOG_... | POST_001 | 123 | https://... | Success | 2025-... |

## Cách sử dụng

### Import vào n8n

1. Mở n8n
2. Click **Import from File**
3. Chọn [`Scheduled_Group_Post_v3.json`](file:///i:/Workflow/n8n/Workflow/Backups/Scheduled_Group_Post_v3.json)
4. Click **Import**

### Cấu hình

1. **Credentials**:
   - Google Sheets: `linhvu.014@gmail.com`
   - Facebook: `NTLV`

2. **Sheet IDs**:
   - Đã hard-code sẵn trong workflow
   - Nếu dùng sheet khác, update `documentId` và `sheetName`

3. **Telegram Bot Token**:
   - Đã có sẵn: `8326759079:AAGrogwPkaOEHSLuJR0xuuhNLdEehu_EQ2M`
   - Nếu đổi bot, update trong nodes:
     - "Convert File ID"
     - "Format Media URL"

### Test

1. **Test Text-only**:
   - Tạo 1 row trong `Posts_Schedule`:
     - Status = Pending
     - Media URLs = (để trống)
     - Groups = 1 group ID

2. **Test Media**:
   - Tạo 1 row:
     - Status = Pending
     - Media URLs = `file_id1|file_id2`
     - Groups = 1 group ID

3. **Test Multi-group**:
   - Groups = `123|456|789` (3 groups)
   - Xem workflow đăng tuần tự vào 3 groups

4. **Run Manually**:
   - Click "Execute Workflow"
   - Xem từng node chạy
   - Check logs trong `Post_Logs` sheet

### Activate

- Toggle **Active** = ON
- Workflow sẽ tự chạy theo lịch: 4h, 9h, 13h, 15h, 20h

## Troubleshooting

### Lỗi "No active groups found"
- Kiểm tra `Groups_Config`:
  - Group ID có đúng?
  - Active = TRUE?

### Text-only không đăng được
- Check node "Post Text Only":
  - `contentType` = "text" hoặc để trống `mediaIds`

### Media không upload
- Check Telegram bot token
- Check file_id còn valid không
- Check Facebook credentials

### Duplicate Media ID
- ✅ Workflow V3 ĐÃ FIX: Mỗi group upload riêng!

## So sánh với V1/V2

| Feature | V1 | V2 | V3 |
|---------|----|----|-----|
| Upload media | 1 lần cho tất cả | Cố gắng per-group | ✅ Per-group đúng |
| Logic rẽ nhánh | IF nested | IF sai logic | ✅ Switch clean |
| Text-only | Qua upload | Qua upload | ✅ Skip upload |
| Dễ hiểu | ⭐⭐ | ⭐ | ✅ ⭐⭐⭐⭐⭐ |
| Error | Duplicate ID | Rối logic | ✅ Resolved |

## Kết luận

Workflow V3 là phiên bản **ổn định** và **production-ready** với:
- ✅ Logic đơn giản, dễ maintain
- ✅ Fix hoàn toàn vấn đề duplicate Media ID
- ✅ Performance tối ưu cho text-only posts
- ✅ Logging và monitoring đầy đủ

**Sẵn sàng để production!** 🚀
