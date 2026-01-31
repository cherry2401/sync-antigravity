# Image-to-Video: Two-Phase Approach

## Problem
Direct processing of Telegram images fails at Google upload despite correct base64 and payload structure. URL-sourced images work perfectly.

## Solution: Split Into Two Phases

### **Phase 1: Upload Image (Immediate)**
**Trigger**: User sends image to Telegram

**Flow**:
1. `Telegram Trigger` → receive image
2. `Get File Info` → get file path
3. `Download Photo` → download binary
4. `Convert to Base64` → encode
5. `Upload Image` → **upload to Google immediately**
6. `Store Media ID` → **save `mediaId` to Data Table** with `chatId` as key
7. `Send Response` → "Image uploaded! Send your prompt."

**Key**: Image uploaded RIGHT AWAY, `mediaId` stored for later use.

---

### **Phase 2: Generate Video (On Prompt)**
**Trigger**: User sends text message

**Flow**:
1. `Telegram Trigger` → receive text
2. `Read Media ID` → **retrieve stored `mediaId`** using `chatId`
3. `Generate Video` → call I2V API with `mediaId` + prompt
4. `Wait` → `Check Status` → `Send Video`

**Key**: Use pre-uploaded `mediaId` with new prompt.

---

## Storage Requirement

**Data Table** structure:
| chatId | mediaId | timestamp |
|--------|---------|-----------|
| 12345 | abc-xyz | 2024-... |

**TTL**: Delete entries older than 1 hour (prevent stale data).

---

## User Experience

**Option A: Caption Flow (Fast Path)**
- User sends: Image + caption
- Workflow: Upload + generate in one go

**Option B: Two-Message Flow (Reliable)**
- User sends: Image → gets confirmation
- User sends: Prompt → workflow generates video

**Hybrid**: Try caption flow, fall back to two-message if no caption.

---

## Implementation Steps

1. **Add Data Table**: Column `chatId`, `mediaId`, `timestamp`
2. **Modify Telegram Trigger**: Detect image vs text
3. **Add Storage Node**: Write `mediaId` after upload
4. **Add Retrieval Node**: Read `mediaId` before generation
5. **Add Response Node**: Confirm upload to user

## Benefits
- ✅ Bypasses Telegram binary issues (upload happens immediately)
- ✅ Flexible UX (caption or separate messages)
- ✅ Reuses existing V3 upload logic
- ✅ State management isolates users

## Trade-offs
- ❌ Requires database/state storage
- ❌ Slightly more complex flow
- ❌ User must send two messages (unless caption provided)
