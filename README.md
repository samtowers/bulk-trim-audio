# Bulk Trim Audio
Trim/crop extended music in bulk.
```
batch-trim-audio.py dir newdir [--length-mins 15] [--ignore keywords.txt] [--dry-run] [--yes]
```
All audio files nested within `dir` will be trimmed if their duration exceeds `--length-mins` (default: 15); audio already shorter than this will be ignored.

A four second fadeout will be applied to the end of trimmed audio.

Impacted audio files will be backed-up into `newdir` before being trimmed. This is done to preserve a copy of the file with its original duration. `newdir` will be created if it doesn't exist.  Any nested folder structures will also be recreated within `newdir`.

## Optional Arguments

`--length-mins [integer]`

Default: `15`. Max duration of audio before a trim is required.


`--ignore [text file]`

Avoid trimming audio files containing certain keywords in their full filepath. Supply a text file with each line containing an ignore keyword. Keywords are not case sensitve.

`--dry-run`

Do not modify the file system. Info and impacted audio files are still printed to console.

`--yes`

Skip warning prompts demanding user input.
