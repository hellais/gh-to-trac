## Github to Trac migration

This tool is used to transfer github issues to trac.

An example of it's usage can be seen here:

`./bin/gh-to-trac -u cypherpunks -p writecode -r TheTorProject/ooni-probe -t https://trac.torproject.org/projects/tor -c Ooni`

This will migrate all of the issues stored on the github
TheTorProject/ooni-probe repo to the torproject trac for component "Ooni".
