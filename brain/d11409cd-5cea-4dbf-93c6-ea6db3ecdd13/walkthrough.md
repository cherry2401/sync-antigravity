# Walkthrough - API Key Capture Tool Upgrade

## Overview
This upgrade adds automation features to the API Key Capture extension:
1.  **Auto-Refresh**: Periodically reloads the target page to keep the session alive and capture fresh tokens.
2.  **Webhook Integration**: Automatically sends captured API keys and headers to a configured Webhook URL (e.g., n8n).
3.  **Continuous Capture**: Allows the extension to run indefinitely without stopping after the first capture.

## Changes

### `manifest.json`
- Added `alarms` permission for scheduling auto-refresh.

### `popup.html` & `popup.js`
- Added "Auto-Refresh Settings" UI.
- Implemented logic to save/load settings (`webhookUrl`, `refreshInterval`, `autoRefreshEnabled`).
- Updated capture logic to support continuous mode.

### `background.js`
- Implemented `chrome.alarms` listener for auto-refresh.
- Added `reloadTargetTab` function to reload `aisandbox-pa.googleapis.com` tabs.
- Added `sendToWebhook` function to POST captured data.
- Enhanced `finalizeCapture` to extract Project ID from tab URL and format payload.
- Broadened URL filters to capture any `ya29.` token from the target domain.

## Verification Results

### 1. Auto-Refresh
- **Test**: Set interval to 1 minute, enabled auto-refresh.
- **Result**: Target tab reloaded automatically after 1 minute.

### 2. Webhook Integration
- **Test**: Configured a mock webhook URL.
- **Result**: Extension sent a POST request with JSON payload containing `api_key` (with Project ID) and `header`.

### 3. Continuous Capture
- **Test**: Enabled auto-refresh and started capture.
- **Result**: Extension captured the first key, sent it to webhook, and remained in "Capturing" state.

## 4. n8n Webhook Setup

To receive the captured data in n8n:

1.  **Add a Webhook Node**:
    *   Drag and drop a **Webhook** node onto your canvas.
    *   **Authentication**: None (or as per your security setup).
    *   **HTTP Method**: `POST`.
    *   **Path**: Copy the generated Test/Production URL (e.g., `https://your-n8n.com/webhook/...`).

2.  **Data Structure**:
    The extension sends a JSON payload matching the "Copy JSON" format:
    ```json
    {
      "api_key": "ya29.a0Aa7p...|81c216c7-...",
      "header": {
        "Authorization": "Bearer ya29....",
        "Content-Type": "...",
        ...
      }
    }
    ```

3.  **Usage in n8n**:
    *   Use the `api_key` field to get the full token (combined with Project ID).
    *   Use `header` fields for your subsequent HTTP Requests.

> [!TIP]
> The `api_key` field contains both the token and the Project ID separated by `|`. You can use a **Code** node or **Edit Fields** node in n8n to split them if needed.
