import os
import argparse
import mutagen


class ProgramArgs(argparse.Namespace):
    main_dir: str
    backup_dir: str
    length_mins: int
    ignore: str
    dry_run: bool
    yes: bool


def fetch_args() -> ProgramArgs:
    parser = argparse.ArgumentParser()
    parser.add_argument('main_dir', type=str, help='Input dir')
    parser.add_argument('backup_dir', type=str, help='Backup dir name')
    parser.add_argument('--length-mins', type=int, default=15, help='Max duration before a file is trimmed')
    parser.add_argument('--ignore', type=str, default='', help='Text file containing keywords')
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--yes', action='store_true')

    # Using `namespace`: See https://stackoverflow.com/a/42279784
    args = parser.parse_args(namespace=ProgramArgs())
    if not os.path.isdir(args.main_dir):
        raise ValueError('main_dir must be a directory.')
    if args.ignore and not os.path.isfile(args.ignore):
        raise ValueError('--ignore should be a valid text file or left unset.')
    # if os.path.split(args.main_dir)[0]:
    #     raise ValueError('main_dir must not be a nested folder or file. '
    #                      +'It must be a folder which exists in the current working directory.')
    return args


def main():
    # Get args:
    try:
        args = fetch_args()
    except ValueError as e:
        return print('Error: ' + str(e))

    # Warn user:
    if not args.dry_run and not args.yes:
        reply = input(
            "Warning: This will modify files in the supplied directory. Please backup your audio folder before proceeding.\nContinue? [y/n]: ").lower()
        while reply not in ['y', 'n']:
            reply = input('Please input y or n: ').lower()
        if reply != 'y':
            
            return

    print(get_audio_files(args))

    for file_path in get_audio_files(args):
        file:mutagen.FileType = mutagen.File(file_path)
        if file.info.length <= args.length_mins * 60: # Skip short files.
            continue
        print(file_path)
    

    # Files exceeding duration:


def get_audio_files(args: ProgramArgs) -> list[str]:
    ignore_keywords: list[str] = parse_ignore_keywords(args.ignore)
    # Find acceptable audio files:
    files = get_files_recursive(args.main_dir)
    audio_files = list(filter(lambda f: is_audio_file(f), files))
    if not ignore_keywords:
        return audio_files
    return list(filter(lambda f: not is_ignored_file(f, ignore_keywords), files))


def is_audio_file(file_path: str) -> bool:
    try:
        return mutagen.File(file_path) != None
    except mutagen.MutagenError:
        return False

# Check if file path contains keyword in `--ignore` list:


def is_ignored_file(file_path: str, ignore_keywords: list[str]) -> bool:
    return any(word in file_path.lower() for word in ignore_keywords)


def get_files_recursive(root_dir: str) -> list[str]:
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            yield os.path.join(root, file)

# Get list of keywords, lowercase and trimmed.


def parse_ignore_keywords(ignore_file: str) -> list[str]:
    if not ignore_file:
        return []
    with open('file.txt', 'r') as f:
        return [line.strip().lower() for line in f if bool(line.strip())]


if __name__ == '__main__':
    main()


"""

# Define the file path and the base directory
file_path = '/root/dir1/dir2/file.txt'
base_directory = '/root/dir1'

# Get the file path relative to the base directory
relative_path = os.path.relpath(file_path, base_directory)
print(relative_path)
"""
