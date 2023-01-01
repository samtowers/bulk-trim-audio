# Bulk Trim Audio
Trim/crop extended music in bulk.
```
batch-trim-audio.py dir newdir [--cutoff-mins 16] [--ignore keywords.txt] [--dry-run] [--yes]
```
All audio files nested within `dir` will be trimmed if their duration exceeds `--cutoff-mins` (default: 16); audio already shorter than this will be ignored. 

Trimmed audio is reduced to `(cutoff-mins - 1)` minutes. E.g. audio longer than `16` minutes will be trimmed to exactly `15` minutes. This it to provide a gap between the cutoff duration and new duration. 

A four second fadeout will be applied to the end of trimmed audio.

Impacted audio files will be backed-up into `newdir` before being trimmed. This is done to preserve a copy of the file with its original duration. `newdir` will be created if it doesn't exist.  Any nested folder structures will also be recreated within `newdir`.

## Optional Arguments

`--cutoff-mins [integer]`

Default: `16`. Max duration of audio before a trim is required.


`--ignore [text file]`

Avoid trimming audio files containing certain keywords in their full filepath. Supply a text file with each line containing an ignore keyword. Keywords are not case sensitve.

`--dry-run`

Do not modify the file system. Info and impacted audio files are still printed to console.

`--yes`

Skip warning prompts demanding user input.

# Installation

Clone this repository.

Install project dependencies:

```pip install -r requirements.txt```

`ffmpeg` must be installed on your system and be present in  `$PATH`.