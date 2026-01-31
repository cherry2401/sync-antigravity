# Extension Token Capture - Testing Guide

## Step 1: Reload Extension

1. Chrome → **Extensions** (chrome://extensions/)
2. Find **"API Key Capture Tool"**
3. Click **🔄 Reload**

---

## Step 2: Test Token Capture

1. **Mở VEO3**: https://labs.google/fx/tools/veo3
2. **F12** → Console tab
3. **Xem logs**:
   ```
   [VEO3 Token Capture] Started monitoring
   [VEO3 Token Capture] Token found: 03AFcWeA6Hg8pSMVmwOHWcXIQr...
   ```

4. **Click extension icon** → Xem logs trong popup

✅ Token được capture mỗi 10 giây tự động!

---

## Step 3: Verify Storage

**F12** → Console:
```javascript
chrome.storage.local.get(['veo3Token'], (res) => {
  console.log('Stored token:', res.veo3Token?.substring(0, 50) + '...');
});
```

---

## Step 4: Cleanup Workflow

### XÓA Nodes:
- ❌ IF Check Captcha Error
- ❌ Solve Captcha  
- ❌ Wait 15s
- ❌ Get Result
- ❌ Edit Fields1 (counter)
- ❌ Increment Counter
- ❌ IF Counter < 3

### GIỮ LẠI:
- ✅ Read Data
- ✅ Edit Fields
- ✅ Create VEO3

---

## Step 5: Update Workflow

### Edit Fields - Add Token Field

Thêm field mới:
```json
{
  "recaptchaToken": "{{ $('Read Data').first().json.VEO3_RecaptchaToken }}"
}
```

### Create VEO3 - JSON Body

Token đã có trong `$json` từ Edit Fields:
```javascript
{{
  JSON.stringify({
    "clientContext": {
      "sessionId": ";" + $json.sessionId,
      "projectId": $json.projectId,
      "tool": "PINHOLE",
      "userPaygateTier": "PAYGATE_TIER_TWO",
      "recaptchaToken": $json.recaptchaToken  // Từ Edit Fields
    },
    "requests": [{
      "aspectRatio": $json.aspectRatio,
      "seed": Math.floor(Math.random() * 10000),
      "textInput": { "prompt": $json.prompt },
      "videoModelKey": $json.videoModelKey,
      "metadata": { "sceneId": $json.sceneId }
    }]
  })
}}
```

---

## Step 6: Data Table

Extension **TỰ ĐỘNG** gửi token về webhook → Data Table update tự động!

Column: `VEO3_RecaptchaToken` = Token mới nhất

---

## Test Video Generation

1. **Gửi Telegram**: "test video"
2. **Workflow chạy**: Read Data → Edit Fields → Create VEO → Success! ✅
3. **No captcha solving** - Token từ browser 100% valid!

---

## Benefits

✅ **Miễn phí** - No OmoCaptcha cost  
✅ **Nhanh** - No solving delay  
✅ **100% success** - Token from real browser  
✅ **Auto-update** - Token refresh mỗi 10s
