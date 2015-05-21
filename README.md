## Simulate FRET Data Using Ernwin ##

For usage instructions see [the webpage](http://www.tbi.univie.ac.at/~pkerp/frenwin/).

Build documentation:

sphinx-build -b html doc ~/public_html/frenwin

find experiments/2015.05.08/ernwin-output-14-96/ -name "log.txt" | xargs cat  | python scripts/grep_dists.py - > experiments/2015.05.08/ernwin_distances_14_96.csv
