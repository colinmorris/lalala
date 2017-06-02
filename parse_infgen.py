"""
WTK: pre-huffman compression ratio
"""

from __future__ import division
import re

fname = 'badromance_infgen.txt'

def parse_ratio(f, verbose=False):
    matches = 0
    n_literals = 0
    n_symbols = 0
    for line in f:
        if line.startswith('match'):
            _, length, dist = line.split()
            matches += 1

        pattern = r'! stats literals \d\.\d bits each \(\d+/(\d+)\)'
        p = re.compile(pattern)
        m = re.match(p, line)
        if m:
            n_literals = int(m.group(1))

        m = re.match(r'! stats total inout \d+:\d+ \((\d+)\)', line)
        if m:
            n_symbols = int(m.group(1))

        m = re.match(r'! stats total block average (\d+)\.\d uncompressed', line)
        if m:
            uncomp = int(m.group(1))

    if verbose:
        print "{} matches, {} literals, {} symbols".format(matches, n_literals, n_symbols)
        print "Uncompressed size = {} bytes".format(uncomp)
    assert matches + n_literals == n_symbols

    # 1 byte per literal, 3 bytes per match.
    pseudosize = matches * 3 + n_literals
    ratio = uncomp / pseudosize
    if verbose:
        print "{} / {} = {:.2f}".format(uncomp, pseudosize, ratio)
    return (uncomp, pseudosize)

if __name__ == '__main__':
    with open(fname) as f:
        parse_ratio(f, verbose=True)

