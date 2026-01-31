# VEO3 Token Service - Complete Implementation

## Giải Thích: recaptchaToken Là Gì?

### Token `03APcPBne...` Là:
- **Proof of Humanity** từ Google reCAPTCHA
- Chứng minh "bạn là người, không phải bot"
- Format: `03` (v3) + encrypted data
- **Validity**: 2-5 phút
- **Size**: ~500+ characters

### Tại Sao Workflow Cần Token?

Google VEO3 API yêu cầu:
```json
{
  "clientContext": {
    "recaptchaToken": "03APcPBne..." ← BẮT BUỘC
  }
}
```

**Không có token** → ❌ "reCAPTCHA evaluation failed"
**Có token** → ✅ Video được tạo

---

## Setup Files

### package.json
```json
{
  "name": "veo-token-service",
  "version": "1.0.0",
  "description": "Capture recaptchaToken from VEO3 browser",
  "dependencies": {
    "express": "^4.18.2",
    "puppeteer": "^21.6.0"
  }
}
```

### server.js
```javascript
const express = require('express');
const puppeteer = require('puppeteer');
const app = express();

// Token cache
let cachedToken = null;
let tokenExpiry = 0;
let isGenerating = false;

/**
 * Capture recaptchaToken from real browser
 * User cần tạo 1 video trên VEO3 để trigger token generation
 */
async function captureTokenFromVEO3() {
  const browser = await puppeteer.launch({ 
    headless: false, // Show browser
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });
  
  const page = await browser.newPage();
  let capturedToken = null;
  
  // Intercept network requests
  await page.setRequestInterception(true);
  
  page.on('request', request => request.continue());
  
  page.on('requestfinished', async request => {
    const url = request.url();
    
    // Check for video generation endpoints
    if (url.includes('batchAsyncGenerateVideoText') || 
        url.includes('batchAsyncGenerateVideoStartAndEndImage')) {
      
      const postData = request.postData();
      if (postData) {
        try {
          const body = JSON.parse(postData);
          
          if (body.clientContext?.recaptchaToken) {
            console.log('✅ Token captured!');
            console.log('Preview:', body.clientContext.recaptchaToken.substring(0, 50) + '...');
            capturedToken = body.clientContext.recaptchaToken;
          }
        } catch (e) {}
      }
    }
  });
  
  console.log('🌐 Opening VEO3...');
  await page.goto('https://labs.google/fx/tools/veo3', {
    waitUntil: 'networkidle2',
    timeout: 60000
  });
  
  console.log('✋ WAITING: Create a video on the browser!');
  
  // Wait max 3 minutes
  const startTime = Date.now();
  while (!capturedToken && (Date.now() - startTime < 180000)) {
    await new Promise(r => setTimeout(r, 1000));
  }
  
  await browser.close();
  
  if (!capturedToken) {
    throw new Error('No token captured. Did you create a video?');
  }
  
  return capturedToken;
}

// API: Get Token
app.get('/get-token', async (req, res) => {
  console.log('\n📥 Token requested');
  
  // Return cached token if valid
  if (cachedToken && Date.now() < tokenExpiry) {
    const expiresIn = Math.floor((tokenExpiry - Date.now()) / 1000);
    console.log(`✅ Cached token (${expiresIn}s left)`);
    
    return res.json({ 
      success: true,
      token: cachedToken,
      from: 'cache',
      expiresIn
    });
  }
  
  if (isGenerating) {
    return res.status(503).json({ 
      success: false,
      error: 'Generating token, please wait...' 
    });
  }
  
  isGenerating = true;
  console.log('🔄 Fetching new token...');
  
  try {
    const token = await captureTokenFromVEO3();
    
    // Cache 3 minutes
    cachedToken = token;
    tokenExpiry = Date.now() + 3 * 60 * 1000;
    
    console.log('✅ Token cached');
    
    res.json({ 
      success: true,
      token,
      from: 'fresh',
      expiresIn: 180
    });
    
  } catch (error) {
    console.error('❌ Error:', error.message);
    res.status(500).json({ 
      success: false,
      error: error.message 
    });
  } finally {
    isGenerating = false;
  }
});

// Health check
app.get('/health', (req, res) => {
  res.json({ 
    status: 'ok',
    hasCache: !!cachedToken,
    cacheValid: cachedToken && Date.now() < tokenExpiry,
    expiresIn: cachedToken && Date.now() < tokenExpiry ?
      Math.floor((tokenExpiry - Date.now()) / 1000) : 0
  });
});

const PORT = 3000;
app.listen(PORT, () => {
  console.log('\n🚀 Token Service Running!');
  console.log('━'.repeat(40));
  console.log(`Get Token: http://localhost:${PORT}/get-token`);
  console.log(`Health:    http://localhost:${PORT}/health`);
  console.log('━'.repeat(40) + '\n');
});
```

---

## Test Locally

### 1. Install
```bash
mkdir veo-token-service
cd veo-token-service
# Copy package.json và server.js vào folder
npm install
```

### 2. Run
```bash
node server.js
```

Output:
```
🚀 Token Service Running!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Get Token: http://localhost:3000/get-token
Health:    http://localhost:3000/health
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 3. Request Token
```bash
# Terminal mới
curl http://localhost:3000/get-token
```

**Browser tự mở** → VEO3 loaded → **BẠN TẠO VIDEO** → Token captured!

Response:
```json
{
  "success": true,
  "token": "03APcPBneAwGcJC-Y9ubb...",
  "from": "fresh",
  "expiresIn": 180
}
```

### 4. Test Cache
```bash
curl http://localhost:3000/get-token
```

Response (instant):
```json
{
  "success": true,
  "token": "03APcPBneAwGcJC-Y9ubb...",
  "from": "cache",
  "expiresIn": 165
}
```

---

## n8n Workflow Integration

### HTTP Request Node
- **Method**: GET
- **URL**: `http://localhost:3000/get-token`
- **Timeout**: 60000

### Use Token in Create VEO3
```json
{
  "clientContext": {
    "recaptchaToken": "{{ $json.token }}",
    ...
  }
}
```

---

## Deploy to Alpine Server (Later)

Sau khi test local OK, deploy lên server n8n với Docker như đã plan!
