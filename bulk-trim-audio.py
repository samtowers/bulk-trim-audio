import os
import shutil
import argparse
from typing import Iterator
import mutagen
import ffmpeg

FADE_SECS = 4

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
        raise ValueError('main_dir must be a valid directory.')
    if os.path.isfile(args.backup_dir):
        raise ValueError('backup_dir must not be a file.')
    if args.ignore and not os.path.isfile(args.ignore):
        raise ValueError('--ignore should be a valid text file or left unset.')
    # if os.path.split(args.main_dir)[0]:
    #     raise ValueError('main_dir must not be a nested folder or file. '
    #                      +'It must be a folder which exists in the current working directory.')
    return args


def main():
    try:
        args = fetch_args()
    except ValueError as e:
        return print('Error: ' + str(e))

    keywords = parse_ignore_file(args.ignore)

    if not args.dry_run and not args.yes:
        reply = input("Warning: This will modify files in the supplied directory. "
                      + "Please backup your audio folder before proceeding.\nContinue? [y/n]: ").lower()
        while reply not in ['y', 'n']:
            reply = input('Please input y or n: ').lower()
        if reply != 'y':
            return

    all_audio = get_audio_files(args.main_dir, keywords)
    # Get audio exceeding max duration. File paths will only be required after this.
    long_audio:list[str] = [f.filename for f in all_audio if f.info.length > args.length_mins * 60]
        
    if not long_audio:
        return print('No applicable audio files detected. Exiting.')
        
    print('\Processing audio files:')
    for f in long_audio:
        # Backup file:
        file_relpath = os.path.relpath(f, args.main_dir)
        backup_file = os.path.normpath(os.path.join(args.backup_dir, file_relpath))
        if os.path.isfile(backup_file):
            print('SKIPPING ' + os.path.basename(f) + ': Backup file already exists: ' + backup_file)
            continue
        os.makedirs(os.path.dirname(backup_file), exist_ok=True)
        print('Move: ', f, '->', backup_file)
        shutil.move(f, backup_file)
        print('Creating trimmed version in original location... ', end='')
        transform_audio(backup_file, f, args.length_mins*60)
        print('Done.')
        # todo Dry run.
        
    print('\nBatch complete.')
    
    
def transform_audio(infile:str, outfile:str, trim_secs:int) -> None:
    (
    ffmpeg
    .input(infile)
    .filter('atrim', end=trim_secs)
    .filter('afade', t='out', st=(trim_secs-FADE_SECS), d=FADE_SECS)
    .output(outfile, loglevel="error")
    .run()
    )


def get_audio_files(root_dir: str, ignore_keywords: list[str]) -> list[mutagen.FileType]:
    files = list(get_files_recursive(root_dir))
    if ignore_keywords:
        files = [f for f in files if not contains_a_keyword(f, ignore_keywords)]
    audio_files = [parse_audio_file(f) for f in files]
    return [a for a in audio_files if a != None]


def parse_audio_file(file_path: str) -> mutagen.FileType | None:
    try:
        return mutagen.File(file_path)
    except mutagen.MutagenError:
        return None


def contains_a_keyword(subject: str, keywords: list[str]) -> bool:
    return any(word in subject.lower() for word in keywords)


def get_files_recursive(root_dir: str) -> Iterator[str]:
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            yield os.path.join(root, file)

def parse_ignore_file(ignore_file: str) -> list[str]:
    """
    Get list of keywords, lowercase and trimmed.
    """
    if not ignore_file:
        return []
    with open('file.txt', 'r') as f:
        return [line.strip().lower() for line in f if bool(line.strip())]


if __name__ == '__main__':
    main()