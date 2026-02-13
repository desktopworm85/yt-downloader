import os
import json
import shutil
import time
import urllib.request
from urllib.error import URLError, HTTPError

ASSET_NAME = "yt-downloader.exe"
GITHUB_LINK = f"https://api.github.com/repos/desktopworm85/yt-downloader/releases/latest"

def _https_get_json(url: str) -> dict:
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read().decode("utf-8"))

def get_latest_release_info():
    data = _https_get_json(GITHUB_LINK)
    tag = data.get("tag_name", "")
    assets = data.get("assets", [])
    asset_url = None
    for a in assets:
        if a.get("name") == ASSET_NAME:
            asset_url = a.get("browser_download_url")
            break
    return asset_url, tag

def download(url:str) -> str:
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req, timeout=60) as resp:
        with open("yt-downloader.exe", "wb") as f:
            shutil.copyfileobj(resp,f)

backup = "yt-downloader.exe.old"

time.sleep(0.8)

if os.path.exists(backup):
    os.remove(backup)

info = get_latest_release_info()

try:
    if os.path.exists("yt-downloader.exe"):
        os.replace("yt-downloader.exe", backup)
    
    download(info[0])
    with open("lib/ver.txt", "w") as f:
        f.write(info[1])
        f.close()
except Exception as e:
    print(e)

    try:
        if os.path.exists(backup) and not os.path.exists("yt-downloader.exe"):
            os.replace(backup, "yt-downloader.exe")
    except Exception as e2:
        print(f"Rollback failed")

time.sleep(0.1)
os.system("yt-downloader.exe")
