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

def path_not_exists(path: str) -> bool:
    return not os.path.exists(path)

def file_exists(path: str) -> bool:
    return os.path.exists(path) and os.path.isfile(path)

def move_file(file: str, dst: str) -> None:
    if path_not_exists(dst):
        log(f"Dir \"{dst}\" does not exist. Creating...")
        os.mkdir(dst)

    if file_exists(file):
        log(f"Moving {file} to {dst}")
        os.rename(file, f"{dst}/{file}")

def dir_exists(path: str) -> bool:
    return os.path.exists(path) and os.path.isdir(path)

def read_config(path: str) -> dict[str, str]:
    # why yml and yaml? oh god
    if path_not_exists(path):
        name, ext = os.path.splitext(path)
        if ext != "yaml" and ext != "yml":
            log(f"Invalid config file. \"{path}\" is not a yaml file.")
            exit(1)

        # try again
        ext = "yml" if ext == "yaml" else "yaml"
        path = f"{name}.{ext}"
        if path_not_exists(path):
            log(f"Config file \"{path}\" does not exist.")
            exit(1)

    with open(path, "r") as f:
        return yaml.safe_load(f)

def file_list(pathname: str) -> list[str]:
    for file in glob.glob(pathname):
        yield file

if __name__ == '__main__':
    main()