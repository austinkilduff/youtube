# Brings dst directory into parity with src directory
# The use case I have is for syncing my mp3 player, e.g.
# python jibe.py ~/Music/ ~/mnt/Music/

import os
import sys

src = sys.argv[1]
dst = sys.argv[2]

# src_files is the list of paths, relative to src, for all files
# Keeping them relative makes comparing src and dst contents easier
src_root = None
src_files = []
for root, directories, files in os.walk(src):
    if not src_root:
        src_root = root + '/'
    for filename_abs in files:
        filename_rel = os.path.join(root, filename_abs)[len(src_root):]
        src_files.append(filename_rel)

# Ditto for dst_files
dst_root = None
dst_files = []
for root, directories, files in os.walk(dst):
    if not dst_root:
        dst_root = root + '/'
    for filename_abs in files:
        filename_rel = os.path.join(root, filename_abs)[len(dst_root):]
        dst_files.append(filename_rel)

src_set = set(src_files)
dst_set = set(dst_files)

# TODO: Files in src but not in dst should be copied from src to dst
# TODO: Files in dst but not in src should be deleted from dst
# TODO: Files in both src and dst should be ignored
print('To be copied from src', src_root, 'to dst', dst_root)
print(src_set - dst_set)

print('To be deleted from dst', dst_root)
print(dst_set - src_set)



# Copy files from src to dst, creating directories where needed
# Here (and below) it makes more sense to use absolute paths
for filename_rel in src_set - dst_set:
    filename_abs = src_root + filename_rel

# Delete files from dst, and purge empty directories
for filename_rel in dst_set - src_set:
    filename_abs = dst_root + filename_rel
