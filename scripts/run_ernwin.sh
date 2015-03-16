#!/usr/bin/bash

find fastas_temp -name "*.fa" | parallel -j 4 ernwin_go.py --dist1 14 --dist2 76 --stats-file ~/projects/ernwin/fess/stats/combined.stats --output-dir ernwin-output/ --log-to-file {}

find fastas_temp -name "*.fa" | xargs -n 1 python ../../scripts/prepare_from_ss.py
find ernwin-output/ -name "log.txt" | xargs cat | awk '{sub(/\[/,"",$2); print $2, $21}' > ernwin-info/all_distances.csv
