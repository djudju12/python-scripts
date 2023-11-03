#!/usr/bin/python3

import yaml, os, glob

CONFIG_PATH="organizer.yaml"
LOG_ACTIVE = True

def log(msg: str) -> None:
    if LOG_ACTIVE:
        print(msg)

def main():
    config = read_config(CONFIG_PATH)
    for dir, file_patterns in config.items():
        if type(file_patterns) is not list:
            log(f"Invalid config file. \"{dir}\" does not contains a list of paths.")
            continue
        
        for pattern in file_patterns:
            for file in file_list(pattern):
                move_file(file, dir)

def move_file(file: str, dst: str) -> None:
    if not os.path.exists(dst):
        log(f"Dir \"{dst}\" does not exist. Creating...")
        os.mkdir(dst)

    if os.path.exists(file) and os.path.isfile(file):
        log(f"Moving {file} to {dst}")
        os.rename(file, f"{dst}/{file}")

def read_config(path: str) -> dict[str, str]:
    if not os.path.exists(path):
        log(f"Config file \"{path}\" does not exist.")
        exit(1)

    with open(path, "r") as f:
        return yaml.safe_load(f)

def file_list(pathname: str) -> list[str]:
    for file in glob.glob(pathname):
        yield file

if __name__ == '__main__':
    main()