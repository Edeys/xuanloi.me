"""
Deploy xuanloi.me to DNCloud CP-2 hosting.
Usage: python scripts/deploy.py
"""
import os, sys, json, ftplib, requests, warnings, subprocess, io, zipfile

warnings.filterwarnings("ignore")

def load_config():
    cfg_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "deploy-config.json")
    if not os.path.exists(cfg_path):
        sys.exit("MISSING scripts/deploy-config.json (xem deploy-config.example.json)")
    with open(cfg_path, "r", encoding="utf-8") as f:
        return json.load(f)

CFG = load_config()
FTP = dict(host=CFG["ftp_host"], user=CFG["ftp_user"], passwd=CFG["ftp_pass"])
SITE = CFG.get("site_url", "https://xuanloi.me")
ROOT = CFG.get("ftp_root", "/public_html")
ZIP = "deploy_new.zip"

PHP = """<?php
function rmrf($d){if(!is_dir($d))return;foreach(scandir($d)as$f){if($f=='.'||$f=='..')continue;$p="$d/$f";is_dir($p)?rmrf($p):unlink($p);}rmdir($d);}
rmrf('.prerender');rmrf('_astro');
$z=new ZipArchive;if($z->open('%s')===TRUE){$z->extractTo('.');$z->close();unlink('%s');unlink(__FILE__);echo'OK-'.date('Y-m-d H:i:s');}else{echo'FAIL';}
?>"""

PROJ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIST = os.path.join(PROJ, "dist")

def build_ok():
    print("[1] Build...")
    r = subprocess.run("npm run build", shell=True, cwd=PROJ, capture_output=True, text=True)
    ok = "Complete!" in (r.stdout + r.stderr)
    print("  OK" if ok else f"  FAIL: {r.stderr[:150]}")
    return ok

def make_zip():
    print("[2] ZIP...")
    zp = os.path.join(PROJ, ZIP)
    if os.path.exists(zp): os.remove(zp)
    with zipfile.ZipFile(zp, "w", zipfile.ZIP_DEFLATED) as zf:
        for rt, dirs, files in os.walk(DIST):
            parts = os.path.relpath(rt, DIST).replace("\\", "/").split("/")
            if parts[0] == "assets" and len(parts) > 2 and parts[1] == "img": continue
            for fn in files:
                fp = os.path.join(rt, fn)
                arc = os.path.relpath(fp, DIST).replace("\\", "/")
                zf.write(fp, arc)
    print(f"  {os.path.getsize(zp)/1048576:.1f}MB")
    return zp

def upload(zp):
    print("[3] Upload...")
    ftp = ftplib.FTP(FTP["host"])
    ftp.login(FTP["user"], FTP["passwd"])
    ftp.set_pasv(True)
    with open(zp, "rb") as f:
        ftp.storbinary(f"STOR {ROOT}/{ZIP}", f)
    code = PHP % (ZIP, ZIP)
    ftp.storbinary(f"STOR {ROOT}/_deploy.php", io.BytesIO(code.encode()))
    ftp.quit()
    print("  Done")

def extract():
    print("[4] Extract...")
    r = requests.get(f"{SITE}/_deploy.php", verify=False, timeout=60)
    ok = "OK" in r.text
    print(f"  {'OK' if ok else r.text.strip()}")
    return ok

def clean(zp):
    print("[5] Clean...")
    if os.path.exists(zp): os.remove(zp)

if __name__ == "__main__":
    print("=" * 30); print("DEPLOY xuanloi.me"); print("=" * 30)
    if not build_ok(): sys.exit(1)
    zp = make_zip()
    upload(zp)
    if extract():
        clean(zp)
        print("DONE!")
    else:
        print("FAILED")
        sys.exit(1)
