import os
import shutil

RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RESET = "\033[0m"

def read_paths_from_file(file_path):
    source_dirs = []
    target_dirs = []

    with open(file_path, "r") as file:
        for line in file:
            line = line.strip()
            if line.startswith("local:"):
                source_dirs.append(line.split(":", 1)[1].strip())
            elif line.startswith("server:"):
                target_dirs.append(line.split(":", 1)[1].strip())

    return source_dirs, target_dirs
  
def sync_files(src_dir, dst_dir):
    print(GREEN + "------------sync begin-----------" + RESET)
    os.makedirs(dst_dir, exist_ok=True)

    update_file_cnt = 0
    for root, dirs, files in os.walk(src_dir):
        relative_path = os.path.relpath(root, src_dir)
        dst_sub_dir = os.path.join(dst_dir, relative_path)
        os.makedirs(dst_sub_dir, exist_ok=True)
        for file in files:
            src_file = os.path.join(root, file)
            dst_file = os.path.join(dst_sub_dir, file)
            src_mtime = os.path.getmtime(src_file)
            if not os.path.exists(dst_file) or os.path.getmtime(dst_file) < src_mtime:
                shutil.copy2(src_file, dst_file)
                update_file_cnt += 1
                print("Update ", YELLOW + dst_file + RESET)
    return update_file_cnt

path_file_path = input("Enter the path to the path.txt file: ")
if path_file_path == '':
    current_directory = os.getcwd()
    path_file_path = os.path.join(current_directory, 'path.txt')
    print(path_file_path)


source_dirs, target_dirs = read_paths_from_file(path_file_path)
dst_info = []
for src_dir, dst_dir in zip(source_dirs, target_dirs):
    print("Sync from '{src_dir}' to '{dst_dir}'...")
    cnt = sync_files(src_dir, dst_dir)
    print(GREEN + "------------ sync end-----------" + RESET)
    dst_info.append((dst_dir, cnt))
for dst in dst_info:
    print(RED + "Update " + dst[0] + " " + str(dst[1]) + " " + "files" + RESET)
