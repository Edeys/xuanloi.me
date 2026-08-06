"""
cPanel UAPI helper for xuanloi.me hosting management.
Usage:
    from cpanel import Cpanel
    cp = Cpanel()
    cp.list_files("/home/ktixknjc/public_html")
    cp.upload("/path/local.txt", "/home/ktixknjc/public_html")
    cp.read("/home/ktixknjc/public_html/robots.txt")
    cp.write("/home/ktixknjc/public_html/robots.txt", "content")
    cp.deploy_zip(zip_path)  # upload + extract via PHP
"""
import json, os, io, time
import requests, warnings

warnings.filterwarnings("ignore")

CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "deploy-config.json")

class Cpanel:
    def __init__(self, config_path=CONFIG_PATH):
        with open(config_path, "r", encoding="utf-8") as f:
            self.cfg = json.load(f)
        self.base = f"https://{self.cfg['host']}:{self.cfg['port']}"
        self.user = self.cfg["username"]
        self.token = self.cfg["api_token"]
        self.root = self.cfg["web_root"]
        self.site = self.cfg["site_url"]
        self.s = requests.Session()
        self.s.verify = False
        self.s.headers["Authorization"] = f"cpanel {self.user}:{self.token}"

    def _uapi(self, module, func, params=None, data=None, files=None, method="get"):
        url = f"{self.base}/execute/{module}/{func}"
        if method.lower() == "get":
            r = self.s.get(url, params=params, timeout=30)
        else:
            r = self.s.post(url, params=params, data=data, files=files, timeout=120)
        try:
            return r.json()
        except:
            return {"errors": [r.text[:200]], "status": 0}

    def _ok(self, result):
        return result.get("status") == 1 and not result.get("errors")

    # ===== File operations =====
    def list_files(self, path=None, filter_=None):
        path = path or self.root
        params = {"dir": path}
        if filter_:
            params["filter"] = filter_
        return self._uapi("Fileman", "list_files", params).get("data", [])

    def read(self, path, file):
        r = self._uapi("Fileman", "get_file_content", {"dir": path, "file": file})
        if self._ok(r):
            return r["data"].get("content", "")
        return None

    def write(self, path, file, content):
        r = self._uapi("Fileman", "save_file_content",
                       data={"dir": path, "file": file, "content": content},
                       method="post")
        return self._ok(r)

    def upload(self, local_path, remote_dir):
        """Upload a NEW file (fails if exists)."""
        fname = os.path.basename(local_path)
        with open(local_path, "rb") as f:
            files = {"file-0": (fname, f)}
            r = self._uapi("Fileman", "upload_files", 
                           params={"dir": remote_dir}, files=files, method="post")
        return self._ok(r)

    def upload_overwrite(self, local_path, remote_dir):
        """Upload file, deleting first via FTP if exists."""
        fname = os.path.basename(local_path)
        # Try delete via FTP first (UAPI has no delete on this server)
        self._ftp_delete(remote_dir, fname)
        return self.upload(local_path, remote_dir)

    # ===== FTP fallback =====
    def _ftp(self):
        import ftplib
        ftp = ftplib.FTP(self.cfg["ftp_host"])
        ftp.login(self.cfg["ftp_user"], self.cfg["ftp_pass"])
        ftp.set_pasv(True)
        return ftp

    def _ftp_delete(self, remote_dir, fname):
        ftp = self._ftp()
        rel = remote_dir.replace(self.root, "").replace("\\", "/")
        remote = f"/public_html{rel}/{fname}".replace("//", "/")
        try:
            ftp.delete(remote)
            return True
        except:
            return False
        finally:
            ftp.quit()

    def ftp_upload(self, local_path, remote_dir):
        """FTP upload (creates or overwrites)."""
        ftp = self._ftp()
        rel = remote_dir.replace(self.root, "").replace("\\", "/")
        remote = f"/public_html{rel}/{os.path.basename(local_path)}".replace("//", "/")
        # Ensure dirs exist
        parts = remote.rsplit("/", 1)[0].split("/")
        cur = ""
        for p in parts:
            cur += p + "/"
            try: ftp.mkd(cur)
            except: pass
        with open(local_path, "rb") as f:
            ftp.storbinary(f"STOR {remote}", f)
        ftp.quit()
        return True

    # ===== Deploy =====
    def deploy(self, zip_path):
        """Full deploy: FTP upload ZIP + PHP extract with cache purge."""
        import io
        # 1. Upload ZIP via FTP (handles large files better)
        ftp = self._ftp()
        zip_name = os.path.basename(zip_path)
        with open(zip_path, "rb") as f:
            ftp.storbinary(f"STOR /public_html/{zip_name}", f)
        ftp.quit()

        # 2. PHP extractor script
        php = (
            "<?php "
            "function rmrf($d){if(!is_dir($d))return;foreach(scandir($d)as$f){"
            "if($f=='.'||$f=='..')continue;$p=\"$d/$f\";is_dir($p)?rmrf($p):unlink($p);}"
            "rmdir($d);} "
            f"rmrf('{self.root.replace('/home/ktixknjc', '.')}'); "
        )
        # simpler: extract to web root relative to public_html
        php = (
            "<?php "
            "function rmrf($d){if(!is_dir($d))return;foreach(scandir($d)as$f){"
            "if($f=='.'||$f=='..')continue;$p=\"$d/$f\";is_dir($p)?rmrf($p):unlink($p);}"
            "rmdir($d);} "
            "rmrf('.prerender');rmrf('_astro');"
            f"$z=new ZipArchive;if($z->open('{zip_name}')===TRUE)"
            f"{{$z->extractTo('.');$z->close();unlink('{zip_name}');unlink(__FILE__);"
            "echo'OK-'.date('Y-m-d H:i:s');}else{echo'FAIL';}?>"
        )
        bio = io.BytesIO(php.encode())
        ftp2 = self._ftp()
        ftp2.storbinary(f"STOR /public_html/_deploy.php", bio)
        ftp2.quit()

        # 3. Trigger
        r = requests.get(f"{self.site}/_deploy.php", verify=False, timeout=120)
        return "OK" in r.text, r.text.strip()

    def verify(self, url="/llms.txt", keyword="xuanloi"):
        r = requests.get(f"{self.site}{url}", verify=False, timeout=15)
        return r.status_code == 200 and keyword in r.text


if __name__ == "__main__":
    cp = Cpanel()
    print("=== Connection test ===")
    info = cp._uapi("ServerInformation", "get_information")
    print(f"Server info: {'OK' if cp._ok(info) else 'FAIL'}")
    files = cp.list_files()
    print(f"Root files: {len(files)}")
    robots = cp.read(cp.root, "robots.txt")
    print(f"robots.txt: {len(robots) if robots else 0} chars")
