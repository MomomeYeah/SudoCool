SudoCool
========

Tired of manually solving Sudoku puzzles?  Haven't realised that half the internet is sudoku?  Then SudoCool is the project for you!

This is mostly a learning experience to learn Django and Python.  I haven't got the faintest idea what I'm doing.

TODO
----

* solveBoard function works, but should return something after loop terminates.  What's the right return value?
* we're doing way too much work - if we guess right that means we've solved the board, we should just return

* Show steps taken to solve puzzle
* Show intermediate steps and how they were calculated
* Store separate board for each update or just list of increments?
* Click particular tiles to see their answer, rather than seeing them all at once?
* Create puzzle with id/uuid for future reference
* URL entry field should be URL type, i.e. .com button for mobile
* Manual entry boxes should be number type
* AJAX URL fetch