#!/bin/sh

# Set the common prefix to strip
PREFIX="https://data.sdss5.org/sas/"

# Set the remote host (used in rsync://)
REMOTE_HOST="sdss5@dtn.sdss.org"

# Input file with full rsync paths
FILELIST="lvmvis_DRP_urls.dat"

# File containing password (must be mode 600 and do not commit it to git!!!!)
PASSWORD_FILE="../.rsync-password"

# Read file list line by line
while IFS= read -r full_path; do
    # Remove the prefix
    relative_path="${full_path#$PREFIX}"

    # Extract the file name (flattening)
    filename=$(basename "$relative_path")

    # Sync the file via rsync://
    CMD="rsync -avzP --no-motd --no-relative --password-file $PASSWORD_FILE rsync://$REMOTE_HOST/$relative_path ./$filename"
    echo "$CMD"
    $CMD
done < "$FILELIST"
