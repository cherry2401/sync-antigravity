# Auto-Sync Cookies on Page Visit + Deduplication

## Mục Tiêu
Tự động gửi cookies về webhook khi user truy cập Shopee, nhưng chỉ gửi khi cookies thay đổi (không trùng).

## Proposed Changes

### 1. Content Script - Detect Page Load

#### [NEW] [content.js](file:///d:/EXTENTIONS/custome-link_v2/content.js)

Content script chạy trên `shopee.vn/*` và `affiliate.shopee.vn/*`:

```javascript
// Run when page loads
(async function() {
  console.log('[Shopee Cookie Sync] Page loaded');
  
  // Wait a bit for cookies to be set
  setTimeout(async () => {
    // Send message to background to sync cookies
    chrome.runtime.sendMessage({
      action: 'auto_sync_cookies',
      url: window.location.href
    });
  }, 2000); // Wait 2 seconds after page load
})();
```

---

### 2. Background Script - Handle Auto-Sync

#### [MODIFY] [background.js](file:///d:/EXTENTIONS/custome-link_v2/background.js)

Thêm handler cho `auto_sync_cookies`:

```javascript
// Listen for auto-sync requests from content script
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === 'auto_sync_cookies') {
    handleAutoSync(sender.tab.id, request.url);
    sendResponse({ success: true });
  }
  // ... existing handlers
});

async function handleAutoSync(tabId, url) {
  try {
    // Check if auto-sync is enabled
    const settings = await chrome.storage.local.get(['auto_sync_enabled', 'n8n_webhook_url', 'last_cookie_hash']);
    
    if (!settings.auto_sync_enabled || !settings.n8n_webhook_url) {
      console.log('[Auto-Sync] Disabled or no webhook URL');
      return;
    }
    
    // Get cookies using DevTools Protocol
    await chrome.debugger.attach({ tabId }, '1.3');
    await chrome.debugger.sendCommand({ tabId }, 'Network.enable');
    
    const result = await chrome.debugger.sendCommand(
      { tabId }, 
      'Network.getCookies',
      { urls: [url] }
    );
    
    await chrome.debugger.detach({ tabId });
    
    if (!result || !result.cookies) {
      console.log('[Auto-Sync] No cookies found');
      return;
    }
    
    const cookieString = result.cookies.map(c => `${c.name}=${c.value}`).join('; ');
    
    // Calculate hash to check if cookies changed
    const currentHash = await hashString(cookieString);
    
    if (currentHash === settings.last_cookie_hash) {
      console.log('[Auto-Sync] Cookies unchanged, skipping sync');
      return;
    }
    
    console.log('[Auto-Sync] Cookies changed, syncing...');
    
    // Send to webhook
    const payload = {
      cookies: cookieString,
      timestamp: new Date().toISOString(),
      cookie_count: result.cookies.length,
      user_id: extractUserId(cookieString),
      source: 'chrome_extension_v2_auto',
      trigger: 'page_visit'
    };
    
    const response = await fetch(settings.n8n_webhook_url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    
    if (response.ok) {
      // Save new hash
      await chrome.storage.local.set({ last_cookie_hash: currentHash });
      console.log('[Auto-Sync] ✅ Synced successfully');
    }
    
  } catch (error) {
    console.error('[Auto-Sync] Error:', error);
  }
}

// SHA-256 hash function
async function hashString(str) {
  const encoder = new TextEncoder();
  const data = encoder.encode(str);
  const hashBuffer = await crypto.subtle.digest('SHA-256', data);
  const hashArray = Array.from(new Uint8Array(hashBuffer));
  return hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
}

function extractUserId(cookieString) {
  const match = cookieString.match(/SPC_U=([^;]+)/);
  return match ? match[1] : 'unknown';
}
```

---

### 3. Manifest Updates

#### [MODIFY] [manifest.json](file:///d:/EXTENTIONS/custome-link_v2/manifest.json)

Thêm content script:

```json
{
  "content_scripts": [
    {
      "matches": [
        "https://shopee.vn/*",
        "https://*.shopee.vn/*"
      ],
      "js": ["content.js"],
      "run_at": "document_end"
    }
  ]
}
```

---

### 4. UI Indicator (Optional)

#### [MODIFY] [sidebar.html](file:///d:/EXTENTIONS/custome-link_v2/sidebar.html)

Thêm badge/indicator hiển thị auto-sync status:

```html
<div style="margin-top: 12px;">
  <label style="display: flex; align-items: center; gap: 8px; cursor: pointer; font-weight: normal;">
    <input type="checkbox" id="autoSyncCheckbox" style="width: auto;" />
    <span>Tự động đồng bộ khi truy cập Shopee</span>
    <span id="autoSyncBadge" class="badge" style="display: none;">🟢 Active</span>
  </label>
  <p class="tip" style="margin-top: 4px;">💡 Chỉ gửi khi cookies thay đổi, không gửi lại cookies trùng</p>
</div>
```

---

## How It Works

### Flow Diagram

```
User visits Shopee
    ↓
Content Script detects page load (wait 2s)
    ↓
Send message to Background Script
    ↓
Background checks: auto_sync_enabled? webhook_url?
    ↓ Yes
Attach debugger → Get cookies → Detach
    ↓
Calculate SHA-256 hash of cookie string
    ↓
Compare with last_cookie_hash
    ↓ Different
Send to webhook + Save new hash
```

### Deduplication Logic

**Cookie Hash:**
- SHA-256 hash of entire cookie string
- Stored in `chrome.storage.local.last_cookie_hash`
- Only sync if hash different

**Benefits:**
- ✅ No duplicate webhook calls
- ✅ Bandwidth efficient
- ✅ N8n không bị spam

---

## User Experience

### Scenario 1: First Visit
1. User visits `affiliate.shopee.vn`
2. Auto-sync triggers (no previous hash)
3. Cookies sent to webhook
4. Hash saved

### Scenario 2: Same Cookies
1. User reloads page
2. Auto-sync checks hash
3. **Skips sync** (cookies unchanged)

### Scenario 3: Cookies Changed
1. User login/logout
2. Cookies different
3. New hash → Sync to webhook
4. Save new hash

### Scenario 4: Manual Sync
1. User clicks "Lấy Cookies Tự Động"
2. Manual sync **always runs** (không check hash)
3. Webhook receives cookies

---

## Settings

**Chrome Storage:**
```javascript
{
  "auto_sync_enabled": true/false,
  "n8n_webhook_url": "https://...",
  "last_cookie_hash": "abc123..."
}
```

**User Controls:**
- ✓ Checkbox "Tự động đồng bộ khi truy cập Shopee"
- Manual "Lấy Cookies Tự Động" button (bypass dedup)
- "Test Webhook" button

---

## Edge Cases

**1. Debugger Already Attached:**
- Try-catch with graceful fallback

**2. Tab Closed During Sync:**
- Background script handles detach errors

**3. Webhook Offline:**
- Log error, don't save hash
- Next visit will retry

**4. Multiple Tabs:**
- Each tab triggers independently
- Hash check prevents duplicates

---

## Verification Plan

### Testing

1. **First visit:**
   - Check console: "[Auto-Sync] Cookies changed, syncing..."
   - Verify webhook receives data
   - Check storage: `last_cookie_hash` saved

2. **Reload page:**
   - Check console: "[Auto-Sync] Cookies unchanged, skipping sync"
   - Verify NO webhook call

3. **Login/Logout:**
   - Cookies change
   - New sync triggered
   - New hash saved

4. **Manual button:**
   - Always works regardless of hash

---

## Notes

- Content script chỉ chạy trên Shopee domains
- Debugger warning sẽ hiện khi sync
- Auto-sync không block user interaction
- Manual sync vẫn hoạt động bình thường
