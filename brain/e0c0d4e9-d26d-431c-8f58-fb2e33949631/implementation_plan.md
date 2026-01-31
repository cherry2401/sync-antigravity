# Goal: Fix Logo in clawdbot-client

The goal is to replace the placeholder `Zap` icon in the title bar with the actual project logo.

## Proposed Changes

### [Component Name] clawdbot-client

#### [NEW] [logo.png](file:///f:/Python/OpenSSH/clawdbot-client/src/assets/logo.png)
- Added the logo asset to the `src/assets` folder.

#### [MODIFY] [TitleBar.tsx](file:///f:/Python/OpenSSH/clawdbot-client/src/components/TitleBar.tsx)
- Import `logo.png`.
- Replace `<Zap />` with an `<img>` tag.
- Apply styling to ensure the logo fits well.

## Verification Plan

### Manual Verification
- Start the app using `npm run electron:dev`.
- Observe the title bar to confirm the logo is displayed correctly.
- Ensure the logo doesn't disrupt the title bar layout.
