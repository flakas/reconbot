wget https://www.fuzzwork.co.uk/dump/sqlite-latest.sqlite.bz2
mkdir datadump
bzip2 -d sqlite-latest.sqlite.bz2
mv sqlite-latest.sqlite datadump/
