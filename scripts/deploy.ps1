param(
    [string]$Server = "root@129.212.238.158",
    [string]$DistPath = "D:\Dự Án Cá Nhân\xuanloi.me\dist",
    [string]$WebRoot = "/var/www/xuanloi.me",
    [string]$SshKey = "C:\Users\xuanl\.ssh\do-9router"
)

Write-Host "=== Deploying xuanloi.me ===" -ForegroundColor Cyan

# 1. Build
Write-Host "[1/5] Building..." -ForegroundColor Yellow
Set-Location "D:\Dự Án Cá Nhân\xuanloi.me"
npm run build
if ($LASTEXITCODE -ne 0) { Write-Host "BUILD FAILED!" -ForegroundColor Red; exit 1 }

# 2. Upload
Write-Host "[2/5] Uploading to $Server..." -ForegroundColor Yellow
Set-Location $DistPath
scp -i $SshKey -C -r * "${Server}:${WebRoot}/"
if ($LASTEXITCODE -ne 0) { Write-Host "UPLOAD FAILED!" -ForegroundColor Red; exit 1 }

# 3. Fix permissions (critical!)
Write-Host "[3/5] Fixing permissions..." -ForegroundColor Yellow
ssh -i $SshKey $Server "find $WebRoot -type d -perm 700 -exec chmod 755 {} \; 2>/dev/null; chmod -R 755 $WebRoot 2>/dev/null; echo 'permissions fixed'"

# 4. Reload nginx
Write-Host "[4/5] Reloading nginx..." -ForegroundColor Yellow
ssh -i $SshKey $Server "nginx -t && systemctl reload nginx && echo 'nginx reloaded'"

# 5. Verify
Write-Host "[5/5] Verifying..." -ForegroundColor Yellow
ssh -i $SshKey $Server "curl -sI https://xuanloi.me/ 2>&1 | head -1"
ssh -i $SshKey $Server "curl -sI https://xuanloi.me/posts/ 2>&1 | head -1"

Write-Host "=== Deploy complete! ===" -ForegroundColor Green
