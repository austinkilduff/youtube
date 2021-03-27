# Brings dst directory into parity with src directory
# The use case I have is for syncing my mp3 player, e.g.
# python jibe.py ~/Music/ ~/mnt/Music/

import os
import sys

src = sys.argv[1]
dst = sys.argv[2]

# TODO: Files in src but not in dst should be copied from src to dst
# TODO: Files in dst but not in src should be deleted from dst
# TODO: Files in both src and dst should be ignored
for root, directories, files in os.walk(src):
    for name in files:
        print(os.path.join(root, name))
    for name in directories:
        print(os.path.join(root, name))

for root, directories, files in os.walk(dst):
    for name in files:
        print(os.path.join(root, name))
    for name in directories:
        print(os.path.join(root, name))
