# Deploy Guide — xuanloi.me

## One-time setup (server)

Set permissions on web root:

```bash
ssh -i <SSH_KEY_PATH> root@<SERVER_IP>
chown -R www-data:www-data /var/www/xuanloi.me
find /var/www/xuanloi.me -type d -exec chmod 755 {} \;
find /var/www/xuanloi.me -type f -exec chmod 644 {} \;
```

Or add this to `/etc/rc.local` to auto-fix on reboot:

```bash
cat >> /etc/rc.local <<EOF
find /var/www/xuanloi.me -type d -exec chmod 755 {} \;
find /var/www/xuanloi.me -type f -exec chmod 644 {} \;
EOF
```

## Deploy (Windows)

```powershell
.\scripts\deploy.ps1
```

## Deploy (Linux/Mac)

```bash
npm run build
scp -i <SSH_KEY_PATH> -C -r dist/* root@<SERVER_IP>:/var/www/xuanloi.me/
ssh -i <SSH_KEY_PATH> root@<SERVER_IP> "find /var/www/xuanloi.me -type d -perm 700 -exec chmod 755 {} \;"
ssh -i <SSH_KEY_PATH> root@<SERVER_IP> "nginx -t && systemctl reload nginx"
```

## Verify

```bash
curl -sI https://xuanloi.me/        # 200
curl -sI https://xuanloi.me/posts/  # 200 (MUST be 200, not 403)
curl -sI https://xuanloi.me/tags/   # 200
curl -sI https://xuanloi.me/about/  # 200
```

## Lưu ý

- Folder permissions từ SCP luôn `700` → cần `chmod 755` sau mỗi deploy
- Đã tạo `scripts\deploy.ps1` tự động fix permissions
