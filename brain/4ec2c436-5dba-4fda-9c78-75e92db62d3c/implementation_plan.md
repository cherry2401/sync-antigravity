# Fixing Watcher Stability via AppData Migration

The HMR loop persists because Vite's watcher is extremely sensitive to changes within the project root. Moving files to `/data` and ignoring them works in some environments but can be flaky. The most robust solution is to move these transient communication files completely outside the project directory into the system's `AppData` folder.

## Proposed Changes

### 1. Update [main.ts](file:///f:/Python/OpenSSH/clawdbot-client/electron/main.ts) & [preload.ts](file:///f:/Python/OpenSSH/clawdbot-client/electron/preload.ts)
- Expose a new API `window.electronAPI.getCommDir()` that returns the path to a `comm-data` folder inside Electron's `userData` path.
- This path will be something like `C:\Users\<User>\AppData\Roaming\clawdbot-client\comm-data`.

### 2. Update [browserRelay.ts](file:///f:/Python/OpenSSH/clawdbot-client/electron/services/browserRelay.ts)
- Use the new `userData` based path for `CDP_INBOUND_FILE` and `CDP_OUTBOUND_FILE`.
- Ensure the directory is created on startup.

### 3. Update [App.tsx](file:///f:/Python/OpenSSH/clawdbot-client/src/App.tsx)
- Dynamically fetch the communication directory on mount.
- Move the "Watcher Active" `system` message logic to the `init` function to ensure it happens *after* the session is loaded/created, avoiding race conditions.
- Update the inbound watcher to use the new path.

### 4. Update [ChatPanel.tsx](file:///f:/Python/OpenSSH/clawdbot-client/src/components/ChatPanel.tsx) & [ChopperLogs.tsx](file:///f:/Python/OpenSSH/clawdbot-client/src/components/ChopperLogs.tsx)
- Update `OUTBOUND_FILE` and `LOG_FILE_PATH` to use the dynamic `commDir`.

### 5. Cleanup
- Delete the local `data/` folder from the project root.
- Update [CHOPPER_GUIDE.md](file:///f:/Python/OpenSSH/clawdbot-client/CHOPPER_GUIDE.md) with instructions on how to find the new AppData path.

## Verification Plan

### Manual Verification
- Restart the App.
- Verify the "Inbound Watcher Active" message appears in the chat.
- Check the console: `[App] Starting global inbound file watcher` should appear exactly once.
- Change tabs multiple times: The watcher must NOT stop.
- Simulate a Chopper message by writing to the file in the `AppData` path and confirm it appears in the UI.
- Verify that editing files in the UI does NOT trigger an App reload.
