# Auto-Sync Cookies on Page Visit - Walkthrough

## ✅ Tính Năng Mới

**Auto-sync khi truy cập Shopee + Deduplication!**

Extension giờ tự động gửi cookies về N8n mỗi khi bạn truy cập Shopee, **nhưng chỉ gửi khi cookies thay đổi**.

## 🔧 Cách Hoạt Động

### Flow Diagram

```
User visits shopee.vn or affiliate.shopee.vn
    ↓
Content script detects (wait 2s)
    ↓
Send message to Background
    ↓
Check: auto_sync_enabled? webhook_url?
    ↓ Yes
Get cookies via DevTools Protocol
    ↓
Calculate SHA-256 hash of cookie string
    ↓
Compare with last saved hash
    ↓
Different? → Send to webhook + Save new hash
Same? → Skip (no webhook call)
```

### Deduplication Logic

**SHA-256 Hash:**
- Hash toàn bộ cookie string
- Lưu trong `chrome.storage.local.last_cookie_hash`
- **Chỉ sync khi hash khác**

**Benefits:**
- ✅ Không spam webhook
- ✅ Bandwidth efficient
- ✅ Chỉ sync khi thực sự cần

## 📁 Files Changed

### 1. [content.js](file:///d:/EXTENTIONS/custome-link_v2/content.js) - NEW

Chạy trên mọi trang Shopee, gửi message sau 2s:

```javascript
chrome.runtime.sendMessage({
  action: 'auto_sync_cookies',
  url: window.location.href
});
```

### 2. [background.js](file:///d:/EXTENTIONS/custome-link_v2/background.js) - MODIFIED

**Added:**
- `handleAutoSync()` - Main auto-sync handler
- `hashString()` - SHA-256 hashing
- `extractUserIdFromCookie()` - Extract SPC_U

**Logic:**
1. Check settings (enabled? webhook?)
2. Get cookies via DevTools Protocol
3. Hash cookie string
4. Compare with last hash
5. If different → Sync + Save hash
6. If same → Skip

### 3. [manifest.json](file:///d:/EXTENTIONS/custome-link_v2/manifest.json) - MODIFIED

Added content_scripts:
```json
"content_scripts": [{
  "matches": ["https://shopee.vn/*", "https://*.shopee.vn/*"],
  "js": ["content.js"],
  "run_at": "document_end"
}]
```

### 4. [sidebar.html](file:///d:/EXTENTIONS/custome-link_v2/sidebar.html) - MODIFIED

Updated checkbox label:
- "Tự động đồng bộ **khi truy cập Shopee**"
- Tooltip: "Chỉ gửi khi cookies thay đổi"

## 🧪 Testing

### Bước 1: Reload Extension
1. `chrome://extensions/`
2. Reload "Shopee Link Converter V2"

### Bước 2: Enable Auto-Sync
1. Extension → Settings
2. Nhập webhook URL
3. ✓ Check "Tự động đồng bộ khi truy cập Shopee"
4. Lưu

### Bước 3: Test First Visit
1. Mở https://affiliate.shopee.vn
2. **Mở Console (F12)**
3. Xem logs:
   ```
   [Shopee Cookie Sync] Page loaded
   [Auto-Sync] Triggered for: https://...
   [Auto-Sync] Current hash: abc123...
   [Auto-Sync] Last hash: none
   [Auto-Sync] 🔄 Cookies changed, syncing...
   [Auto-Sync] ✅ Synced successfully
   ```
4. Check n8n webhook received data

### Bước 4: Test Deduplication
1. **Reload trang** (F5)
2. Xem console:
   ```
   [Auto-Sync] Current hash: abc123...
   [Auto-Sync] Last hash: abc123...
   [Auto-Sync] ⏭️ Cookies unchanged, skipping sync
   ```
3. **No webhook call** (check n8n - không có request mới)

### Bước 5: Test Cookie Change
1. Login/logout hoặc clear cookies
2. Reload trang
3. Console sẽ show:
   ```
   [Auto-Sync] 🔄 Cookies changed, syncing...
   ```
4. New webhook call với cookies mới

## 📊 Webhook Data

```json
{
  "cookies": "SPC_F=...; SPC_ST=...",
  "timestamp": "2025-12-24T13:22:58+07:00",
  "cookie_count": 23,
  "user_id": "1271922156",
  "source": "chrome_extension_v2_auto",
  "trigger": "page_visit"
}
```

**Fields:**
- `source`: "chrome_extension_v2_**auto**" (khác với manual)
- `trigger`: "page_visit" (biết đây là auto-sync)

## 🎯 Use Cases

### Scenario 1: First Visit
- Visit Shopee → Auto-sync triggers
- No previous hash → Send webhook
- Save hash

### Scenario 2: Reload Page
- Same cookies → Skip sync
- No webhook call

### Scenario 3: Login/Logout
- Cookies changed → New hash
- Webhook called with new cookies

### Scenario 4: Multiple Tabs
- Each tab triggers independently
- Hash check prevents duplicates

### Scenario 5: Manual Button
- "Lấy Cookies Tự Động" **always works**
- Bypasses hash check

## ⚠️ Lưu Ý

**Debugger Warning:**
- Mỗi khi auto-sync sẽ hiện "Debugger has been detected"
- Chỉ ~ 1-2 giây, tự động biến mất
- Hoàn toàn an toàn

**Performance:**
- Content script chỉ ~1KB
- Auto-sync chạy sau 2s load
- Không ảnh hưởng page performance

**Storage:**
- `last_cookie_hash`: SHA-256 string (64 chars)
- Minimal storage usage

## 🎓 Kết Luận

Extension V2 giờ có:
- ✅ Auto-sync khi truy cập Shopee
- ✅ SHA-256 hash deduplication
- ✅ Chỉ sync khi cookies thay đổi
- ✅ Manual button vẫn hoạt động
- ✅ Console logs chi tiết

**Hoàn toàn tự động, không spam webhook!** 🚀
