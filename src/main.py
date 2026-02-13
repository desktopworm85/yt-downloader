import tkinter as tk
import tkinter.font as tkFont
import subprocess
import os
import json
import urllib.request
import sys
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
    return tag

def is_newer(latest_tag: str) -> bool:
    with open("lib/ver.txt", "r") as f:
        current_tag = f.read()
        f.close()
    
    if (latest_tag != current_tag):
        os.system("updater.exe")
        sys.exit()

is_newer(get_latest_release_info())

root = tk.Tk()
root.geometry("800x400")
root.title("Youtube Downloader")

app_font = tkFont.Font(family="Arial", size=20)

link_var = tk.StringVar()
choice = tk.StringVar(value="mp4")

def download():
    link = link_var.get()
    extChoice = choice.get()

    exe_path = "lib\yt-dlp.exe"
    if extChoice == "mp4":
        command = [exe_path, "-S", "res,ext:mp4:m4a", "--recode", "mp4", link]
    elif extChoice == "mp3":
        command = [exe_path, "-S", "res,ext:mp3:m3a", "--recode", "mp3", link]
    subprocess.run(command)

frame = tk.Frame(root)
frame.grid(row=1,column=0)

T = tk.Label(root, text="Youtube Downloader by Desktopworm", font=("Helvetica",35))
field = tk.Entry(frame, textvariable=link_var)
fieldLabel = tk.Label(frame, text="Link    ", font=app_font)
downButton = tk.Button(root, text="Download", command = download)
mp3Butt = tk.Radiobutton(frame, text="MP3", variable=choice, value="mp3")
mp4Butt = tk.Radiobutton(frame, text="MP4", variable=choice, value="mp4")

T.grid(row=0,column=0)
fieldLabel.grid(row=0,column=0)
field.grid(row=0,column=1)
mp3Butt.grid(row=1,column=0)
mp4Butt.grid(row=2,column=0)
downButton.grid(row=2,column=0)

root.mainloop()
