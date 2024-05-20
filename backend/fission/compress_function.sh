#!/bin/sh

# check if folder name is provided
if [ -z "$1" ]; then
  echo "Usage: $0 <folder_name>"
  exit 1
fi

FOLDER_NAME=$1
FUNCTIONS_DIR="./functions"

# check if functions directory exists
if [ ! -d "$FUNCTIONS_DIR" ]; then
  echo "Error: functions directory does not exist."
  exit 1
fi

# check if target folder exists
TARGET_DIR="$FUNCTIONS_DIR/$FOLDER_NAME"
if [ ! -d "$TARGET_DIR" ]; then
  echo "Error: $TARGET_DIR does not exist."
  exit 1
fi

# enter target folder
cd "$TARGET_DIR" || exit 1

# zip the folder
ZIP_FILE="../$FOLDER_NAME.zip"
zip -r "$ZIP_FILE" .

# back to the previous directory
cd - || exit 1

echo "Folder $FOLDER_NAME compressed to $ZIP_FILE"
