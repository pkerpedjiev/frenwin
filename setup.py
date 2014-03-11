from distutils.core import setup

setup(name='ernwin',
      version='0.1',
      description='FRET Pipeline Using Ernwin',
      author='Peter Kerpedjiev',
      author_email='pkerp@tbi.univie.ac.at',
      url='http://www.tbi.univie.ac.at/~pkerp/frenwin/',
      scripts=['scripts/dsu_to_fasta.py', 'scripts/frenwin.py']
     )
