#!/usr/bin/python

import re
import sys
from optparse import OptionParser

def main():
    usage = """
    python scrips/grep_dists2.py log.txt

    Find the distances output by ernwin.
    """
    num_args= 1
    parser = OptionParser(usage=usage)

    #parser.add_option('-d', '--dist-num', dest='dist_num', default=1, help="Place holder for a real option", type='int')
    #parser.add_option('-u', '--useless', dest='uselesss', default=False, action='store_true', help='Another useless option')

    (options, args) = parser.parse_args()

    if len(args) < num_args:
        parser.print_help()
        sys.exit(1)

    if args[0] == '-':
        f = sys.stdin
    else:
        f = open(args[0], 'r')

    prog = re.compile("native_energy \[([\d]+) [\d]+\]*.*")
    dist_re = re.compile('dist2: (.*?)\]') 

    for line in f:
        m = prog.match(line)

        if m is None:
            continue

        sequence_number = m.group(1)
        distances = []

        for m in dist_re.finditer(line):
            if len(m.groups()) == 1:
                distances += [m.group(1)]

        print sequence_number, ' '.join(distances)

if __name__ == '__main__':
    main()

