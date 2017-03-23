#!/bin/bash

# Filter out lyrics files that are too small

for song in `ls lyrics/*.txt`
do
    chars=`wc -c $song | cut -d ' ' -f 1`
    if (( chars < 3 ))
    then
        mv $song bad_lyrics/whisps/
    elif (( chars < 40 ))
    then
        mv $song bad_lyrics/questionable/
    fi
done
