#!/usr/bin/python

import re
import sys
import os
import os.path as op
from optparse import OptionParser

def main():
    usage = """
    python dsu_to_fasta.py file.dsu

    Convert a dsu file (from Marcelo) to a set of fasta files containing an id,
    a sequence and a secondary structure to be used as input to ernwin.
    """
    num_args= 1
    parser = OptionParser(usage=usage)

    parser.add_option('-o', '--output-dir', dest='output_dir', default='fastas_temp', help="The directory where to store each fasta file", type='str')
    parser.add_option('-n', '--first-n', dest='first_n', default=-1, help='Output only the first n structures as fasta files', type='int')
    #parser.add_option('-u', '--useless', dest='uselesss', default=False, action='store_true', help='Another useless option')

    (options, args) = parser.parse_args()

    if len(args) < num_args:
        parser.print_help()
        sys.exit(1)

    if not op.exists(options.output_dir):
        os.makedirs(options.output_dir)

    counter = 0

    with open(args[0], 'r') as f:
        lines = iter(f)
        seq = lines.next().strip()

        for line in lines:
            if len(line.strip()) == 0:
                continue

            print >>sys.stderr, line
            m = re.search('([\d]+)\t([\.\(\)\[\]]+)', line)
            ss_str = m.group(2)
            id_str = m.group(1)

            out_str = ">%s\n%s\n%s\n" % (id_str, seq, ss_str)

            if options.first_n > 0:
                if counter >= options.first_n:
                    break

            with open(op.join(options.output_dir, id_str + ".fa"), 'w') as f1:
                print >>sys.stderr, "writing...", op.join(options.output_dir, id_str + ".fa")
                f1.write(out_str)
                counter += 1

if __name__ == '__main__':
    main()

