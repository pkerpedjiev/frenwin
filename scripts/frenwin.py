#!/usr/bin/python

import os
import os.path as op
import subprocess as sp
import sys

import forgi.utilities.debug as fud
from optparse import OptionParser

def main():
    usage = """
    python jing_pipeline dsu_file

    The results will all be placed in the directory where
    dsu_file exists. The fastas will be placed in fastas_dsu_file.
    The structures will be placed in structures_dsu_file.
    """
    num_args= 1
    parser = OptionParser(usage=usage)

    #parser.add_option('-o', '--options', dest='some_option', default='yo', help="Place holder for a real option", type='str')
    #parser.add_option('-u', '--useless', dest='uselesss', default=False, action='store_true', help='Another useless option')
    parser.add_option('-n', '--first-n', dest='first_n', default=-1, help='Output only the first n structures as fasta files', type='int')

    (options, args) = parser.parse_args()

    if len(args) < num_args:
        parser.print_help()
        sys.exit(1)

    # Create the fasta files
    directory, filename = op.split(args[0])
    filebase, extension = op.splitext(filename)
    output_directory = op.join(directory, "fastas_" + filebase)

    if not op.exists(output_directory):
        os.makedirs(output_directory)

    fud.pv('"*" + output_directory + "*"')
    p = sp.Popen(['python',
                  'scripts/dsu_to_fasta.py',
                  '-o', output_directory,
                  '-n', str(options.first_n),
                  args[0]])
    out, err = p.communicate()

    print "directory:", directory, "filebase:", filebase


if __name__ == '__main__':
    main()

