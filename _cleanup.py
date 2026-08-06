import os, shutil
dirs = [
    r'D:\Dự Án Cá Nhân\xuanloi.me\src\i18n',
    r'D:\Dự Án Cá Nhân\xuanloi.me\src\components\i18n',
]
for d in dirs:
    if os.path.exists(d):
        shutil.rmtree(d)
        print(f'Removed: {d}')
    else:
        print(f'Not found: {d}')

# Restore astro.config.mjs from git
import subprocess
result = subprocess.run(['git', 'checkout', 'astro.config.mjs'], cwd=r'D:\Dự Án Cá Nhân\xuanloi.me', capture_output=True)
print('astro config:', result.stdout.decode().strip() or 'restored')
