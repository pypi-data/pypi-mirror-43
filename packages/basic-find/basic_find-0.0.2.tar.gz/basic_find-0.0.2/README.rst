basic\_find
===========

Basic find program, cut-down version of unix ‘find’. Walks a file
hierarchy.

-  [x] find . -name ‘\*.txt’
-  [x] find temp -type f
-  [x] find . -type d
-  [ ] find . -name '\*.rb' -exec rm {} ;

Run as follows:

-  [x] python -m basic\_find . -name ‘\*.txt’
-  [x] python -m basic\_find temp -type f
-  [x] python -m basic\_find . -type d
