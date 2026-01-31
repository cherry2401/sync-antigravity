# Workflow v4 - Fixes Applied

## ✅ Fixed: "No active groups found" Error

### Problem
Node `Combine Post + Groups Data` was using **WRONG input parsing**:
```javascript
// ❌ OLD (WRONG)
const postItems = $input.first().json;
const groupsItems = $input.last().json;
const allGroups = JSON.parse(groupsItems['Groups Config'] || '[]');
```

This assumed data came from `$input.first()` and `$input.last()`, but actually:
- Post data comes from `Parse Media & Groups` node
- Groups config comes from `Read Groups Config` node (Google Sheets → direct array)

### Solution
```javascript
// ✅ NEW (CORRECT)
const postData = $('Parse Media & Groups').first().json;
const allGroups = $('Read Groups Config').all();
```

### Key Changes
1. **Direct node reference**: Use `$('node_name')` instead of `$input`
2. **Correct data structure**: Groups from Google Sheets are already an array of objects with `.json` property
3. **Better error messages**: Now shows which groups are available vs which were requested

---

## 📋 Next Steps to Test

### 1. Import workflow vào n8n
- File: `Scheduled_Group_Post_v3.json`
- Workflow name: `Scheduled_Group_Post_v4`

### 2. Test với post có status "Pending"
Workflow sẽ:
1. ✅ Read Posts Schedule → Filter Pending → Split Posts Batch
2. ✅ Parse Media & Groups (lấy `group_ids` từ cột "Groups")
3. ✅ Read Groups Config (lấy tất cả groups)
4. ✅ **Combine Post + Groups Data** (filter groups theo `Active=TRUE` + match `Group ID`)
5. ✅ Switch Media Type → branch text/media
6. ✅ Route By Post Type → branch Group/Page

### 3. Kiểm tra Groups_Config sheet
Đảm bảo có ít nhất 1 row:
- ✅ `Active` = `TRUE`
- ✅ `Group ID` khớp với giá trị trong cột "Groups" của Posts_Schedule
- ✅ `Post Type` = "Group" hoặc "Page"

---

## 🔍 Example Data Flow

**Posts_Schedule:**
- Post ID: `POST_2026-01-02`
- Groups: `4721470959918861|4845136726244447` (pipe-separated)
- Status: `Pending`

**Groups_Config:**
| Group ID | Active | Post Type |
|----------|--------|-----------|
| 4721470959918861 | TRUE | Page |
| 4845136726244447 | FALSE | Group |

**Result:**
- Only `4721470959918861` will be processed (Active=TRUE)
- Will go to "Page" branch (Post Type = Page)
