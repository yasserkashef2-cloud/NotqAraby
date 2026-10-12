#!/usr/bin/env python3
"""Copy the supplied media into ../assets/media under ASCII names (<id>.<ext>) and
re-encode the one oversize file (158 MB, over GitHub's 100 MB per-file limit).
Usage: python3 -I prepare_media.py <folder-with-extracted-Audiovisuals.zip>"""
import os, shutil, subprocess, sys
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE)
from media_map import MEDIA
ROOT=os.path.dirname(HERE); OUT=os.path.join(ROOT,'assets','media'); os.makedirs(OUT,exist_ok=True)
src_root=sys.argv[1]
for m in MEDIA:
    ext=os.path.splitext(m['src'])[1].lower()
    dst=os.path.join(OUT,m['id']+ext)
    src=os.path.join(src_root,m['src'])
    if os.path.exists(dst): continue
    if m['heavy']:
        cmd=['ffmpeg','-v','error','-y','-i',src,'-vf','scale=480:-2','-c:v','libx264','-crf','32','-preset','slow','-r','25',
             '-c:a','aac','-b:a','48k','-ac','1','-movflags','+faststart',dst]
        print('re-encoding',m['id']); subprocess.run(cmd,check=True)
    else:
        shutil.copy(src,dst)
print('media ready:',len(os.listdir(OUT)),'files')
