import subprocess, os, glob

base = r'D:\Dự Án Cá Nhân\xuanloi.me\dist'
ssh_key = r'C:\Users\xuanl\.ssh\do-9router'
server = 'root@129.212.238.158'
dest = '/var/www/xuanloi.me/'

# Use scp with compression for speed
cmd = f'scp -i {ssh_key} -C -r'
cmd += f' "{base}\index.html" "{base}\robots.txt" "{base}\rss.xml" "{base}\sitemap-index.xml" "{base}\sitemap-0.xml" "{base}\404.html" "{base}\500.html" "{base}\favicon.svg" "{base}\og.png" "{base}\site.webmanifest" "{base}\_astro" "{base}\pagefind" "{server}:{dest}"'

p = subprocess.run(cmd, shell=True, capture_output=True, timeout=180)
print('STDOUT:', p.stdout.decode('utf-8',errors='replace')[-300:])
print('STDERR:', p.stderr.decode('utf-8',errors='replace')[-300:])
print('RC:', p.returncode)
