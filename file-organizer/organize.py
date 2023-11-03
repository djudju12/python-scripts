#!/usr/bin/python3

import yaml, os, glob, sys

CONFIG_PATH="organizer.yaml"
LOG_ACTIVE = False

def main():
    global LOG_ACTIVE

    args = shift_args(sys.argv)
    if "--verbose" in args or "-v" in args:
        LOG_ACTIVE = True
        remove_anyway(args, "--verbose")
        remove_anyway(args, "-v")

    if len(args) > 0:
        match args[0]:
            case "-h" | "--help":
                usage()
                return
            
            case "-i" | "--init":
                init_config()
                return
            
            case "-a" | "--add":
                args = shift_args(args)
                if len(args) < 2:
                    usage_add()
                    return

                add_config(dir=args[0], paths=args[1:])
                return

            case _: 
                usage()
                return

    config = read_config(CONFIG_PATH)
    for dir, file_patterns in config.items():
        if type(file_patterns) is not list:
            log(f"Invalid config file. \"{dir}\" does not contains a list of paths.")
            continue
        
        for pattern in file_patterns:
            for file in file_list(pattern):
                move_file(file, dir)

def log(msg: str) -> None:
    if LOG_ACTIVE:
        print(msg)

def usage() -> None:
    print("Usage: organize [OPTIONS]")
    print("Options:")
    print("  -h, --help\t\tShow this message.")
    print("  -v, --verbose\t\tLog information.")
    print("  -i, --init\t\tCreate a new config file.")
    print("  -a, --add\t\tAdd a entry to the config file.")

def usage_add() -> None:
    print("Usage: organize -a | --add [DIR] [PATH_PATTERN...]")

def shift_args(args) -> list[str]:
    if len(args) > 1:
        return args[1:]
    return []

def path_exists(path: str) -> bool:
    return os.path.exists(path)

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

def init_config() -> None:
    if path_exists(CONFIG_PATH):
        log(f"Config file \"{CONFIG_PATH}\" already exists.")
        if input("Want to overwrite? (y/n): ") != "y":
            exit(0)

    config = {"Documents": ["*.pdf"]}
    log(f"Creating new config file \"{CONFIG_PATH}\"")
    save_config(config, CONFIG_PATH)

def read_config(path: str) -> dict[str, str]:
    # why yml and yaml? oh god
    if path_not_exists(path):
        name, ext = os.path.splitext(path)
        if ext != ".yaml" and ext != ".yml":
            log(f"Invalid config file. \"{path}\" is not a yaml file.")
            exit(1)

        # try again
        ext = ".yml" if ext == ".yaml" else ".yaml"
        path = f"{name}{ext}"
        if path_not_exists(path):
            log(f"Config file \"{path}\" does not exist.")
            exit(1)

    with open(path, "r") as f:
        return yaml.safe_load(f)

def save_config(config: dict[str, str], path: str) -> None:
    with open(path, "w") as f:
        yaml.dump(config, f)

def add_config(dir: str, paths: list[str], config_path: str = CONFIG_PATH) -> None:
    config = read_config(config_path)
    for path in paths:
        if dir in config and path not in config[dir]:
            config[dir].append(path)
        elif dir not in config:
            config[dir] = [path]
        else:
            return # its all good

    save_config(config, config_path)

def file_list(pathname: str) -> list[str]:
    for file in glob.glob(pathname):
        yield file

def remove_anyway(list, item):
    try:
        list.remove(item)
    except ValueError:
        pass

if __name__ == '__main__':
    main()