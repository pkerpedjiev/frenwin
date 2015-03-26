#!/usr/bin/python

import glob
import os
import os.path as op
import subprocess as sp
import sys

import forgi.utilities.debug as fud
from optparse import OptionParser

def main():
    usage = """
    python jing_pipeline dsu_file dist1 dist2

    The results will all be placed in the directory where
    dsu_file exists. The fastas will be placed in fastas_dsu_file.
    The structures will be placed in structures_dsu_file.
    """
    num_args= 3
    parser = OptionParser(usage=usage)

    #parser.add_option('-o', '--options', dest='some_option', default='yo', help="Place holder for a real option", type='str')
    #parser.add_option('-u', '--useless', dest='uselesss', default=False, action='store_true', help='Another useless option')
    parser.add_option('-n', '--first-n', dest='first_n', default=-1, help='Output only the first n structures as fasta files', type='int')
    parser.add_option('-i', '--ernwin-iterations', dest='ernwin_iterations', default=10000, 
                      help='The number of iterations to run ernwin for', type='int')

    (options, args) = parser.parse_args()

    if len(args) < num_args:
        parser.print_help()
        sys.exit(1)

    try:
        dist1 = int(args[1])
        dist2 = int(args[2])
    except ValueError as ve:
        print >>sys.stderr, "The nucleotides between which to calculate the distances need to be entered as numbers"
        return

    # Create the fasta files
    directory, filename = op.split(args[0])
    filebase, extension = op.splitext(filename)
    output_directory = op.join(directory, "fastas_" + filebase)
    ernwin_output_directory = op.join(directory, 'ernwin-output')

    if not op.exists(output_directory):
        os.makedirs(output_directory)


    # create the fasta files
    fud.pv('"*" + output_directory + "*"')
    p = sp.Popen(['dsu_to_fasta.py',
                  '-o', output_directory,
                  '-n', str(options.first_n),
                  args[0]])
    out, err = p.communicate()

    fastas_list = glob.glob(op.join(output_directory, "*.fa"))

    scons_text = """
import glob
import os
import os.path as op

env = Environment(ENV=os.environ)

fastas_list = glob.glob(op.join("{}", "*.fa"))
ernwin_output_directory = "{}"
for fasta in fastas_list:
    fa_id = op.splitext(op.basename(fasta))
    target_file = op.join(ernwin_output_dir, fa_id, "log.txt") 
    env.Command(target=target_file, source=fasta, action="ernwin_go.py --dist1 {} --dist2 {} --output-dir {} --log-to-file")
""".format(output_directory, ernwin_output_directory, dist1, dist2, ernwin_output_directory)

    with open(op.join(op.dirname(args[0]), 'SConstruct'), 'w') as f:
        f.write(scons_text)

    '''
    print >>sys.stderr, "fastas_list:", fastas_list

    print "directory:", directory, "filebase:", filebase
    # run ernwin in parallel
    command = ['parallel',
                  '-j', '4',
                  'ernwin_go.py',
                  '-i', str(options.ernwin_iterations),
                  '--dist1', str(dist1),
                  '--dist2', str(dist2),
                  '--output-dir', ernwin_output_directory,
                  '--log-to-file', ":::"]  + fastas_list
    print "command:", command
    p = sp.Popen(command)
    out, err = p.communicate()
    '''

if __name__ == '__main__':
    main()

