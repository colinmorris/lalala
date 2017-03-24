#!/bin/bash

bads=`grep '\[' lyrics/*.txt | cut -d ':' -f 1 | sort | uniq`
nbad=`echo "$bads" | wc -l`
echo "Moving $nbad braced lyrics files"
for bad in $bads
do
    mv $bad bad_lyrics/braces/
    rm $bad.gz
done
