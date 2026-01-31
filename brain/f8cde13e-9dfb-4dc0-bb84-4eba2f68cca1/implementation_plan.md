# Browser-Based VEO3 API Calls

## Problem

Token từ browser **chỉ valid khi browser gọi API**. n8n server gọi → Token invalid!

## Solution: Browser Gọi API

```
Telegram → n8n Webhook Trigger → Gửi data về Extension
                                          ↓
                                    Extension gọi VEO3 API (có token hợp lệ)
                                          ↓
                                    Nhận response
                                          ↓
                                    POST result về n8n Webhook
                                          ↓
                                    n8n xử lý video
```

---

## Implementation

### 1. n8n Workflow

**Flow mới**:
```
Telegram Trigger → Webhook (gửi command về extension) → Webhook (nhận result) → Process video
```

#### Webhook 1: Send Command to Extension
- **Method**: GET
- **Path**: `/veo3-command`
- **Response**: JSON with prompt, aspectRatio, model
- Extension polling webhook này để lấy command

#### Webhook 2: Receive Result
- **Method**: POST  
- **Path**: `/veo3-result`
- **Body**: Video result from API
- Xử lý như cũ (download, send Telegram)

---

### 2. Extension Update

**File**: `background.js`

```javascript
// Poll for commands from n8n
async function pollForCommands() {
  const webhookUrl = 'N8N_WEBHOOK_URL/veo3-command';
  
  try {
    const response = await fetch(webhookUrl);
    const command = await response.json();
    
    if (command.prompt) {
      console.log('[VEO3] New command:', command);
      await executeVEO3Request(command);
    }
  } catch (e) {
    console.log('[VEO3] No command');
  }
}

// Execute VEO3 API call from browser
async function executeVEO3Request(command) {
  // Get latest token
  const { veo3Token } = await chrome.storage.local.get(['veo3Token']);
  
  // Get API key from storage
  const { apiKey, projectId } = await chrome.storage.local.get(['apiKey', 'projectId']);
  
  const sessionId = ';' + Date.now();
  const sceneId = 'scene_' + Math.random().toString(36).substr(2, 9);
  
  const body = {
    clientContext: {
      sessionId: sessionId,
      projectId: projectId,
      tool: 'PINHOLE',
      userPaygateTier: 'PAYGATE_TIER_TWO',
      recaptchaToken: veo3Token
    },
    requests: [{
      aspectRatio: command.aspectRatio || 'VIDEO_ASPECT_RATIO_LANDSCAPE',
      seed: Math.floor(Math.random() * 10000),
      textInput: { prompt: command.prompt },
      videoModelKey: command.videoModelKey || 'veo_3_1_t2v_fast_ultra',
      metadata: { sceneId: sceneId }
    }]
  };
  
  console.log('[VEO3] Making API call...');
  
  try {
    const response = await fetch('https://aisandbox-pa.googleapis.com/v1/media/CAMaJ...', {
      method: 'POST',
      headers: {
        'authorization': 'Bearer ' + apiKey,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(body)
    });
    
    const result = await response.json();
    console.log('[VEO3] API response:', result);
    
    // Send result to n8n
    await sendResultToN8N(result, command);
    
  } catch (e) {
    console.error('[VEO3] API error:', e);
    await sendErrorToN8N(e, command);
  }
}

// Send result back to n8n
async function sendResultToN8N(result, command) {
  const webhookUrl = 'N8N_WEBHOOK_URL/veo3-result';
  
  await fetch(webhookUrl, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      success: true,
      result: result,
      command: command,
      timestamp: new Date().toISOString()
    })
  });
  
  console.log('[VEO3] Result sent to n8n');
}

// Poll every 5 seconds
setInterval(pollForCommands, 5000);
```

---

## Benefits

✅ **Token hợp lệ** - Browser gọi API  
✅ **Không captcha errors**  
✅ **n8n chỉ xử lý kết quả** - Đơn giản hơn  

## Drawbacks

⚠️ Browser **phải mở** VEO3 page  
⚠️ Extension **phải có API key & Project ID**  
⚠️ Polling mỗi 5s (có thể optimize)

---

## Next Steps

1. Tạo 2 webhooks trong n8n
2. Update extension code
3. Test workflow
