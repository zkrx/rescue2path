#!/usr/bin/python3

import sys
import subprocess

if len(sys.argv) != 4:
  print("Usage: " + sys.argv[0] + " ddrescue.mapfile /dev/sdxy part_offset_in_bytes")
  sys.exit(-1)

DELIM = "  "
BLOCK_SIZE = 4096
mapfile = sys.argv[1]
device = sys.argv[2]
part_offset = sys.argv[3]

def find_path_by_block(addr, size):
  print("Block @ " + hex(addr) + " of size " + hex(size) + " bytes:")
  block_number = int((int(addr) - int(part_offset)) / BLOCK_SIZE)
  debugfs = subprocess.Popen(["debugfs"], stdin = subprocess.PIPE,
                             stdout = subprocess.PIPE, encoding = "utf-8")
  # each command is echoed back
  # open
  debugfs.stdin.write("open " + str(device) + "\n")
  debugfs.stdin.flush()
  line = debugfs.stdout.readline()

  # testb
  debugfs.stdin.write("testb " + str(block_number) + "\n")
  debugfs.stdin.flush()
  line = debugfs.stdout.readline()
  line = debugfs.stdout.readline()
  if "not" in line:
    # unused block
    print(line)

    # quit
    debugfs.stdin.write("q\n")
    debugfs.stdin.flush()
    return

  # icheck
  debugfs.stdin.write("icheck " + str(block_number) + "\n")
  debugfs.stdin.flush()
  line = debugfs.stdout.readline() # echoed command
  line = debugfs.stdout.readline() # "Block Inode number"
  line = debugfs.stdout.readline() # inode
  inode = line.split('\t')[1]

  # ncheck
  debugfs.stdin.write("ncheck " + str(inode) + "\n")
  debugfs.stdin.flush()
  line = debugfs.stdout.readline() # echoed command
  line = debugfs.stdout.readline() # "Inode Pathname"
  line = debugfs.stdout.readline() # path
  print(line)

  # quit
  debugfs.stdin.write("q\n")
  debugfs.stdin.flush()

def find_all_paths(addr, size):
  addr = int(addr, 16)
  size = int(size, 16)
  while size > 0:
    find_path_by_block(addr, BLOCK_SIZE)
    size -= BLOCK_SIZE
    addr += BLOCK_SIZE


with open(mapfile) as fp:  
  lines = fp.read().splitlines()

  for line in lines:
    cols = line.split(DELIM)

    if cols[0].startswith("#"):
      # ignore comments
      continue

    # -: bad block
    # /: unscraped
    if len(cols) == 3 and (cols[2] == '-' or cols[2] == '/'):
        find_all_paths(cols[0], cols[1])
