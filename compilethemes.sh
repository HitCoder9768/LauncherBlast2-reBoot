#! /bin/sh
# hacky workaround for theme garbage

# init the themes file
echo "themes = {}" > qss/themes.py

# look for theme files, and load them into the file
FILES=$(find qss/*.qss)

for f in $FILES
do
    echo "themes[\"${basename $f .qss}\"] = \"\"\"" >> qss/themes.py
    echo "\"\"\"" >> qss/themes.py
done