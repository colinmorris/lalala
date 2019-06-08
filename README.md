Investigating repetition in pop music. Interested in questions like:

- Has pop music been getting more (or less) repetitive over time?
- Which songs/artists/genres are the most/least repetitive?

I'm measuring repetitiveness of a song by how well gzip can compress it. (Which sounds cheeky, but I think it can actually be justified when you look at how Lempel-Ziv compression works.)

The investigations from this repo were a precursor to a visual essay I did for Pudding.cool: [Are Pop Lyrics Getting More Repetitive?](https://pudding.cool/2017/05/song-repetition). The code for that essay lives at https://github.com/polygraph-cool/song-repetition

## Brief overview of calculating lyric compressibility

1. Put lyrics in text files (making sure they're ASCII encoded)
2. Compress those text files using gzip (I used the -9 flag to maximize the compression efficiency)
3. Run [infgen](https://github.com/madler/infgen) on each gzip file, redirecting the output to a file. (See `badromance_infgen.txt` for an example of what one of these files looks like)
4. Run `parse_ratio` from `parse_infgen.py` on those files. This returns a tuple of the original (uncompressed) and compressed sizes (in bytes/characters). The ratio of those two numbers will give you the compression ratio.

Roughly speaking, `parse_ratio` calculates the compressed size using only the Lempel-Ziv part of the DEFLATE compression performed by gzip (and not the Huffman coding part). Infgen is what lets us separate those steps. The compressed size is calculated by treating a 'match' (i.e. a pointer backwards to an earlier portion of the text which is repeated) as costing 3 bytes. This is close to reality, but also just gives intuitively reasonable results for my purposes. You can increase the cost (to put more emphasis on longer repeated sequences, and avoid spurious repetitions on short character sequences) or decrease it - it shouldn't have a huge effect.

### Lazy version

Run steps 1 and 2 above, then just look at the ratio between the file sizes of the original (text) files and the gzip files. The disadvantage is that this also incorporates the Huffman coding step (which is not relevant to the natural sense of 'repetitiveness' of song lyrics), and adds a constant amount of overhead (from the gzip header, and the huffman table), which can distort the rankings for very short texts. But overall, the rankings you get with this method will be pretty close to the more principled one above.
