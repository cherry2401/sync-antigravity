# Vortex Terminal - Modern Windows Terminal Emulator

> A lightweight, modern Terminal Emulator for Windows using **Wails v2** (Go + React) with **ConPTY** integration, **SSH** support, and **xterm.js** rendering.

---

## Executive Summary

Xây dựng ứng dụng Terminal Emulator hiện đại cho Windows, tương tự Tabby/Hyper nhưng nhẹ hơn. Sử dụng Go cho backend với ConPTY API để xử lý I/O đúng chuẩn, React + xterm.js cho frontend.

### Tech Stack

| Layer | Technology |
|-------|------------|
| Framework | Wails v2 |
| Frontend | React + TailwindCSS |
| Terminal | xterm.js + addons |
| Backend | Go (Golang) |
| PTY | Windows ConPTY via `charmbracelet/x/conpty` |
| SSH | `golang.org/x/crypto/ssh` |

---

## User Review Required

> [!IMPORTANT]
> **Project Location**: Dự án sẽ được tạo tại `C:\Users\Cherry\.gemini\antigravity\scratch\vortex-terminal`
> 
> Anh có muốn đổi tên hoặc thư mục khác không?

> [!WARNING]
> **ConPTY Requirement**: ConPTY chỉ khả dụng từ Windows 10 version 1809 trở lên. Anh đang dùng Windows version nào?

---

## Proposed Changes

### 1. Project Scaffold

#### [NEW] Project Root Structure
```
vortex-terminal/
├── frontend/           # React app
│   ├── src/
│   │   ├── components/
│   │   │   ├── App.tsx
│   │   │   ├── TerminalView.tsx
│   │   │   ├── TabManager.tsx
│   │   │   ├── Titlebar.tsx
│   │   │   └── SSHModal.tsx
│   │   ├── hooks/
│   │   │   └── useTerminal.ts
│   │   ├── styles/
│   │   │   └── terminal.css
│   │   └── main.tsx
│   ├── index.html
│   └── package.json
├── internal/
│   ├── pty/
│   │   └── conpty.go      # ConPTY wrapper
│   └── ssh/
│       └── client.go      # SSH client
├── app.go                  # Wails app logic
├── main.go                 # Entry point
├── wails.json
└── go.mod
```

---

### 2. Backend Components

#### [NEW] [main.go](file:///C:/Users/Cherry/.gemini/antigravity/scratch/vortex-terminal/main.go)
- Entry point cho Wails app
- Configure frameless window
- Setup app context

#### [NEW] [app.go](file:///C:/Users/Cherry/.gemini/antigravity/scratch/vortex-terminal/app.go)
- **Core Methods to bind:**
  - `CreateLocalSession(shell string) string` - Spawn ConPTY với powershell/cmd
  - `CreateSSHSession(host, user, password, key string, port int) string` - SSH connection
  - `WriteToSession(sessionId, data string)` - Gửi input tới PTY
  - `ResizeSession(sessionId string, rows, cols int)` - Resize PTY
  - `CloseSession(sessionId string)` - Cleanup

#### [NEW] [internal/pty/conpty.go](file:///C:/Users/Cherry/.gemini/antigravity/scratch/vortex-terminal/internal/pty/conpty.go)
```go
// Key implementation using charmbracelet/x/conpty
package pty

import (
    "github.com/charmbracelet/x/conpty"
    "io"
)

type Session struct {
    ID     string
    ConPty *conpty.ConPty
    Stdin  io.Writer
    Stdout io.Reader
}

func NewSession(shell string, rows, cols int) (*Session, error) {
    // Create ConPTY with UTF-8 support
    cpty, err := conpty.New(cols, rows)
    if err != nil {
        return nil, err
    }
    
    // Spawn shell process
    if err := cpty.Spawn(shell); err != nil {
        return nil, err
    }
    
    return &Session{
        ID:     generateID(),
        ConPty: cpty,
        Stdin:  cpty,
        Stdout: cpty,
    }, nil
}
```

#### [NEW] [internal/ssh/client.go](file:///C:/Users/Cherry/.gemini/antigravity/scratch/vortex-terminal/internal/ssh/client.go)
- SSH client using `golang.org/x/crypto/ssh`
- Support password và key authentication
- PTY request cho interactive shell

---

### 3. Frontend Components

#### [NEW] [TerminalView.tsx](file:///C:/Users/Cherry/.gemini/antigravity/scratch/vortex-terminal/frontend/src/components/TerminalView.tsx)
```tsx
// Core terminal component
import { Terminal } from 'xterm';
import { FitAddon } from 'xterm-addon-fit';
import { WebglAddon } from 'xterm-addon-webgl';

// Features:
// - Initialize xterm.js with UTF-8 support
// - Connect to backend via Wails runtime events
// - Handle resize with FitAddon
// - onData -> Backend WriteToSession
// - Backend output -> terminal.write()
```

#### [NEW] [TabManager.tsx](file:///C:/Users/Cherry/.gemini/antigravity/scratch/vortex-terminal/frontend/src/components/TabManager.tsx)
- Quản lý multiple terminal tabs
- Add/Remove/Switch tabs
- Each tab = 1 session (local hoặc SSH)

#### [NEW] [Titlebar.tsx](file:///C:/Users/Cherry/.gemini/antigravity/scratch/vortex-terminal/frontend/src/components/Titlebar.tsx)
- Custom frameless titlebar
- Tabs inline với titlebar
- Min/Max/Close buttons

#### [NEW] [SSHModal.tsx](file:///C:/Users/Cherry/.gemini/antigravity/scratch/vortex-terminal/frontend/src/components/SSHModal.tsx)
- Form nhập SSH credentials
- Host, Port, User, Password/Key
- Save connections (optional)

---

### 4. Data Flow Architecture

```mermaid
sequenceDiagram
    participant User
    participant xterm.js
    participant Wails Runtime
    participant Go Backend
    participant ConPTY/SSH

    User->>xterm.js: Type "echo hello"
    xterm.js->>Wails Runtime: onData event
    Wails Runtime->>Go Backend: WriteToSession()
    Go Backend->>ConPTY/SSH: Write to stdin
    ConPTY/SSH-->>Go Backend: stdout output
    Go Backend-->>Wails Runtime: Emit "pty:output"
    Wails Runtime-->>xterm.js: EventsOn callback
    xterm.js-->>User: Display output
```

---

### 5. Critical Implementation Details

#### UTF-8 Vietnamese Support
```go
// In conpty.go - Enable UTF-8 for PowerShell
func (s *Session) enableUTF8() {
    // Send chcp 65001 to set UTF-8 codepage
    s.Stdin.Write([]byte("chcp 65001\r\n"))
}
```

#### Resize Handling
```tsx
// In TerminalView.tsx
const fitAddon = new FitAddon();
term.loadAddon(fitAddon);

const handleResize = () => {
    fitAddon.fit();
    const { rows, cols } = term;
    window.go.main.App.ResizeSession(sessionId, rows, cols);
};

window.addEventListener('resize', handleResize);
```

---

## Verification Plan

### Automated Tests

| Test | Command | Description |
|------|---------|-------------|
| Go Build | `go build -v ./...` | Verify Go code compiles |
| Frontend Build | `cd frontend && npm run build` | Verify React builds |
| Wails Build | `wails build` | Full production build |

### Manual Verification

1. **Start Dev Server**
   ```powershell
   cd C:\Users\Cherry\.gemini\antigravity\scratch\vortex-terminal
   wails dev
   ```

2. **Test Local Shell**
   - App window appears with terminal
   - Type commands, verify output displays

3. **Test Vietnamese (UTF-8)**
   ```powershell
   echo "Xin chào Việt Nam 🇻🇳"
   ```
   - Phải hiển thị đúng tiếng Việt có dấu

4. **Test Multi-Tab**
   - Click "+" to add new tab
   - Each tab has independent session

5. **Test SSH** (nếu có server để test)
   - Open SSH modal
   - Connect to remote server
   - Verify interactive shell works

6. **Test Resize**
   - Resize window
   - Text should reflow correctly, không bị vỡ

---

## Build Checklist (For Agent)

```
1. wails init -n vortex-terminal -t react
2. cd vortex-terminal
3. go get github.com/charmbracelet/x/conpty
4. go get golang.org/x/crypto/ssh
5. cd frontend && npm install xterm xterm-addon-fit xterm-addon-webgl
6. npm install -D tailwindcss postcss autoprefixer
7. npx tailwindcss init -p
8. Implement backend (app.go, internal/pty, internal/ssh)
9. Implement frontend components
10. wails dev (test)
11. wails build (production)
```

---

## Next Steps After Approval

```
1️⃣ Approve plan? → Tôi sẽ bắt đầu code ngay
2️⃣ Muốn xem UI mockup trước? → /visualize
3️⃣ Cần chỉnh sửa? → Cho tôi biết cần thay đổi gì
```
