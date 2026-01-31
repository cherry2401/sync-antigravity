# Hướng dẫn Cài đặt Clawdbot Gateway (Windows Service với NSSM)

## 📋 Tổng quan
Hướng dẫn cài đặt Clawdbot Gateway chạy dưới dạng **Windows Service** thực thụ bằng công cụ **NSSM**.
Phương pháp này ưu việt hơn Task Scheduler vì:
- ✅ **Tự động khởi động** cùng Windows (trước cả khi login).
- ✅ **Tự động restart** nếu ứng dụng bị crash.
- ✅ **Chạy ẩn hoàn toàn** (không bao giờ hiện cửa sổ CMD).
- ✅ **Ổn định cao**, không bị ảnh hưởng khi Sleep/Wake máy.

---

## 🛠 Bước 1: Cài đặt & Cấu hình

Tải file script cấu hình tự động dưới đây và chạy với quyền Administrator.

**Tạo file `C:\Scripts\setup-clawdbot-service.ps1`:**

```powershell
# 1. Cài đặt NSSM qua Winget (nếu chưa có)
winget install NSSM.NSSM --accept-package-agreements --accept-source-agreements

# Tìm đường dẫn NSSM
$nssmParams = @("nssm", "install", "ClawdbotGateway", "C:\Program Files\nodejs\node.exe", "scripts/run-node.mjs gateway")
$nssmPath = Get-Command nssm -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Source
if (-not $nssmPath) {
    # Fallback path if not in env var
    $nssmPath = "C:\Users\$env:USERNAME\AppData\Local\Microsoft\WinGet\Packages\NSSM.NSSM_Microsoft.Winget.Source_8wekyb3d8bbwe\nssm-2.24-101-g897c7ad\win64\nssm.exe"
}

Write-Host "🔹 Stopping old service (if exists)..."
& $nssmPath stop ClawdbotGateway 2>$null
& $nssmPath remove ClawdbotGateway confirm 2>$null

Write-Host "🔹 Installing Service..."
# Cấu hình chạy trực tiếp Node.exe để ẩn console hoàn toàn
& $nssmPath install ClawdbotGateway "C:\Program Files\nodejs\node.exe"
& $nssmPath set ClawdbotGateway AppParameters "scripts/run-node.mjs gateway"
& $nssmPath set ClawdbotGateway AppDirectory "G:\AIHub\clawdbot"
& $nssmPath set ClawdbotGateway Description "Clawdbot Gateway Service"

# Thiết lập môi trường
& $nssmPath set ClawdbotGateway AppEnvironmentExtra "USERPROFILE=C:\Users\$env:USERNAME" "APPDATA=C:\Users\$env:USERNAME\AppData\Roaming" "LOCALAPPDATA=C:\Users\$env:USERNAME\AppData\Local"

# Cấu hình ẩn console và auto-restart
& $nssmPath set ClawdbotGateway AppNoConsole 1
& $nssmPath set ClawdbotGateway AppStopMethodSkip 0
& $nssmPath set ClawdbotGateway AppStopMethodConsole 0

Write-Host "🔹 Starting Service..."
& $nssmPath start ClawdbotGateway

Write-Host "✅ DONE! Service installed and running."
& $nssmPath status ClawdbotGateway
```

---

## 🚀 Bước 2: Chạy cài đặt

1. Mở **PowerShell (Admin)**.
2. Chạy lệnh:
   ```powershell
   C:\Scripts\setup-clawdbot-service.ps1
   ```

---

## 📊 Kiểm tra & Quản lý

### Kiểm tra trạng thái
```powershell
sc query ClawdbotGateway
```
Hoặc xem trong **Task Manager** > Tab **Services**.

### Khởi động / Dừng / Restart
```powershell
sc start ClawdbotGateway
sc stop ClawdbotGateway
# Restart = Stop rồi Start
```

### Xem log (nếu có lỗi)
Bot vẫn ghi log vào thư mục temp cũ hoặc bạn có thể cấu hình log riêng bằng lệnh:
```powershell
nssm set ClawdbotGateway AppStdout "C:\Scripts\clawdbot.log"
nssm set ClawdbotGateway AppStderr "C:\Scripts\clawdbot.log"
```
(Nhớ restart service sau khi set log).

---

## ⚠️ Xử lý lỗi thường gặp

1. **Lỗi "Service paused" hoặc tắt ngay sau khi bật:**
   - Kiểm tra xem cổng **18999** (hoặc 18789) có bị chiếm dụng không.
   - Thử chạy lệnh thủ công: `node scripts/run-node.mjs gateway` xem có lỗi gì không.

2. **Lỗi "Access Denied":**
   - Đảm bảo bạn đang chạy PowerShell với quyền **Run as Administrator**.

3. **Hiện cửa sổ pop-up liên tục:**
   - Do xung đột với Task Scheduler hoặc script cũ. Hãy chạy file `kill-all-clawdbot.bat` để dọn dẹp sạch sẽ trước khi cài service.
