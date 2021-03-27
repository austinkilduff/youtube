# Brings dst directory into parity with src directory
# The use case I have is for syncing my mp3 player, e.g.
# python jibe.py ~/Music/ ~/mnt/Music/

import os
import sys

src = sys.argv[1]
dst = sys.argv[2]

src_root = None
src_files = []
for root, directories, files in os.walk(src):
    if not src_root:
        src_root = root + '/'
    for name in files:
        rel_path = os.path.join(root, name)[len(src_root):]
        src_files.append(rel_path)

dst_root = None
dst_files = []
for root, directories, files in os.walk(dst):
    if not dst_root:
        dst_root = root + '/'
    for name in files:
        rel_path = os.path.join(root, name)[len(dst_root):]
        dst_files.append(rel_path)

src_set = set(src_files)
dst_set = set(dst_files)

# TODO: Files in src but not in dst should be copied from src to dst
# TODO: Files in dst but not in src should be deleted from dst
# TODO: Files in both src and dst should be ignored
print('To be copied from src', src_root, 'to dst', dst_root)
print(src_set - dst_set)

print('To be deleted from dst', dst_root)
print(dst_set - src_set)
