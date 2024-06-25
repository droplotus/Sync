import os
import shutil
import hashlib
import argparse
import logging
import time

def show_md5(filename):
    hash = hashlib.md5()
    with open(filename, "rb") as f:
        while True:
            chunk = f.read(4096)
            if not chunk:
                break
            hash.update(chunk)
    return hash.hexdigest()

def sync_folders(source, replica):
    logging.info(f"Starting synchronization from {source} to {replica}")
    for src_dir, dirs, files in os.walk(source):
        relative_path = os.path.relpath(src_dir, source)
        dst_dir = os.path.join(replica, relative_path)

        print("====")
        print(src_dir)
        print(dirs)
        print(files)
        print("====")

        logging.debug(f"Processing source directory: {src_dir} -> Replica directory: {dst_dir}")

        if not os.path.exists(dst_dir):
            os.makedirs(dst_dir)
            logging.debug(f"Created directory: {dst_dir}")

        for file in files:
            src_file = os.path.join(src_dir, file)
            dst_file = os.path.join(dst_dir, file)
            if not os.path.exists(dst_file) or show_md5(src_file) != show_md5(dst_file):
                shutil.copy2(src_file, dst_file)
                logging.info(f"Copied {src_file} to {dst_file}")

        for r_file in os.listdir(dst_dir):
            full_r_file = os.path.join(dst_dir, r_file)
            if not os.path.exists(os.path.join(src_dir, r_file)):
                os.remove(full_r_file)
                logging.info(f"Removed {full_r_file}")


def main():
    parser = argparse.ArgumentParser(description='Sync two folders')
    parser.add_argument('source', help='Source dir path')
    parser.add_argument('replica', help='Replica dir path')
    parser.add_argument('log_path', help='Logfile txt path')
    parser.add_argument('interval', type=int, help='Interval in seconds')
    args = parser.parse_args()

    logging.basicConfig(filename=args.log_path, level=logging.INFO)

    while True:
        sync_folders(args.source, args.replica)
        time.sleep(args.interval)

if __name__ == "__main__":
    main()
