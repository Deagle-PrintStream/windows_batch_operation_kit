# windows_batch_operation_kit
Some simple python scripts for easy batch operations on windows list rename or move.

## batch rename

A simple script to batch rename files in same directory.

Arguments to input: target directory; substring for filter;prefix for rename; suffix for rename; sort order
A complete well-rounded example:`$python batch_rename -d D:/pictures/pixiv R12/ -ss *.jpg -pf anime_ -sf .jpg -so mtime`
Easy mode to modify all files in one dir:`$python bathc_rename -ez D:/pictures/pixiv R12/`
Or you can directly luanch the script by `$python batch_rename` and input parameters within.
Wherein -d and -ss are necessary.If -sf left default then original suffix remains still.Sort order choices: mtime, ctime, atime, size, name.

*Note: If the new sequentail name already exists in this directory, then the old file rename would be skipped*
